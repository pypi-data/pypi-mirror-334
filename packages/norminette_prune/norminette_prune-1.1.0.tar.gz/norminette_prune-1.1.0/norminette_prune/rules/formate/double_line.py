from os import path
from subprocess import run


def double_line(app):
    """
    Id : 04
    Description : Remove double empty lines in HTML, JS, and CSS files.

    Tags :
    - format
    - files_content
    - web_files

    Args:
        app (str): The name of the Django app to check.
        errors (list): A list to store error messages if the structure is incorrect.
    """
    templates_dir = path.join(app, "templates", app)
    if path.exists(templates_dir):
        run(
            f"find {templates_dir} -type f \\( -name '*.html' -o -name '*.js' -o -name '*.css' \\) -exec sed -i '/^$/N;/^\\n$/D;' {{}} \\;",
            shell=True,
        )
