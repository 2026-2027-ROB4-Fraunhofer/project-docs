project = "ROB4 Fraunhofer Mobile Manipulator Pick and Place"
author = "Yasmine Makkaoui"
copyright = "Fraunhofer IPA"

extensions = [
    "myst_parser",
    "sphinx_copybutton",
]
source_suffix = {".md": "markdown"}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_title = project

# html_theme = "furo"
# html_theme_options = {
#     "source_repository": "https://github.com/2026-2027-ROB4-Fraunhofer/project-docs/",
#     "source_branch": "main",
#     "source_directory": "docs/",
# }
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "version_selector": False,
    "collapse_navigation": False,
    "navigation_depth": 4,
}