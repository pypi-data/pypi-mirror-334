from __future__ import absolute_import
import os
import sys
from typing import Any, Tuple
import wrapt

if "TF_BUILD" in os.environ:
    WARNING_MESSAGE_FMT = "##vso[task.logissue type=warning]%(message)s"
    ERROR_MESSAGE_FMT = "##vso[task.logissue type=error]%(message)s"
elif "GITHUB_ACTIONS" in os.environ:
    WARNING_MESSAGE_FMT = "::warning::%(message)s"
    ERROR_MESSAGE_FMT = "::error::%(message)s"
else:
    WARNING_MESSAGE_FMT = os.environ.get("LOGGING_PIPELINE_WARNING_MESSAGE_FORMAT")
    ERROR_MESSAGE_FMT = os.environ.get("LOGGING_PIPELINE_ERROR_MESSAGE_FORMAT")

default_handler = None
warning_handler = None
error_handler = None


@wrapt.when_imported("logging")
def apply_patches(logging):
    """Apply the patching on module import"""
    pipeline_handler(logging)


def pipeline_handler(logging):
    """Inject the pipeline handlers."""
    if WARNING_MESSAGE_FMT is None and ERROR_MESSAGE_FMT is None:
        return

    def get_handler_for_levels(levelno: Tuple[int, ...], fmt: str) -> Any:
        """Get the handler for given levels with the prefix"""
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(fmt))
        handler.addFilter(lambda record: record.levelno in levelno)
        return handler

    global default_handler
    global warning_handler
    global error_handler
    if default_handler is None:
        default_handler = logging.StreamHandler()
        default_handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
    if warning_handler is None and WARNING_MESSAGE_FMT is not None:
        warning_handler = get_handler_for_levels(
            (logging.WARNING,), WARNING_MESSAGE_FMT
        )
    if error_handler is None and ERROR_MESSAGE_FMT is not None:
        error_handler = get_handler_for_levels(
            (logging.ERROR, logging.CRITICAL), ERROR_MESSAGE_FMT
        )

    def remove_logging_handlers():
        logging.getLogger().removeHandler(default_handler)
        if warning_handler is not None:
            logging.getLogger().removeHandler(warning_handler)
        if error_handler is not None:
            logging.getLogger().removeHandler(error_handler)

    def add_logging_handlers():
        if warning_handler is not None:
            logging.getLogger().addHandler(warning_handler)
        if error_handler is not None:
            logging.getLogger().addHandler(error_handler)

    # The default handler only needs to be applied here and not with basicConfig
    logging.getLogger().addHandler(default_handler)
    add_logging_handlers()

    def basic_config(wrapped, _instance, args, kwargs):
        """Patch the basicConfig function."""
        remove_logging_handlers()
        wrapped(*args, **kwargs)
        add_logging_handlers()

    wrapt.wrap_function_wrapper(logging, "basicConfig", basic_config)
