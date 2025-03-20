from os import listdir, path


def verify_structure_templates_static(app, errors):
    """
    Id : 03
    Description : Verify that the `static/` and `templates/` folders contain only one subfolder named after the app.

    Tags :
    - architecture

    Args:
        app (str): The name of the Django app to check.
        errors (list): A list to store error messages if the structure is incorrect.
    """
    directories = ["templates", "static"]

    for dir_name in directories:
        dir_path = path.join(app, dir_name)

        if not path.exists(dir_path):
            continue

        list_dir = listdir(dir_path)

        if app not in list_dir:
            errors.append(
                f"\n🚨 Problème dans `{dir_name}` 🚨\n"
                f"Le dossier `{dir_name}` doit contenir un sous-dossier nommé `{app}`, mais il est absent.\n"
            )

        if len(list_dir) > 1:
            extra_contents = [item for item in list_dir if item != app]
            errors.append(
                f"\n🚨 Structure incorrecte dans `{dir_name}` 🚨\n"
                f"Le dossier `{dir_name}` ne doit contenir que `{app}`, mais d'autres éléments sont présents :\n\n"
                + "\n".join(f"📌 `{item}`" for item in extra_contents)
                + "\n"
            )
