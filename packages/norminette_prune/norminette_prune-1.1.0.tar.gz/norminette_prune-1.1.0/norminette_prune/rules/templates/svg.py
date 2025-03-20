from os import path
from subprocess import CalledProcessError, check_output


def svg(app, errors):
    """
    Id : 08
    Description : Verify that SVG files are inside the `svg/` folder and use the `.html` extension.

    Tags :
    - web_files
    - architecture

    Args:
        app (str): The name of the Django app to check.
        errors (list): A list to store error messages if the structure is incorrect.
    """
    try:
        svg_files = (
            check_output(
                f"grep -rl '</svg>' --include='*.html' --include='*.svg' {app} --exclude-dir='.venv' --exclude-dir='whitenoise-root'",
                text=True,
                shell=True,
            )
            .strip()
            .split("\n")
        )

        wrong_folder_files = []
        wrong_extension_files = []

        for file_path in svg_files:
            if "static_assets/" in file_path or "static/" in file_path:
                continue
            parent_dir = path.basename(path.dirname(file_path))
            file = path.basename(file_path)
            if not parent_dir:
                continue
            if parent_dir != "svg":
                wrong_folder_files.append(file_path)
            file_name, extension = path.splitext(file)
            if extension == ".svg":
                wrong_extension_files.append(file_path)

        if wrong_folder_files:
            errors.append(
                "\n🚨 Fichiers SVG mal placés 🚨\n"
                "Les fichiers contenant des `<svg>` doivent être dans un dossier svg.\n"
                "Les fichiers suivants sont mal placés :\n"
                + "\n".join([f"- `{file}`" for file in wrong_folder_files])
            )

        if wrong_extension_files:
            errors.append(
                "\n🚨 Fichiers SVG mal nommés 🚨\n"
                "Les fichiers contenant des balises `<svg>` doivent être en `.html`, pas en `.svg`.\n"
                "Les fichiers suivants ont la mauvaise extension :\n"
                + "\n".join([f"- `{file}`" for file in wrong_extension_files])
            )
    except CalledProcessError as e:
        if e.returncode == 1:
            pass
