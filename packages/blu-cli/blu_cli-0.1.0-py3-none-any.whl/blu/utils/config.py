import os
import json
import questionary
from halo import Halo
import configparser
from blu.utils.run_command import run_command

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "blu")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
DEFAULT_CONFIG = {
    "github_username": None,
    "cached_directories": [],
    "blu_path": None,
}
spinner = Halo(spinner="dot")


def load_config():
    """Load configuration from the file or initialize default if it doesn't exist."""
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        spinner.info(
            f"Configuration file created at {CONFIG_FILE} with default values."
        )
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)

        # Merge the loaded config with the default config to include new keys
        updated_config = {**DEFAULT_CONFIG, **config}

        # If the config was updated with new keys, save it back to the file
        if config != updated_config:
            save_config(updated_config)
            spinner.info("Configuration file updated with new default keys....")

        return updated_config

    except json.JSONDecodeError:
        raise ValueError(
            f"Configuration file at {CONFIG_FILE} is not a valid JSON file."
        )

# this is a nonsenicle logic, anyone can open config and add themselves to the allowed_users -> should move to blu-services
def load_allowed_users():
    """Load configuration from the file or initialize default if it doesn't exist."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            return config.get("allowed_users", [])
    return []


def save_config(config):
    """Save configuration to the file."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)


def cache_username(config):
    # Cache GitHub username
    if not config["github_username"]:
        github_username = questionary.text("Enter your GitHub username:").ask()

        config["github_username"] = github_username.strip()
        save_config(config)
        spinner.info(f"GitHub username '{github_username}' saved for future use.")
    else:
        spinner.info(f"Using cached GitHub username: {config["github_username"]}")

    return config["github_username"]


def cache_blu_path(config):
    if not config["blu_path"]:
        blu_PATH = os.getcwd()
        config["blu_path"] = blu_PATH

        save_config(config)
        spinner.info(f"blu Path set as {blu_PATH}")
    else:
        spinner.info(f"Using cached Path: '{config["blu_path"]}'")

    return config["blu_path"]


def ensure_pypirc(test):
    """
    Ensure the .pypirc file exists and has valid credentials for the selected repository.
    If credentials are invalid, prompt the user to provide valid values.
    """
    spinner = Halo(spinner="dots")
    pypirc_path = os.path.expanduser("~/.pypirc")
    repository = "testpypi" if test else "pypi"

    if not os.path.exists(pypirc_path):
        spinner.warn(".pypirc file not found.")

        create_pypirc = questionary.confirm(
            "The .pypirc file does not exist. Would you like to create one?"
        ).ask()

        if not create_pypirc:
            spinner.fail("Deployment aborted. .pypirc file is required for upload.")
            exit(1)

        # Gather credentials to create a new .pypirc file
        username = questionary.text(
            f"Enter your {repository} username (e.g., '__token__'):"
        ).ask()
        password = questionary.password(f"Enter your {repository} token:").ask()

        # Create and populate the .pypirc file
        spinner.start("Creating .pypirc file...")
        config = configparser.ConfigParser()
        config["distutils"] = {"index-servers": "pypi\ntestpypi"}
        config["pypi"] = {
            "repository": "https://upload.pypi.org/legacy/",
            "username": username,
            "password": password,
        }
        config["testpypi"] = {
            "repository": "https://test.pypi.org/legacy/",
            "username": username,
            "password": password,
        }

        with open(pypirc_path, "w") as configfile:
            config.write(configfile)
        spinner.succeed(".pypirc file created successfully.")
    else:
        # Validate the existing .pypirc file
        spinner.start(f"Validating .pypirc file for {repository}...")
        config = configparser.ConfigParser()
        config.read(pypirc_path)

        if repository not in config.sections():
            spinner.fail(
                f"The .pypirc file does not contain credentials for {repository}."
            )
            update_credentials = questionary.confirm(
                "Would you like to add credentials now?"
            ).ask()

            if update_credentials:
                username = questionary.text(
                    f"Enter your {repository} username (e.g., '__token__'):"
                ).ask()
                password = questionary.password(f"Enter your {repository} token:").ask()

                config[repository] = {
                    "repository": f"https://{repository}.pypi.org/legacy/",
                    "username": username,
                    "password": password,
                }

                with open(pypirc_path, "w") as configfile:
                    config.write(configfile)
                spinner.succeed(f"Added credentials for {repository}.")
            else:
                spinner.fail("Deployment aborted.")
                exit(1)

        username = config[repository].get("username")
        password = config[repository].get("password")

        if not username or username != "__token__":
            spinner.warn(f"Invalid username in .pypirc for {repository}.")
            username = questionary.text(
                f"Enter your {repository} username (e.g., '__token__'):"
            ).ask()

            config[repository]["username"] = username

        if not password or password.lower() == "none":
            spinner.warn(f"Invalid or missing token in .pypirc for {repository}.")
            password = questionary.password(f"Enter your {repository} token:").ask()

            config[repository]["password"] = password

        with open(pypirc_path, "w") as configfile:
            config.write(configfile)

        spinner.succeed(f".pypirc file is valid for {repository}.")

    return True


