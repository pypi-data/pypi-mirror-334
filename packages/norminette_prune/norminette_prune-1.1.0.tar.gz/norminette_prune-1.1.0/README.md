# Prune's Norminette

## What is it for?

The norminette automatically checks the organization of files in a Django project as well as code rules.
This allows for the same code standard between projects and makes it easier to navigate.

## Prerequisites

- To be installed on a Prune Django project that uses poetry or UV

## UV project

### Installation

Run the following command in the console:

```bash
uv add norminette_prune
```

### Running the norminette

To run the package, simply enter in the console:
```bash
norminette_prune
```

### Display rules in the project

To list all the rule checks in the project, run the following command:
```bash
norminette_display_rules
```

### Updating the norminette
Don't hesitate to regularly run `uv sync --upgrade`, as the norminette evolves with time and our practices!

## Poetry project

### Installation

Run the following command:

```bash
poetry add norminette_prune
```

### Running the norminette
```bash
poetry run norminette_prune
```

### Display rules in the project

To list all the rule checks in the project, run the following command:
```bash
poetry run norminette_display_rules
```

### Updating the norminette
Don't hesitate to regularly run `poetry update`, as the norminette evolves with time and our practices!

## For developers: add new rule

The rules are located in the `rules/` folder.

To add a new rule based on a function's docstring, follow this format:
```python
"""
    Id: 10
    Description: Describe what the rule checks.

    Tags:
        - Use relevant tags from the list below.

    Args:
        app (str): The name of the Django app to check.
        errors (list): A list to store error messages if the structure is incorrect.
"""
```

### Available Tags
The currently available tags are:

- **web_files**: HTML, JS, and CSS files.
- **python_files**: Python files with `.py` extension.
- **architecture**: Checks folder and file placement consistency.
- **format**: Directly modifies file formatting.
- **files_content**: Inspects file contents.

### Integration Steps
- Import the new function in `utils/run_checks.py`. (Remember to add errors in args)
- Sync the new rules to update `README.md` and `README-FR.md`.

To sync rules after adding them to the project, run:
```bash
python -m norminette_prune.utils.rules.generate_readme
```

For adding a tag, add it to the `get_tags_descriptions()` function in `utils/rules/extract_rules.py` file.

## Project architecture at Prune

To access the documentation, please go to the link where you can find documentation in English and French.

[Documentation](https://gitlab.com/bastien_arnout/prune-doc.git)

If you want to download it directly, here is the link:

[Download](https://gitlab.com/bastien_arnout/prune-doc/-/archive/main/prune-doc-main.zip)

# Available Versions

| Version | Date       | Notes                      |
|---------|-----------|---------------------------|
| 0.1.0   | 2025-03-13 | Initial release  |
| 0.1.1   | 2025-03-14 | Fixed import bug and added rules      |
| 1.0.0   | 2025-03-14 | Added rules to readme            |
| 1.1.0   | 2025-03-17 | added command to display rules on terminal            |
## Rules

| Id  | Name | Description | Tags |
|:---:|-----|-------------|------|
| 01 | name_view_function | Verify that the name of rendering functions for views ends with '_view'. | python_files files_content |
| 02 | verify_pages_folder | Verify if `page.html` files are inside the `pages/` folder and ensure files in `pages/`     are named `page` (except in `components`, `sections`, and `layouts` folders). | web_files architecture |
| 03 | verify_structure_templates_static | Verify that the `static/` and `templates/` folders contain only one subfolder named after the app. | architecture |
| 04 | double_line | Remove double empty lines in HTML, JS, and CSS files. | format files_content web_files |
| 05 | space_tag | Normalize spaces in Django tags (with exactly one space between the tag and its content). | format web_files files_content |
| 06 | component_layout_emplacement | Verify that layout, component, and section files are correctly placed based on their `include` references. | web_files architecture |
| 07 | include_svg | Ensure that SVG includes use absolute paths. | web_files files_content |
| 08 | svg | Verify that SVG files are inside the `svg/` folder and use the `.html` extension. | web_files architecture |


### Tags  
- **web_files** : HTML, JS, and CSS files.
- **python_files** : Python files with `.py` extension.
- **architecture** : Checks folder and file placement consistency.
- **format** : Directly modifies file formatting.
- **files_content** : Inspects file contents.
