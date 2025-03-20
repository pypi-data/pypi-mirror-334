import shlex
from os import path, sep
from re import compile
from subprocess import CalledProcessError, check_output


def component_layout_emplacement(app, errors):
    """
    Id : 06
    Description : Verify that layout, component, and section files are correctly placed based on their `include` references.

    Tags :
    - web_files
    - architecture

    Args:
        app (str): The name of the Django app to check.
        errors (list): A list to store error messages if the structure is incorrect.
    """
    component_layout_dict = {
        "components": {
            "pattern": r"{% include\s+[\'\"]([^\'\"]+components[^\'\"]+\.html)[\'\"]",
            "subfolder": "components",
            "entity_name": "composant",
        },
        "sections": {
            "pattern": r"{% include\s+[\'\"]([^\'\"]+sections[^\'\"]+\.html)[\'\"]",
            "subfolder": "sections",
            "entity_name": "composant",
        },
        "layout": {
            "pattern": r"{% extends\s+[\'\"]([^\'\"]+layout[^\'\"]+\.html)[\'\"]",
            "subfolder": "layout",
            "entity_name": "layout",
        },
    }

    for key, value in component_layout_dict.items():
        includes_extends_dict = get_includes_extends_paths(app, value["pattern"])

        for component_layout, file_paths in includes_extends_dict.items():
            if len(file_paths) == 1:
                continue

            file_component_layout = path.basename(component_layout)
            expected_path = determine_expected_path(
                app, file_paths, file_component_layout, value["subfolder"]
            )

            verify_file_location(
                app, file_component_layout, expected_path, value["subfolder"], errors
            )


def get_includes_extends_paths(app, pattern_str):
    """
    Récupère tous les chemins dans includes ou extends selon le pattern
    """
    includes_extends_dict = {}
    include_extend_pattern = compile(pattern_str)

    try:
        includes_extends = (
            check_output(
                f"find {app} -type f -name '*.html' ! -path '*svg/*' -exec grep -E {shlex.quote(pattern_str)} {{}} +",
                shell=True,
                text=True,
            )
            .strip()
            .splitlines()
        )

        for include_extend in includes_extends:
            if ":" in include_extend:
                file_path, include_extend_line = include_extend.split(":", 1)
                match = include_extend_pattern.search(include_extend_line)
                if match:
                    include_extend_path = match.group(1)
                    includes_extends_dict.setdefault(include_extend_path, set()).add(
                        file_path
                    )

    except CalledProcessError as e:
        if e.returncode == 1:
            pass
    return includes_extends_dict


def determine_expected_path(app, file_paths, file_name, subfolder):
    """
    Détermine le chemin attendu en fonction du type et de l'utilisation
    """
    directories = [path.dirname(file_path) for file_path in file_paths]

    dir_groups = {}
    for directory in directories:
        parent_dir = path.dirname(directory)
        dir_groups.setdefault(parent_dir, []).append(directory)

    if len(dir_groups) == 1:
        common_parent_dir = list(dir_groups.keys())[0]
    else:
        common_parent_dir = path.commonpath(directories)

    common_parent_dir = adjust_path_based_on_subfolder(
        common_parent_dir, subfolder, file_name
    )

    return path.join(common_parent_dir, subfolder, file_name)


def adjust_path_based_on_subfolder(common_parent_dir, subfolder, filename):
    """
    Ajuste le chemin en fonction du sous-dossier actuel selon les règles spécifiées
    """
    if subfolder == "layout" and filename == "base.html":
        common_parent_dir = common_parent_dir.replace(path.join(sep, "pages"), "")
    if "layout" in common_parent_dir.split(sep):
        common_parent_dir = common_parent_dir.replace(path.join(sep, "layout"), "")
    elif "components" in common_parent_dir.split(sep):
        common_parent_dir = common_parent_dir.replace(path.join(sep, "components"), "")
    elif "sections" in common_parent_dir.split(sep):
        common_parent_dir = common_parent_dir.replace(path.join(sep, "sections"), "")
    return common_parent_dir


def verify_file_location(app, file_name, expected_path, subfolder, errors):
    """
    Vérifie si le fichier est au bon emplacement et ajoute des erreurs si nécessaire
    """
    try:
        real_path = (
            check_output(
                f"find {app} -type f -name '{file_name}' ! -path '*svg/*'",
                shell=True,
                text=True,
            )
            .strip()
            .splitlines()
        )

        if not real_path:
            real_path = (
                check_output(
                    f"find . -type f -name '{file_name}' ! -path '*svg/*'",
                    shell=True,
                    text=True,
                )
                .strip()
                .splitlines()
            )

        if len(real_path) > 1:
            errors.append(
                f"\n🚨 Problème de fichiers en double 🚨\n"
                f"Le `{subfolder}` `{file_name}` ne peut pas être évalué correctement car plusieurs fichiers portent le même nom.\n"
                f"Voici la liste des fichiers trouvés :\n"
                + "\n".join([f"- {p}" for p in real_path])
            )
        elif real_path and real_path[0] != expected_path:
            errors.append(
                f"\n🚨 Fichier mal placé 🚨\n"
                f"Le `{subfolder}` `{file_name}` est dans le mauvais dossier.\n"
                f"- Chemin attendu : `{expected_path}`\n"
                f"- Chemin réel : `{real_path[0]}`"
            )

    except CalledProcessError:
        errors.append(
            f"\n❌ Fichier non trouvé ❌\n"
            f"Le `{subfolder}` `{file_name}` est introuvable dans `{expected_path}`."
        )
