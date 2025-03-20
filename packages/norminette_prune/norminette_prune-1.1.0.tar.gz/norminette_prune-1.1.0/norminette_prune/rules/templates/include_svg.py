from subprocess import CalledProcessError, check_output


def include_svg(app, errors):
    """
    Id : 07
    Description : Ensure that SVG includes use absolute paths.

    Tags :
    - web_files
    - files_content

    Args:
        app (str): The name of the Django app to check.
        errors (list): A list to store error messages if the structure is incorrect.
    """
    try:
        svg_incorrects = (
            check_output(
                rf"grep -rEHn '{{% include [\"''](../|./).*\/svg\/.*\.html[\"'']' {app}",
                text=True,
                shell=True,
            )
            .strip()
            .split("\n")
        )

        svg_incorrects = [line for line in svg_incorrects if line]

        if svg_incorrects:
            errors.append(
                "\n🚨 Problèmes d'inclusion des fichiers SVG 🚨\n"
                "Les fichiers SVG doivent être inclus avec un **chemin absolu**, pas relatif (`../` ou `./`).\n"
                "Les inclusions incorrectes sont détectées dans les fichiers suivants :\n\n"
                + "\n".join([f"- `{line}`" for line in svg_incorrects])
            )

    except CalledProcessError as e:
        if e.returncode == 1:
            pass
