import subprocess
import os
import sys
from halo import Halo


# Helper function to run shell commands
def run_command(
    command,
    cwd=None,
    start="Process",
    show_except=True,
    return_on_fail=False,
    return_fail_message=False,
):
    spinner = Halo(spinner="dots")
    """Run shell commands and display output."""
    try:
        spinner.start(start)
        result = subprocess.run(
            command, shell=True, cwd=cwd, check=True, text=True, capture_output=True
        )
        spinner.succeed(f"{start} - Completed successfully.")

        # Display the standard output
        return result.stdout.strip() if result.stdout else ""

    except subprocess.CalledProcessError as e:
        spinner.fail(f"{start} - Failed with error: ")

        if e.stdout or e.stderr:
            if show_except:
                fail_message = "\n".join(
                    output.strip() for output in [e.stdout, e.stderr] if output
                )
                spinner.fail(fail_message)

                if return_fail_message:
                    return fail_message

        if return_on_fail:
            return None
        sys.exit(1)

    except KeyboardInterrupt:
        # Handle user interrupt (CTRL + C) and exit cleanly
        spinner.warn(
            f"\nProcess interrupted. while executing `{command}` Exiting cleanly... 🚪"
        )
        sys.exit(1)  # Exit gracefully


def increment_version(BLU_PATH, version_type="patch"):
    """
    Increment the version number in setup.py for major, minor, or patch updates.

    :param setup_file: Path to the setup.py file.
    :param version_type: The part of the version to increment: 'major', 'minor', or 'patch'.
    """
    setup_file = os.path.join(BLU_PATH, "setup.py")

    spinner = Halo(spinner="dots")
    spinner.start(f"Incrementing {version_type} version in setup.py...")

    try:
        with open(setup_file, "r") as file:
            lines = file.readlines()

        new_lines = []
        version_found = False

        for line in lines:
            if "version=" in line:
                version_found = True
                # Extract the version
                version_str = line.split("=")[1].strip().strip('",')
                major, minor, patch = map(int, version_str.split("."))

                # Increment the correct part of the version
                if version_type == "major":
                    major += 1
                elif version_type == "minor":
                    minor += 1
                elif version_type == "patch":
                    patch += 1
                else:
                    raise ValueError(f"Invalid version type: {version_type}")

                # Update the line with the new version
                new_version = f"{major}.{minor}.{patch}"
                new_lines.append(f'    version="{new_version}",\n')
                spinner.succeed(f"Version updated to {new_version}.")
            else:
                new_lines.append(line)

        # If no version line is found, add one to the setup() function
        if not version_found:
            spinner.warn(
                "No version line found in setup.py. Adding a new version line."
            )
            new_version = "0.1.0"  # Default to initial version if no version is found
            for i, line in enumerate(new_lines):
                if (
                    "setup(" in line
                ):  # TODO: update after switching to toml (setup deprecated)
                    new_lines.insert(i + 1, f'    version="{new_version}",\n')
                    break
            spinner.succeed(f"Version initialized to {new_version}.")

        with open(setup_file, "w") as file:
            file.writelines(new_lines)

        return new_version
    except Exception as e:
        spinner.fail(f"Failed to increment version in setup.py: {e}")
        exit(1)


def graceful_exit():
    """
    Executes clean exit when user cancels an execution.
    """
    spinner = Halo(spinner="dots")
    spinner.warn("\nProcess interrupted. Exiting cleanly... 🚪")
    sys.exit(1)


def push_to_github(
    repo_name, local_repo_path, commit_message="Automated Push", add_path="."
):
    """
    Push README changes to GitHub.
    """
    spinner = Halo(spinner="dots")

    run_command(f"git add {add_path}", cwd=local_repo_path, start="Staging README...")
    run_command(
        f'git commit -m "{commit_message}"',
        cwd=local_repo_path,
        start="Committing changes...",
    )
    run_command(
        "git push origin main",
        cwd=local_repo_path,
        start="Pushing changes to GitHub...",
    )

    spinner.succeed(f"README successfully pushed to '{repo_name}' on GitHub.")
