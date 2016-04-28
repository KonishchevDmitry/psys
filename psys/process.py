"""Various process-related functions."""

import logging
import os
import signal

log = logging.getLogger(__name__)

_TERMINATION_SIGNAL_HANDLERS = []
"""UNIX signal handlers that was added by add_terminate_signal_handler()."""

_TERMINATION_SIGNAL_RECEIVED = False
"""True if the program received a termination UNIX signal."""


def add_terminate_signal_handler(handler):
    """Adds a handler for SIGINT, SIGQUIT and SIGTERM signals."""

    _TERMINATION_SIGNAL_HANDLERS.append(handler)
    return handler


def remove_terminate_signal_handler(handler):
    """Removes a handler added by add_terminate_signal_handler()."""

    _TERMINATION_SIGNAL_HANDLERS.remove(handler)


def end_work_signal_received():
    """Returns True if the program received termination UNIX signal."""

    return _TERMINATION_SIGNAL_RECEIVED


def _signal_handler(signum, stack):
    """Handler for the UNIX signals."""

    log.info("Got a termination UNIX signal [%s].", signum)

    global _TERMINATION_SIGNAL_RECEIVED
    _TERMINATION_SIGNAL_RECEIVED = True

    if _TERMINATION_SIGNAL_HANDLERS:
        for handler in _TERMINATION_SIGNAL_HANDLERS:
            try:
                log.debug("Calling termination UNIX signal handler %s...", handler)
                handler()
            except Exception as e:
                log.error("Error while calling a termination signal handler: %s.", e)


def init(handle_unix_signals=True):
    """
    Starts the UNIX signals handling.
    When the program gets a signal the corresponding signal handlers are invoked.
    """

    if handle_unix_signals:
        signal.signal(signal.SIGINT, _signal_handler)
        signal.siginterrupt(signal.SIGINT, False)

        signal.signal(signal.SIGQUIT, _signal_handler)
        signal.siginterrupt(signal.SIGQUIT, False)

        signal.signal(signal.SIGTERM, _signal_handler)
        signal.siginterrupt(signal.SIGTERM, False)

        signal.siginterrupt(signal.SIGCHLD, False)
        signal.siginterrupt(signal.SIGPIPE, False)

    # Setting the proper PATH environment variable -->
    required_paths = "/sbin:/usr/sbin:/bin:/usr/bin"
    paths = os.getenv("PATH", required_paths).split(":")

    for path in required_paths.split(":"):
        if path not in paths:
            paths.append(path)

    os.environ.update(PATH=":".join(paths))
    # Setting the proper PATH environment variable <--
