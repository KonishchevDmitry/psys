"""Provides a wrapper around a UNIX pipe."""

import fcntl
import logging
import os

from psys import eintr_retry

log = logging.getLogger(__name__)


class Pipe(object):
    """Represents a UNIX pipe."""

    read = None
    """Read FD."""

    write = None
    """Write FD."""

    def __init__(self, nonblock=False):
        self.read, self.write = os.pipe()

        try:
            if nonblock:
                for fd in self.read, self.write:
                    flags = eintr_retry(fcntl.fcntl)(fd, fcntl.F_GETFL)
                    eintr_retry(fcntl.fcntl)(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        except:
            self.close()
            raise

    def __del__(self):
        self.close()

    def close(self, read=True, write=True):
        """Closes the pipe."""

        if read and self.read is not None:
            try:
                eintr_retry(os.close)(self.read)
            except Exception as e:
                log.error("Unable to close a pipe: %s.", e)
            else:
                self.read = None

        if write and self.write is not None:
            try:
                eintr_retry(os.close)(self.write)
            except Exception as e:
                log.error("Unable to close a pipe: %s.", e)
            else:
                self.write = None
