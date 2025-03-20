from os import path
from subprocess import CalledProcessError, check_output


def verify_pages_folder(app, errors):
    """
    Id : 02

    Description : Verify if `page.html` files are inside the `pages/` folder and ensure files in `pages/`
    are named `page` (except in `components`, `sections`, and `layouts` folders).

    Tags:
        - web_files
        - architecture

    Args:
        app (str): The name of the Django app to check.
        errors (list): A list to store error messages if the structure is incorrect.
    """
    try:
        misplaced_pages = check_output(
            f"find {app} -name 'page.html' ! -path '*/pages/*'", text=True, shell=True
        ).split()

        if misplaced_pages:
            errors.append(
                "\n🚨 Fichiers 'page.html' mal placés 🚨\n"
                "Le fichier `page.html` doit être dans le dossier `/pages`.\n"
                "Les fichiers suivants ne respectent pas cette règle :\n\n"
                + "\n".join(f"📌 `{file}`" for file in misplaced_pages)
                + "\n"
            )

        templates_dir = path.join(app, "templates", app, "pages")
        if path.exists(templates_dir):
            wrong_files = check_output(
                f"find {templates_dir} -type f -name '*.html' ! -path '*/layout/*' ! -path '*/sections/*' ! -path '*/components/*' ! -name 'page.html'",
                shell=True,
                text=True,
            ).split()

            if wrong_files:
                errors.append(
                    "\n🚨 Fichiers incorrects dans '/pages' 🚨\n"
                    "Tous les fichiers dans `/pages` doivent commencer par `page.`, excepté ceux dans des dossiers `/components`, `/sections` ou `/layout`\n"
                    "Les fichiers suivants ne respectent pas cette convention :\n\n"
                    + "\n".join(f"📌 `{file}`" for file in wrong_files)
                    + "\n"
                )

    except CalledProcessError as e:
        if e.returncode == 1:
            pass
