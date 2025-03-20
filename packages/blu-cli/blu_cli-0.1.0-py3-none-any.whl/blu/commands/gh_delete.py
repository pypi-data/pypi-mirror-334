import questionary
from halo import Halo
from blu.utils.config import load_config, cache_gh_creds
from blu.utils.run_command import run_command, graceful_exit
from blu.utils.directories import locate_local_repo

spinner = Halo(spinner="dots")


def gh_delete():
    """Delete one or more repositories from your GitHub account and optionally their local copies.

    \b
    Features:
        - Supports single or bulk deletion of repositories.
        - Prompts to confirm deletions to avoid accidental removal.
        - Automatically detects and deletes local repositories if desired.
        - Provides the ability to skip local repository detection during the deletion process.

    \b
    Considerations:
        - Ensure you have admin rights and delete permissions for the GitHub repository.
        - Ensure that you want to permanently delete the selected repositories as this action cannot be undone.
    """

    # load config
    config = load_config()

    cache_gh_creds(config)

    # Determine single or bulk deletion
    delete_mode = questionary.select(
        "Would you like to perform a single deletion or bulk deletion?",
        choices=["Single Deletion", "Bulk Deletion"],
    ).ask()

    if delete_mode is None:
        graceful_exit()

    # Fetch the repositories using GitHub CLI
    repos_output = run_command(
        "gh repo list --json name -q '.[].name'", start="Fetching repositories..."
    )

    repos = repos_output.strip().split("\n")
    total_repos = None

    # Display selection instructions
    print(
        "\nNavigate the list using the arrow keys. Use the spacebar to select items. Press Enter to confirm your selection.\n"
    )

    if delete_mode == "Single Deletion":
        # Enforce only one selection
        selected_repos = questionary.checkbox(
            "Select the repository you want to delete (only one selection allowed):",
            choices=repos,
            validate=lambda choices: (
                "Please select exactly one repository." if len(choices) != 1 else True
            ),
        ).ask()

        if selected_repos is None:
            graceful_exit()

        repos_to_delete = selected_repos

    elif delete_mode == "Bulk Deletion":
        # Allow multiple selections
        selected_repos = questionary.checkbox(
            "Select the repositories you want to delete:",
            choices=repos + ["Select All"],
        ).ask()

        if selected_repos is None:
            graceful_exit()

        if "Select All" in selected_repos:
            repos_to_delete = repos
        else:
            repos_to_delete = selected_repos

        total_repos = len(repos_to_delete)

    # Proceed with deletion
    for index, repo in enumerate(repos_to_delete, start=1):

        spinner.info(f"Found remote repository: {repo}")

        if delete_mode == "Bulk Deletion":
            remaining_repos = total_repos - index
            spinner.warn(
                f"\nDeleting repository {index}/{total_repos}. Remaining repositories: {remaining_repos}\n"
            )

        confirm_delete = questionary.confirm(
            f"Are you sure you want to delete the remote repository '{repo}'?"
        ).ask()

        if confirm_delete is None:
            graceful_exit()

        if confirm_delete:
            try:
                # Delete the remote repository
                run_command(
                    f"gh repo delete {repo} --yes",
                    start=f"Deleting remote repository '{repo}'...",
                )
                spinner.succeed(f"Deleted remote repository: {repo}")

                # Locate the local repository
                local_path = locate_local_repo(repo_name=repo)

                if local_path:
                    # Confirm and delete the local repository
                    confirm_local_delete = questionary.confirm(
                        f"Local repository detected at '{local_path}'. Do you want to delete it?"
                    ).ask()

                    if confirm_local_delete is None:
                        graceful_exit()

                    if confirm_local_delete:
                        run_command(
                            f"rm -rf {local_path}",
                            start=f"Deleting local repository at '{local_path}'...",
                        )
                        spinner.succeed(f"Deleted local repository at: {local_path}")
                    else:
                        spinner.info(
                            f"Skipped deletion of local repository for '{repo}'."
                        )
                else:
                    spinner.warn(f"No matching local repository found for '{repo}'.")
            except Exception as e:
                spinner.fail(f"Failed to delete repository '{repo}': {e}")
        else:
            spinner.info(f"Skipped deletion of repository: {repo}")

    spinner.succeed("Completed deletion process!")

    if total_repos:
        spinner.warn(f"\nDeleted a total of {total_repos} Repositories!\n")
