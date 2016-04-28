"""Various daemon-related functions."""

import errno
import fcntl
import os
import signal
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


def write_pidfile(fd):
    """Write pid to pidfile previously allocated by acquire_pidfile()"""

    data = str(os.getpid())
    datalen = len(data)

    while data:
        size = eintr_retry(os.write)(fd, data)
        data = data[size:]

    eintr_retry(os.ftruncate)(fd, datalen)


def daemonize(do_fork=True, skip_fds=[]):
    """Daemonizes current process."""

    if do_fork:
        if os.fork():
            os._exit(0)
        else:
            os.setsid()

            if os.fork():
                os._exit(0)

    os.chdir("/")
    os.umask(0)

    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    signal.siginterrupt(signal.SIGHUP, False)

    # Redirecting standard streams to /dev/null and closing original descriptors
    null_dev = eintr_retry(os.open)("/dev/null", os.O_RDWR)
    try:
        for fd in (sys.stdin.fileno(), sys.stdout.fileno(), sys.stderr.fileno()):
            if fd not in skip_fds:
                os.dup2(null_dev, fd)
    finally:
        eintr_retry(os.close)(null_dev)
