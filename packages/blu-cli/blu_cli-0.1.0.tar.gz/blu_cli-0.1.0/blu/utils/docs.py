import difflib
import os
import sys
import questionary
import requests
from halo import Halo


def extract_changed_sections(original_text, updated_text):
    """Extracts sections that were modified based on diff."""
    diff = difflib.unified_diff(
        original_text.splitlines(), updated_text.splitlines(), lineterm=""
    )
    changed_sections = []
    current_section = []

    for line in diff:
        if line.startswith("+") and not line.startswith("+++"):
            current_section.append(line[1:])
        elif line.startswith("-") and not line.startswith("---"):
            if current_section:
                changed_sections.append("\n".join(current_section))
                current_section = []
        else:
            if current_section:
                changed_sections.append("\n".join(current_section))
                current_section = []

    return changed_sections


def display_diff_and_confirm(original_text, updated_text):
    """
    Display the diff between original and updated README content.
    Prompt the user for confirmation before proceeding.
    If the user rejects changes, allow selection of sections to regenerate.
    """

    def supports_ansi():
        return sys.platform != "win32" or os.getenv("TERM", "").startswith("xterm")

    use_ansi = supports_ansi()

    # Define ANSI color codes with fallback for unsupported terminals
    GREEN, RED, RESET = ("\033[32m", "\033[31m", "\033[0m") if use_ansi else ""

    diff = list(
        difflib.unified_diff(
            original_text.splitlines(),
            updated_text.splitlines(),
            lineterm="",
            fromfile="Original",
            tofile="Updated",
        )
    )

    if not diff:
        print(f"{GREEN}No changes detected in README.{RESET}")
        return True, []  # No changes to confirm

    print("\nProposed README Changes:\n")
    changed_sections = extract_changed_sections(original_text, updated_text)

    for line in diff:
        if line.startswith("+") and not line.startswith("+++"):  # Added lines
            print(f"{GREEN}{line}{RESET}")
        elif line.startswith("-") and not line.startswith("---"):  # Removed lines
            print(f"{RED}{line}{RESET}")
        else:
            print(line)  # Context lines (no color)

    print("\n")

    confirm_changes = questionary.confirm("Do you accept these changes?").ask()
    if confirm_changes:
        return True, []  # User accepted the changes

    # Prompt user to select sections they want to regenerate
    selected_rejections = questionary.checkbox(
        "Select the sections to regenerate:",
        choices=changed_sections + ["All"],
    ).ask()

    return False, selected_rejections


def generate_doc_content_with_ai(
    repo_name, graphql_mutation, user_context, repo_context, existing_readme=""
):
    """
    Generate README content using OpenAI API with RAG retrieval.
    """

    # API Endpoint for toast
    API_ENDPOINT = "https://toast/graphql"

    spinner = Halo("dots")

    # Send GraphQL mutation request to FastAPI backend
    spinner.start("Generating README content with AI...")

    response = requests.post(
        API_ENDPOINT,
        json={
            "query": graphql_mutation,
            "variables": {
                "repoName": repo_name,
                "repoContext": repo_context,
                "userContext": user_context,
                "existingReadme": existing_readme or None,
            },
        },
    )

    if response.status_code != 200:
        spinner.fail("Failed to generate README. API request failed.")
        return

    response_data = response.json()
    generated_content = (
        response_data.get("data", {}).get("generateReadme", {}).get("content", "")
    )

    if not generated_content:
        spinner.fail("No content was returned from the API.")
        return

    spinner.succeed("README content generated successfully.")
    return generated_content


def extract_docstrings_and_functions(lines):
    """
    Extracts docstrings, function/class signatures from Python code.
    """
    snippets = []
    inside_docstring = False
    docstring = []

    for line in lines:
        stripped = line.strip()

        # Capture function and class definitions
        if stripped.startswith(("def ", "class ")):
            snippets.append(stripped)

        # Capture multi-line docstrings
        if stripped.startswith(('"""', "'''")):
            if inside_docstring:
                docstring.append(stripped)
                snippets.append("\n".join(docstring))
                inside_docstring = False
                docstring = []
            else:
                inside_docstring = True
                docstring.append(stripped)
        elif inside_docstring:
            docstring.append(stripped)

    return snippets
