import logging
import os
import signal


LOG = logging.getLogger(__name__)
"""Logger instance."""

_TERMINATE_SIGNAL_HANDLERS = []
"""
SIGINT, SIGQUIT and SIGTERM handlers that was added by
add_terminate_signal_handler().
"""

_END_WORK_SIGNAL_RECEIVED = False
"""True, if the program received end work UNIX signal."""


def add_terminate_signal_handler(handler):
    """Sets a handler for SIGINT, SIGQUIT and SIGTERM signals."""

    _TERMINATE_SIGNAL_HANDLERS.append(handler)
    return handler


def remove_terminate_signal_handler(handler):
    """Removes handler added by add_terminate_signal_handler()."""

    _TERMINATE_SIGNAL_HANDLERS.remove(handler)


def end_work_signal_received():
    """Returns True if the program received end work UNIX signal."""

    return _END_WORK_SIGNAL_RECEIVED


def __signal_handler(signum, stack):
    """Handler for the UNIX signals."""

    LOG.info("Program received deadly UNIX signal [%s].", signum)

    global _END_WORK_SIGNAL_RECEIVED
    _END_WORK_SIGNAL_RECEIVED = True

    if _TERMINATE_SIGNAL_HANDLERS:
        for handler in _TERMINATE_SIGNAL_HANDLERS:
            try:
                LOG.info("Calling terminate UNIX signal handler %s...", handler)
                handler()
            except Exception as e:
                LOG.error("Error while calling a terminate signal handler: %s.", e)


def init(handle_unix_signals=True):
    """
    Starts the UNIX signals handling.
    When the program gets a signal the corresponding signal handlers is invoked.
    """

    if handle_unix_signals:
        signal.signal(signal.SIGINT, __signal_handler)
        signal.siginterrupt(signal.SIGINT, False)

        signal.signal(signal.SIGQUIT, __signal_handler)
        signal.siginterrupt(signal.SIGQUIT, False)

        signal.signal(signal.SIGTERM, __signal_handler)
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
