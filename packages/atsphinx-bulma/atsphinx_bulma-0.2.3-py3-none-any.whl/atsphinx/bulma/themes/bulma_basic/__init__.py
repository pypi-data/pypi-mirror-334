"""Entrypoint of theme."""

from pathlib import Path

from sphinx.application import Sphinx

from ... import __version__
from ...components.navbar import register_root_toctree_dict

here = Path(__file__).parent


def setup(app: Sphinx):  # noqa: D103
    app.add_html_theme("bulma-basic", str(here))
    app.connect("html-page-context", register_root_toctree_dict)
    app.setup_extension("atsphinx.bulma")
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
