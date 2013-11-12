"""Various daemon-related functions."""

import errno
import fcntl
import os
import stat
import sys

from psys import Error
from psys import eintr_retry


class PidFileLockError(Error):
    """Raised on failed attempt to lock a PID file."""

    def __init__(self, path, *args):
        super(PidFileLockError, self).__init__(*args)
        self.path = path


class PidFileLockedError(PidFileLockError):
    """Raised when we attempt to lock an already locked PID file."""

    def __init__(self, path):
        super(PidFileLockedError, self).__init__(path,
            "PID file '{0}' is already locked by another process.", path)


def acquire_pidfile(path):
    """Creates and locks a PID file."""

    fd = -1

    try:
        fd = eintr_retry(os.open)(path, os.O_RDWR | os.O_CREAT, 0o600)

        if fd <= sys.stderr.fileno():
            eintr_retry(os.dup2)(fd, sys.stderr.fileno() + 1)
            eintr_retry(os.close)(fd)
            fd = sys.stderr.fileno() + 1

        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except EnvironmentError as e:
            if e.errno == errno.EWOULDBLOCK:
                raise PidFileLockedError(path)
            else:
                raise e

        fd_stat = os.fstat(fd)

        try:
            file_stat = os.stat(path)
        except EnvironmentError as e:
            if e.errno == errno.ENOENT:
                raise PidFileLockedError(path)
            else:
                raise e

        if(
            ( fd_stat[stat.ST_DEV],   fd_stat[stat.ST_INO]   ) !=
            ( file_stat[stat.ST_DEV], file_stat[stat.ST_INO] )
        ):
            raise PidFileLockedError(path)

        return fd
    except Exception as e:
        if fd != -1:
            eintr_retry(os.close)(fd)

        if isinstance(e, PidFileLockedError):
            raise e

        raise PidFileLockError(path,
            "Failed to lock PID file '{0}': {1}.", path, e)


def release_pidfile(path, fd):
    """Releases a locked PID file."""

    try:
        eintr_retry(os.unlink)(path)
    finally:
        eintr_retry(os.close)(fd)