# GH AUTH


def cache_gh_creds(config):
    """Check cached GitHub credentials before running any GH checks."""

    # If everything is cached, skip setup
    if (
        config.get("gh_installed")
        and config.get("git_configured")
        and config.get("gh_authenticated")
    ):
        spinner.succeed("All GitHub credentials are already set (cached).")
        return True

    # Run checks only if missing
    if not config.get("gh_installed"):
        config["gh_installed"] = check_gh_installed()
    if not config.get("git_configured"):
        config["git_configured"] = check_git_config()
    if not config.get("gh_authenticated"):
        config["gh_authenticated"] = check_gh_auth()

    save_config(config)
    return (
        config["gh_installed"]
        and config["git_configured"]
        and config["gh_authenticated"]
    )


def check_gh_installed():
    """Check if GitHub CLI is installed and install it if necessary."""
    try:
        result = run_command("gh --version", start="Checking for GitHub CLI...")
        if result:
            spinner.succeed("GitHub CLI is already installed.")
            return True
    except Exception:
        pass

    available_managers = detect_package_manager()
    if not available_managers:
        spinner.warn(
            "No supported package manager found. Please install GitHub CLI manually."
        )
        return False

    selected_choice = questionary.select(
        "Select a package manager to install GitHub CLI:",
        choices=[
            (f"{mgr} (Recommended)" if i == 0 else mgr, cmd)
            for i, (mgr, cmd) in enumerate(available_managers)
        ],
    ).ask()

    install_command = next(
        cmd for mgr, cmd in available_managers if mgr in selected_choice
    )
    if questionary.confirm(f"Install GitHub CLI using {selected_choice}?").ask():
        run_command(
            install_command, start=f"Installing GitHub CLI using {selected_choice}..."
        )
        spinner.succeed("GitHub CLI installed successfully.")
        return True

    return False


def check_git_config():
    """Check and prompt the user to set up Git global configuration if missing."""
    git_cred = run_command(
        "git config --global credential.helper", start="checking credential helper..."
    )
    git_name = run_command(
        "git config --global user.name", start="checking global config: username..."
    )
    git_email = run_command(
        "git config --global user.email", start="checking global config: email..."
    )

    # Identify missing configurations
    missing = {
        "credential.helper": git_cred,
        "user.name": git_name,
        "user.email": git_email,
    }

    # If everything is set, exit early
    if all(missing.values()):
        spinner.succeed("Git global configuration is correctly set.")
        return True

    spinner.warn(
        f"Missing Git global configuration: {', '.join(k for k, v in missing.items() if not v)}"
    )

    # Set Credential Helper First
    if not git_cred:
        git_cred = questionary.select(
            "Choose a Git authentication method:",
            choices=[
                "cache (Temporarily stores credentials)",
                "store (Saves credentials in plaintext)",
                "manager (Uses system credential manager, Windows only)",
                "osxkeychain (MacOS Keychain, Mac only)",
                "gpg (For signing commits, advanced users)",
            ],
        ).ask()
        run_command(
            f'git config --global credential.helper "{git_cred.split()[0]}"',
            start="Setting Git credential helper...",
        )

    # Set User Name and Email After Credential Helper
    if not git_name:
        git_name = questionary.text("Enter your Git user name:").ask()
        run_command(
            f'git config --global user.name "{git_name}"',
            start="Setting Git user name...",
        )

    if not git_email:
        git_email = questionary.text("Enter your Git user email:").ask()
        run_command(
            f'git config --global user.email "{git_email}"',
            start="Setting Git user email...",
        )

    spinner.succeed("Git global configuration updated successfully.")
    return True


