import shutil
import os
import subprocess
import ctypes
import sys
import io
import tempfile
from contextlib import contextmanager
from ctypes import CDLL

libc = ctypes.CDLL(None)
c_stdout = ctypes.c_void_p.in_dll(libc, 'stdout')

@contextmanager
def stdout_redirector(stream):
    # The original fd stdout points to. Usually 1 on POSIX systems.
    original_stdout_fd = sys.stdout.fileno()

    def _redirect_stdout(to_fd):
        """Redirect stdout to the given file descriptor."""
        # Flush the C-level buffer stdout
        libc.fflush(c_stdout)
        # Flush and close sys.stdout - also closes the file descriptor (fd)
        sys.stdout.close()
        # Make original_stdout_fd point to the same file as to_fd
        os.dup2(to_fd, original_stdout_fd)
        # Create a new sys.stdout that points to the redirected fd
        sys.stdout = io.TextIOWrapper(os.fdopen(original_stdout_fd, 'wb'))

    # Save a copy of the original stdout fd in saved_stdout_fd
    saved_stdout_fd = os.dup(original_stdout_fd)
    try:
        # Create a temporary file and redirect stdout to it
        tfile = tempfile.TemporaryFile(mode='w+b')
        _redirect_stdout(tfile.fileno())
        # Yield to caller, then redirect stdout back to the saved fd
        yield
        _redirect_stdout(saved_stdout_fd)
        # Copy contents of temporary file to the given stream
        tfile.flush()
        tfile.seek(0, io.SEEK_SET)
        stream.write(tfile.read())
    finally:
        tfile.close()
        os.close(saved_stdout_fd)

def compile(file_to_test):
    # copy file to currend directory (don't want to work on oryginal)
    shutil.copyfile(f"../src/{file_to_test}.c", f"{file_to_test}.c")
    print(f"file copied to {file_to_test}.c")
    # compile it as shaded (.so) file
    subprocess.run(["gcc", "-fPIC", "-shared", "-o",
                    f"{file_to_test}.so", f"{file_to_test}.c"])
    print(f"file compiled as {file_to_test}.so")

def clean_file(file_to_test):
    # clean everything
    os.remove(f"{file_to_test}.c")
    print(f"{file_to_test}.c removed")
    os.remove(f"{file_to_test}.so")
    print(f"{file_to_test}.so removed")

