import os
import re
import subprocess
import questionary
from halo import Halo
from blu.utils.config import load_config, cache_username, cache_gh_creds
from blu.utils.run_command import run_command, graceful_exit
from blu.utils.directories import locate_local_repo


def gh_add():
    """Push an existing local repository to a remote repository on GitHub.

    \b
    Features:
        - Detects if a remote repository with the same name exists in your GitHub account.
        - Allows you to create a new remote repository if none exists.
        - Automatically initializes a Git repository if the local directory is not already a Git repository.
        - Ensures an appropriate `.gitignore` file is present, adding common ignored files if necessary.
        - Handles upstream branch setup and prompts for user confirmation if changes are required.

    \b
    Considerations:
        - Ensure you are authenticated with the GitHub CLI (`gh auth login`) before using this command.
        - Only compatible with directories containing a valid Git repository or ready for initialization.
    """

    spinner = Halo(spinner="dots")

    # Load configuration
    config = load_config()

    cache_username(config)
    cache_gh_creds(config)

    # Confirm or locate the local repository
    use_current = questionary.confirm(
        "Do you want to use the current directory as the repository?"
    ).ask()

    if use_current:
        local_repo_path = os.getcwd()
    else:
        while True:
            # Prompt for the name of the existing local repository to locate
            repo_name = questionary.text(
                "Enter the name of the local repository to push:"
            ).ask()

            if repo_name is None:
                graceful_exit()

            # Validate against GitHub's naming rules
            if not re.match(r"^[a-zA-Z0-9]([a-zA-Z0-9_.-]*[a-zA-Z0-9])?$", repo_name):
                spinner.warn(
                    "Invalid repository name:\n Repository names must start and end with letters or numbers,\n "
                    "and can only contain letters, numbers, underscores, hyphens, and periods.\n No spaces are allowed."
                )
            else:
                # Try locating the repository
                local_repo_path = locate_local_repo(repo_name=repo_name)

                if not local_repo_path:
                    spinner.fail(f"Local repository '{repo_name}' not found.")
                    return
                break  # Exit the loop if a valid name and repository path are found

    # Confirm the detected local repository
    confirm_local_repo = questionary.confirm(
        f"Detected local repository at '{local_repo_path}'. Is this correct?"
    ).ask()

    if confirm_local_repo is None:
        graceful_exit()

    if not confirm_local_repo:
        spinner.info("Operation aborted.")
        return

    # Check if the directory is a Git repository

    os.chdir(local_repo_path)  # Change to the local repository directory

    if not os.path.exists(os.path.join(local_repo_path, ".git")):
        spinner.info(
            "This directory is not a Git repository. Initializing it as one..."
        )
        run_command(
            "git init", cwd=local_repo_path, start="Initializing Git repository"
        )
        spinner.succeed("Git repository initialized.")

    # Check for and update .gitignore
    gitignore_path = os.path.join(local_repo_path, ".gitignore")

    files_to_ignore = [
        "__pycache__/",
        "*.pyc",
        ".env",
        ".env.*",
        "venv/",
        ".DS_Store",
        "/node_modules",
        "/build",
        "/coverage",
        "/.pnp",
        ".pnp.js",
        "npm-debug.log*",
        "yarn-debug.log*",
        "yarn-error.log*",
        "*.log",
        "*.tmp",
    ]

    # Filter the list to include only files or directories that exist in the local repository
    existing_files_to_ignore = [
        entry
        for entry in files_to_ignore
        if os.path.exists(
            os.path.join(local_repo_path, entry.strip("/*"))
        )  # Check for directory existence
        or os.path.isfile(
            os.path.join(local_repo_path, entry.strip("*"))
        )  # Check for file existence
    ]

    if existing_files_to_ignore:
        # If no .gitignore file exists, create one
        if not os.path.exists(gitignore_path):
            spinner.info("No .gitignore file found. Creating one...")
            with open(gitignore_path, "w") as gitignore_file:
                gitignore_file.write("\n".join(existing_files_to_ignore) + "\n")
            spinner.succeed(".gitignore file created.")
        else:
            # If .gitignore exists, append missing entries
            with open(gitignore_path, "r") as gitignore_file:
                existing_entries = gitignore_file.read().splitlines()

            new_entries = [
                entry
                for entry in existing_files_to_ignore
                if entry not in existing_entries
            ]

            if new_entries:
                with open(gitignore_path, "a") as gitignore_file:
                    gitignore_file.write("\n".join(new_entries) + "\n")
                spinner.succeed(
                    f"Added missing entries to .gitignore: {', '.join(new_entries)}"
                )
    else:
        spinner.info("No matching files found to ignore. Skipping .gitignore creation.")

    # Check if a remote repository exists
    repo_name = os.path.basename(local_repo_path)
    spinner.start(f"Checking for existing remote repository named '{repo_name}'...")

    remote_repo_output = run_command(
        f"gh repo view {repo_name} --json name -q .name",
        cwd=local_repo_path,
        start="Checking remote repository",
        show_except=False,
        return_on_fail=True,
    )

    # Create a new remote repository if needed
    if not remote_repo_output:
        spinner.warn(f"No remote repository found for '{repo_name}'.")
        create_remote = questionary.confirm(
            f"No remote repository found for '{repo_name}'. Would you like to create one?"
        ).ask()

        if create_remote is None:
            graceful_exit()

        if create_remote:
            # Prompt user for repository details
            repo_description = questionary.text(
                "Enter a description for the repository:"
            ).ask()
            if repo_description is None:
                graceful_exit()
            private = questionary.confirm("Should the repository be private?").ask()
            if private is None:
                graceful_exit()

            # Determine visibility
            visibility = "private" if private else "public"

            # Create the repository
            try:
                run_command(
                    f"gh repo create {repo_name} --{visibility} --description '{repo_description}' --confirm",
                    cwd=local_repo_path,
                    start=f"Creating {visibility} repository on GitHub using GitHub CLI...",
                )
                spinner.succeed(
                    f"Created {visibility} repository on GitHub CLI successfully!"
                )
            except subprocess.CalledProcessError as e:
                spinner.fail(
                    f"Creating {visibility} repository on GitHub using GitHub CLI failed with error: {e.stderr}"
                )
                return
        else:
            spinner.info("Operation aborted. No remote repository created.")
            return
    else:
        spinner.succeed(
            f"Found existing remote repository: {remote_repo_output.strip()}"
        )

    # Push to existing remote repository
    confirm_push = questionary.confirm(
        f"Do you want to push the local repository to the remote repository '{repo_name}'?"
    ).ask()

    if confirm_push is None:
        graceful_exit()

    git_url = f"https://github.com/{config["github_username"]}/{repo_name}.git"

    if confirm_push:
        try:
            # Stage and commit changes
            run_command("git add .", cwd=local_repo_path, start="Staging changes")
            run_command(
                'git commit -m "Initial commit"',
                cwd=local_repo_path,
                start="Committing changes",
                return_on_fail=True,
                show_except=True,
            )
            run_command(
                "git branch -M main",
                cwd=local_repo_path,
                start="Setting default branch to main",
                return_on_fail=True,
                show_except=True,
            )

            # Always ensure a remote origin is added first
            remote_check_output = run_command(
                "git remote -v",
                cwd=local_repo_path,
                start="Ensuring remote origin is set...",
                return_on_fail=True,
                show_except=True,
            )

            if not remote_check_output or "origin" not in remote_check_output:
                run_command(
                    f"git remote add origin {git_url}",
                    cwd=local_repo_path,
                    start="Adding remote origin to current repository",
                )
                spinner.succeed("Remote origin added successfully.")
            else:
                spinner.succeed("Remote origin is already set.")

            # Check if upstream branch is already set
            upstream_output = run_command(
                "git rev-parse --abbrev-ref --symbolic-full-name @{u}",
                cwd=local_repo_path,
                start="Checking for upstream branch",
                show_except=True,
                return_on_fail=True,
            )

            if upstream_output:
                # Upstream branch already set
                spinner.warn("An upstream branch is already set for this repository.")
                reset_upstream = questionary.confirm(
                    "Would you like to reset the upstream branch to the current remote repository?"
                ).ask()

                if reset_upstream is None:
                    graceful_exit()

                if reset_upstream:
                    # Remove existing remote if needed and add a new one
                    run_command(
                        "git remote remove origin",
                        cwd=local_repo_path,
                        start="Removing existing remote origin",
                    )
                    run_command(
                        f"git remote add origin {git_url}",
                        cwd=local_repo_path,
                        start="Adding remote origin to current repository",
                    )
                    run_command(
                        "git push -u origin main",
                        cwd=local_repo_path,
                        start="Resetting and pushing to new upstream",
                    )
                    spinner.succeed(
                        "Successfully reset upstream branch and pushed to remote."
                    )
                else:
                    spinner.info(
                        "Skipped resetting upstream branch. Changes not pushed."
                    )
            else:
                # No upstream branch set, proceed with adding remote and pushing
                run_command(
                    "git push -u origin main",
                    cwd=local_repo_path,
                    start="Pushing to remote repository",
                )
                spinner.succeed("Successfully pushed local repository to remote.")

        except subprocess.CalledProcessError as e:
            spinner.fail(f"Failed to push to remote repository: {e}")
            return

    spinner.succeed("Completed repository push process!")
