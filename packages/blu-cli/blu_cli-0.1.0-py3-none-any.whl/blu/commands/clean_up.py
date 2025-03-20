import questionary
from halo import Halo
from blu.utils.config import load_config, cache_blu_path
from blu.utils.run_command import run_command
from blu.utils.directories import locate_local_repo
import click

spinner = Halo(spinner="dots")


@click.option(
    "--file",
    type=str,
    default=None,
    help="Provide a specific path to run the clean up command on",
)
def clean_up(file):
    """Clean up and fix linting issues in the BLU codebase.

    \b
    Features:
        - Identifies and fixes Python linting issues using `flake8` and `black`.
        - Automatically reformats code to adhere to PEP8 standards.
        - Prompts the user to manually clean up any unresolved issues.
        - Provides a summary of resolved and unresolved linting issues after the process.
        - Exits cleanly with an "all clean" message if no issues are found.

    \b
    Considerations:
        - Ensure `flake8` and `black` are installed in your environment.
        - Review unresolved issues carefully, as they may require manual intervention.
        - Use this command as part of your workflow to maintain consistent coding standards.
    """

    config = load_config()

    # ensure BLU path has been set
    cache_blu_path(config)

    BLU_PATH = config["blu_path"]

    def run_flake8(target):
        """
        Run flake8 to check for linting issues.
        :return: List of files with linting issues.
        """
        try:
            output = run_command(
                f"flake8 {target} --ignore=E501,W503 --format=default",
                cwd=BLU_PATH,
                start=f"Checking for linting issues in {target}...",
                show_except=True,
                return_on_fail=False,
                return_fail_message=True,
            )

            spinner.succeed("flake8 completed.")

            if not output.strip():
                return []

            # Extract file paths with linting issues
            files_with_issues = set(line.split(":")[0] for line in output.splitlines())
            return sorted(files_with_issues)
        except Exception as e:
            spinner.fail(f"Failed to run flake8: {e}")
            return []

    def resolve_linting_issues(files_with_issues):
        """
        Automatically resolve linting issues in files.
        :param files_with_issues: List of file paths with linting issues.
        """
        for file_path in files_with_issues:
            spinner.info(f"Resolving issues in: {file_path}")
            try:
                # Use Black for formatting the file
                run_command(
                    f"black {file_path}",
                    cwd=BLU_PATH,
                    start=f"Auto-formatting {file_path}",
                )
                spinner.succeed(f"Formatted: {file_path}")
            except Exception as e:
                spinner.warn(f"Could not format {file_path} automatically: {e}")

        spinner.succeed("Completed resolving linting issues.")

    # Handle path detection
    if file:
        located_path = locate_local_repo(file_name=file)

        if not located_path:
            spinner.fail(
                f"Specified path '{file}' could not be located. Please check the name and try again."
            )
            return

        confirm_path = questionary.confirm(
            f"Located path: '{located_path}'. Do you want to run the clean-up on this path?"
        ).ask()

        if not confirm_path:
            spinner.info("Exiting as the path was not confirmed.")
            return

        file = located_path
    else:
        file = "."

    """
    Run the cleanup.
    Check if linting issues exist, execute cleanup with black if present
    """
    spinner.start("Running linting process...")
    files_with_issues = run_flake8(file)

    if not files_with_issues:
        spinner.succeed("No linting issues found! 🎉")
        return

    spinner.warn(f"Linting issues found in {len(files_with_issues)} file(s).")

    # Prompt user to clean up linting issues
    fix_issues = questionary.confirm(
        "Do you want to resolve these linting issues automatically?"
    ).ask()

    if not fix_issues:
        spinner.info("Exiting without making any changes.")
        return

    resolve_linting_issues(files_with_issues)

    # Run flake8 again to ensure no issues remain
    spinner.start("Re-checking linting after fixes...")
    remaining_issues = run_flake8(file)

    if not remaining_issues:
        spinner.succeed("All linting issues resolved! Your code is clean! 🎉")
    else:
        spinner.warn(f"Some linting issues remain in {len(remaining_issues)} file(s).")
        for f in remaining_issues:
            print(f" - {f}")
        spinner.info("Please review these files manually.")
