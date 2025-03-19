"""Additional for navbar."""

from typing import Any, Optional

from docutils import nodes
from sphinx.addnodes import toctree
from sphinx.application import Sphinx


def register_root_toctree_dict(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict[str, Any],
    doctree: Optional[nodes.document],
) -> None:
    """Pass toctree of root for navbar."""

    def root_toctree_dict(show_hidden: bool = False):
        doctree = app.env.get_doctree(app.config.root_doc)
        subs = []
        for tree in doctree.findall(toctree):
            if tree["hidden"] and not show_hidden:
                continue
            for title, page in tree["entries"]:
                subs.append(
                    {
                        "uri": app.builder.get_relative_uri(pagename, page),
                        "title": title
                        or next(
                            app.env.get_doctree(page).findall(nodes.title)
                        ).astext(),
                    }
                )
        return subs

    context["root_toctree_dict"] = root_toctree_dict
    return
