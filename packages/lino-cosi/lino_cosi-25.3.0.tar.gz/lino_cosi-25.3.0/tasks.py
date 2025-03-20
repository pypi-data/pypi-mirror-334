from atelier.invlib import setup_from_tasks

ns = setup_from_tasks(
    globals(),
    "lino_cosi",
    doc_trees=[],
    languages="en de fr et nl".split(),
    # tolerate_sphinx_warnings=True,
    blogref_url="https://luc.lino-framework.org",
    locale_dir="lino_cosi/lib/cosi/locale",
    revision_control_system="git",
)
