import sys
from os import listdir

from django.conf import settings

from norminette_prune.rules.content_python_file.name_view_function import (
    name_view_function,
)
from norminette_prune.rules.files_emplacement.verify_pages_folder import (
    verify_pages_folder,
)
from norminette_prune.rules.files_emplacement.verify_structure_templates_static import (
    verify_structure_templates_static,
)
from norminette_prune.rules.formate.double_line import double_line
from norminette_prune.rules.formate.space_tag import space_tag
from norminette_prune.rules.templates.components_layout_emplacement import (
    component_layout_emplacement,
)
from norminette_prune.rules.templates.include_svg import include_svg
from norminette_prune.rules.templates.svg import svg


def run_checks():
    """Exécute toutes les vérifications sur les applications Django installées."""
    errors_by_app = {}

    try:
        for app in listdir():
            if app in settings.INSTALLED_APPS:
                errors = []
                svg(app, errors)
                include_svg(app, errors)
                name_view_function(app, errors)
                verify_pages_folder(app, errors)
                verify_structure_templates_static(app, errors)
                component_layout_emplacement(app, errors)

                double_line(app)
                space_tag(app)

                if errors:
                    errors_by_app[app] = errors

    except ValueError as e:
        print(f"Erreur lors de l'exécution des vérifications : {e}")
        sys.exit(1)

    return errors_by_app
