import click
import os
import getpass
from dotenv import load_dotenv

from blu.commands.gh_create import gh_create  # Import subcommands
from blu.commands.gh_add import gh_add
from blu.commands.gh_delete import gh_delete
from blu.commands.gh_readme import gh_readme
from blu.commands.build import build
from blu.commands.deploy import deploy
from blu.commands.linear import linear
from blu.commands.clean_up import clean_up

# Load the environment variables
env_file = ".env.dev" if os.getenv("ENV") == "dev" else ".env.prod"
load_dotenv(env_file)

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(
    context_settings=CONTEXT_SETTINGS,
    help=f"""
        BLU CLI - An AI-powered CLI Automating the entire Software Development Lifecycle

        Specify configs in the config.json file:\n
            /Users/{getpass.getuser()}/.config/blu

        More configuration info: blu --help config
    """,
    epilog="\nRun 'blu <command> --help, -h' for more details on a specific command.\n",
)
def blu():
    """"""


pass

# Access BLU_DEV_MODE
if os.getenv("BLU_DEV_MODE") == "1":
    print("Developer mode enabled.")

    blu.command("build")(build)
    blu.command("deploy")(deploy)
    blu.command("clean-up")(clean_up)


# Add subcommands to the CLI
blu.command("gh-create")(gh_create)
blu.command("gh-add")(gh_add)
blu.command("gh-delete")(gh_delete)
blu.command("linear")(linear)
blu.command("gh-readme")(gh_readme)

# Add future commands here
# blu.command("data-utils")(data_utils)
# blu.command("schedule-task")(schedule_task)

if __name__ == "__main__":
    blu()