def check_gh_auth():
    """Check GitHub authentication and prompt user if needed."""
    try:
        result = run_command(
            "gh auth status",
            start="Checking GitHub authentication...",
        )
        if "Logged in" in result:
            spinner.succeed("GitHub authentication is already set up.")
            return True
    except Exception:
        pass

    if questionary.confirm(
        "GitHub authentication is not set up. Would you like to log in now?"
    ).ask():
        run_command("gh auth login", start="Setting up GitHub authentication...")
        return check_gh_auth()

    spinner.warn(
        "You will need to manually enter credentials when using GitHub CLI commands."
    )
    return False


def detect_package_manager():
    """Detect available package managers dynamically for installing GitHub CLI."""
    package_managers = {
        "Darwin": [
            ("brew", "brew install gh"),
            ("port", "sudo port install gh"),
        ],  # macOS
        "Linux": [
            ("apt", "sudo apt update && sudo apt install gh -y"),
            ("dnf", "sudo dnf install gh -y"),
            ("pacman", "sudo pacman -S github-cli"),
            ("zypper", "sudo zypper install gh"),
            ("snap", "sudo snap install gh"),
            ("flatpak", "flatpak install flathub com.github.cli"),
        ],
        "Windows": [
            ("winget", "winget install --id GitHub.cli -e"),
            ("choco", "choco install gh"),
            ("scoop", "scoop install gh"),
        ],
    }

    os_type = os.uname().sysname
    available_managers = [
        (mgr, cmd)
        for mgr, cmd in package_managers.get(os_type, [])
        if run_command(f"command -v {mgr}", start="Detecting package managers...")
    ]
    return available_managers


# integrate in future versions
# (intended to help efficiency/relevancy of repo detection logic as everyone will not want to search starting from Developer)

"""
Usage - place these vars in any command that uses locate_local_repo

# Load configuration
config = load_config()

# Cache search paths and get whether default paths are being used
search_paths, using_default_paths = cache_search_paths(config)

# Locate a local repository
repo_path = locate_local_repo(repo_name, search_paths=search_paths, using_default_paths=using_default_paths)
"""


def cache_search_paths(config):
    """
    Cache the prioritized search paths for locating local repositories.

    :param config: The configuration dictionary.
    :return: The cached search paths and whether the user is using defaults.
    """
    # Check if the search paths are already cached
    if "search_paths" not in config or "using_default_paths" not in config:
        spinner.info("No search paths are cached. Let's set them up.")

        # Prompt the user if they want to use the default paths
        use_default = questionary.confirm(
            "Would you like to use the default search paths? (Developer directory and home directory)"
        ).ask()

        home_directory = os.path.expanduser("~")
        default_developer_path = os.path.join(home_directory, "Developer")
        default_paths = [default_developer_path, home_directory]

        if use_default:
            config["search_paths"] = default_paths
            config["using_default_paths"] = True
            save_config(config)
            spinner.info(f"Using default search paths: {default_paths}")
        else:
            spinner.info("Let's set up your custom search paths.")

            # Gather custom search paths from the user
            search_paths = []
            add_paths = True
            while add_paths:
                new_path = questionary.path(
                    "Enter a directory to include in your search paths:"
                ).ask()
                search_paths.append(new_path)

                add_paths = questionary.confirm(
                    "Would you like to add another directory?"
                ).ask()

            config["search_paths"] = search_paths
            config["using_default_paths"] = False
            save_config(config)
            spinner.info(f"Custom search paths cached successfully: {search_paths}")
    else:
        spinner.info(
            f"Using cached search paths: {config['search_paths']} (Default paths: {config['using_default_paths']})"
        )

    return config["search_paths"], config["using_default_paths"]
