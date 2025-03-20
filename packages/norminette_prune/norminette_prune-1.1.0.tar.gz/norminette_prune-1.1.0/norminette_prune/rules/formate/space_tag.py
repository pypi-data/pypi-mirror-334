import re
import subprocess
from os import path


def space_tag(app):
    """
    Id : 05
    Description : Normalize spaces in Django tags (with exactly one space between the tag and its content).

    Tags :
    - format
    - web_files
    - files_content

    Args:
        app (str): The name of the Django app to check.
        errors (list): A list to store error messages if the structure is incorrect.
    """
    templates_dir = path.join(app, "templates", app)
    if not path.exists(templates_dir):
        return

    def normalize_spaces(content):
        def normalize_single_tag(match):
            full_tag = match.group(0)

            if full_tag.startswith("{{"):
                inner_content = full_tag[2:-2].strip()
                formatted_tag = "{{ " + inner_content + " }}"
                return formatted_tag
            elif full_tag.startswith("{%"):
                inner_content = full_tag[2:-2].strip()
                formatted_tag = "{% " + inner_content + " %}"
                return formatted_tag
            else:
                return full_tag

        pattern = r"\{\{[^}]*\}\}|\{%[^%]*%\}"
        return re.sub(pattern, normalize_single_tag, content)

    find_process = subprocess.run(
        f"find {templates_dir} -name '*.html' -not -path '*/.*' -type f",
        capture_output=True,
        text=True,
        shell=True,
    )

    for template_file in find_process.stdout.splitlines():
        with open(template_file, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = normalize_spaces(content)

        if new_content != content:
            with open(template_file, "w", encoding="utf-8") as f:
                f.write(new_content)
