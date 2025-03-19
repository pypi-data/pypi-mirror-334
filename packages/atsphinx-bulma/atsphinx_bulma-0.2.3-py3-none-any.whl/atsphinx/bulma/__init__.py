"""Bluma using suite for Sphinx.."""

from sphinx.application import Sphinx

from .components.messages import DEFAULT_MESSAGE_CLASSES, MessageClassMap
from .translator import BulmaTranslator

__version__ = "0.2.3"


def setup(app: Sphinx):  # noqa: D103
    app.add_config_value(
        "bulma_message_classes",
        DEFAULT_MESSAGE_CLASSES,
        "env",
        MessageClassMap,
    )
    app.add_config_value("bulma_message_fallback", "", "env", str)
    app.set_translator("html", BulmaTranslator)
    app.set_translator("dirhtml", BulmaTranslator)
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
