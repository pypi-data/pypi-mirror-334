import os
import re
import subprocess


def find_norminette_path():
    try:
        chemin = subprocess.check_output(
            "find . -type d -name 'norminette_prune'", shell=True, text=True
        ).strip()
        return chemin if chemin else None
    except subprocess.CalledProcessError:
        return None


def extract_docstrings():
    """Extract rules documentation by extracting docstring"""
    directory = os.path.join(find_norminette_path(), "rules")
    pattern = re.compile(
        r'def\s+(\w+)\s*\(.*?\):\s+"""\s+Id\s*:\s*(\d+)\s+Description\s*:\s*(.*?)\s+Tags\s*:\s*(.*?)\s+Args\s*:(.*?)"""',
        re.DOTALL,
    )
    results = []
    try:
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            return results

        for rules_folder in os.listdir(directory):
            rules_path = os.path.join(directory, rules_folder)

            for root, _, files in os.walk(rules_path):
                for file in files:
                    if file.endswith(".py"):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, "r", encoding="utf-8") as f:
                                content = f.read()
                                matches = pattern.findall(content)
                                for match in matches:
                                    function_name, rule_id, description, tags, args = (
                                        match
                                    )
                                    description = " ".join(
                                        description.splitlines()
                                    ).strip()
                                    tags_list = " ".join(
                                        [
                                            t.strip()
                                            for t in tags.split("-")
                                            if t.strip()
                                        ]
                                    )

                                    results.append(
                                        (
                                            function_name,
                                            rule_id,
                                            description.strip(),
                                            tags_list,
                                        )
                                    )
                        except Exception as e:
                            print(f"Error processing file {filepath}: {e}")
    except Exception as e:
        print(f"Error scanning directory: {e}")
    return results


def get_tags_descriptions():
    """Returns a dictionary of tag descriptions."""
    return {
        "web_files": "HTML, JS, and CSS files.",
        "python_files": "Python files with `.py` extension.",
        "architecture": "Checks folder and file placement consistency.",
        "format": "Directly modifies file formatting.",
        "files_content": "Inspects file contents.",
    }


def get_sorted_rules():
    """Returns rules sorted by ID."""
    docstrings = extract_docstrings()
    docstrings.sort(key=lambda x: int(x[1]))
    return docstrings
