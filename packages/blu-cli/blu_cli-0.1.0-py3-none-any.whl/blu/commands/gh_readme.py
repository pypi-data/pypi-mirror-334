import os
import questionary
from halo import Halo
from blu.utils.graphql_loader import GraphQLLoader
from blu.utils.run_command import push_to_github
from blu.utils.directories import (
    locate_local_repo,
    save_readme,
    retrieve_repo_context,
)
from blu.utils.docs import (
    extract_changed_sections,
    display_diff_and_confirm,
    generate_doc_content_with_ai,
)


def gh_readme():
    """
    Create or update a README file for a GitHub repository.
    Uses OpenAI API with RAG to generate content dynamically.
    """

    spinner = Halo("dots")

    GENERATE_README_MUTATION = GraphQLLoader.load_graphql_mutation("generate_readme")

    # Prompt user for repository name
    repo_name = questionary.text("Enter the name of the repository:").ask()
    local_repo_path = locate_local_repo(repo_name=repo_name)

    if not local_repo_path:
        spinner.fail(f"Repository '{repo_name}' not found.")
        return

    # Confirm correct repo
    confirm_update = questionary.confirm(
        f"Repository found at '{local_repo_path}'. Do you want to update the README?"
    ).ask()

    if not confirm_update:
        spinner.info("Operation aborted.")
        return

    # Retrieve repository context (Advanced RAG)
    repo_context = retrieve_repo_context(local_repo_path)

    # Check if README exists
    readme_path = os.path.join(local_repo_path, "README.md")
    existing_readme = (
        open(readme_path, "r").read() if os.path.exists(readme_path) else ""
    )

    # Prompt for additional README context
    user_context = questionary.text(
        "Enter additional context for README generation:"
    ).ask()

    # Generate README using OpenAI API with RAG
    generated_content = generate_doc_content_with_ai(
        repo_name, GENERATE_README_MUTATION, user_context, repo_context, existing_readme
    )

    while True:
        # Show changes in a diff UI
        changes_accepted, rejected_sections = display_diff_and_confirm(
            existing_readme, generated_content
        )

        if changes_accepted:
            break  # Exit the loop if user is happy with changes

        if rejected_sections:
            # If "All" is selected, regenerate all the detected changes ONLY
            if "All" in rejected_sections:
                rejected_sections = extract_changed_sections(
                    existing_readme, generated_content
                )

            # Regenerate only the rejected sections of the README with repo context.
            spinner.info(f"Regenerating selected sections: {rejected_sections}")

            updated_readme = generated_content

            for section in rejected_sections:
                new_section = generate_doc_content_with_ai(
                    repo_name,
                    GENERATE_README_MUTATION,
                    section,
                    repo_context,
                    existing_readme,
                )
                updated_readme = updated_readme.replace(section, new_section)

            generated_content = updated_readme

    # Prompt user to save or push changes
    save_choice = questionary.select(
        "How would you like to proceed?",
        choices=["Save locally", "Save & push to GitHub", "Cancel"],
    ).ask()

    if save_choice == "Save locally":
        save_readme(generated_content, readme_path)
    elif save_choice == "Save & push to GitHub":
        save_readme(generated_content, readme_path)
        push_to_github(
            repo_name,
            local_repo_path,
            commit_message="Updated README via BLU CLI",
            add_path="README.md",
        )
    else:
        spinner.info("Operation aborted.")
