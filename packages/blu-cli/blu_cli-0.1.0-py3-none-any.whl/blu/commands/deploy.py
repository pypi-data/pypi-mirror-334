import os
import questionary
import click
import getpass
from blu.utils.run_command import run_command, increment_version
from blu.utils.config import (
    load_allowed_users,
    cache_blu_path,
    load_config,
    ensure_pypirc,
)
from halo import Halo


@click.option("--test", is_flag=True, help="Push the package to TestPyPI.")
@click.option("--prod", is_flag=True, help="Push the package to Prod PyPI.")
@click.option(
    "--skip-sanity-check",
    is_flag=True,
    help="Skip the sanity check step before deployment",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Useful for additon logging in the case of no deploys",
)
@click.option("--major", is_flag=True, help="Increment the major version.")
@click.option("--minor", is_flag=True, help="Increment the minor version.")
@click.option("--patch", is_flag=True, help="Increment the patch version (default).")
def deploy(test, prod, skip_sanity_check, verbose, major, minor, patch):
    """Deploy the BLU package to PyPI or TestPyPI.

    \b
    Features:
        - Supports deployment to TestPyPI (testing environment) or PyPI (production).
        - Automatically increments the package version (major, minor, or patch).
        - Performs sanity checks on the build artifacts using `twine`.
        - Handles authentication and ensures credentials are valid in `.pypirc`.

    \b
    Considerations:
        - Ensure your `.pypirc` file is configured with valid credentials.
        - Use the `--test` flag to test the deployment before pushing to production.
    """
    spinner = Halo(spinner="dots")

    # Prevent Unauthorized Deployments
    username = getpass.getuser()
    allowed_users = load_allowed_users()

    if username not in allowed_users:
        spinner.fail(f"Unauthorized user: {username}.")
        spinner.info("Only maintainers can deploy this package.")
        exit(1)

    # Ensure the .pypirc file exists and has valid credentials
    ensure_pypirc(test)

    # Ensure BLU Path is Set
    config = load_config()
    cache_blu_path(config)
    BLU_PATH = config["blu_path"]

    # Confirm Deployment Environment
    env_choice = "testpypi" if test else "pypi"
    verbose = "--verbose" if verbose else ""
    version_type = "major" if major else "minor" if minor else "patch"

    if not questionary.confirm(
        f"Are you sure you want to deploy to {env_choice}?"
    ).ask():
        spinner.fail("Deployment aborted.")
        return

    # Prompt for Release Notes
    release_notes = questionary.text(
        "Enter release notes or changelog for this version (leave blank to skip):"
    ).ask()
    changelog_path = "CHANGELOG.md"

    if release_notes.strip():
        if not os.path.exists(changelog_path):
            with open(changelog_path, "w") as changelog_file:
                changelog_file.write("# Changelog\n\n")
            spinner.succeed(f"Created {changelog_path}.")
        with open(changelog_path, "a") as changelog_file:
            changelog_file.write(
                f"\n## {env_choice} Release Notes\n{release_notes.strip()}\n"
            )
        spinner.info("Release notes appended to CHANGELOG.md.")

    # Build the Package
    os.environ["ENV"] = "prod"  # Set environment to prod
    spinner.info("Environment variable 'ENV' set to 'prod'.")

    log_file = os.path.join(BLU_PATH, "sanity_check_errors.log")

    try:
        increment_version(BLU_PATH, version_type)
        run_command(
            "rm -rf dist/ build/ *.egg-info",
            BLU_PATH,
            start="Cleaning previous build artifacts...",
        )
        run_command("python3 -m build", BLU_PATH, start="Building the package...")
    except Exception as e:
        spinner.fail(f"Build failed: {e}")
        return

    # Sanity Check
    if not skip_sanity_check:
        try:
            run_command(
                "twine check dist/*",
                BLU_PATH,
                start="Performing sanity check on the build artifacts...",
            )
            spinner.succeed("Sanity check passed. No build issues detected.")

            # Remove the log file if the sanity check passes
            if os.path.exists(log_file):
                os.remove(log_file)

        except Exception as e:
            spinner.fail("Sanity check failed. Build contains errors.")
            with open(log_file, "w") as log_file_handle:
                log_file_handle.write(f"Sanity Check Errors:\n{str(e)}\n")
            spinner.info(f"Error details saved to: {log_file}")
            print(f"\nSanity Check Errors:\n{str(e)}")  # Print the log to the terminal
            return

    # Increment version
    if version_type == "patch" and not (major or minor or patch):
        spinner.info("No version flag provided. Defaulting to 'patch'.")

    # Push to PyPI or TestPyPI
    try:
        run_command(
            f"python3 -m twine upload --repository {env_choice} dist/* {verbose}",
            BLU_PATH,
            start=f"Pushing package to {env_choice}...",
        )
        spinner.succeed(f"Package successfully pushed to {env_choice}!")
    except Exception as e:
        spinner.fail(f"Deployment failed: {e}")
