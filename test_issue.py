import os
import stat
import sys
import tkinter as tk
from pathlib import Path


LOG_PATH = os.getenv("PBS_TK_LOG")


def log(*parts: object) -> None:
    line = " ".join(str(part) for part in parts)
    print(line)
    if LOG_PATH:
        with Path(LOG_PATH).open("a", encoding="utf-8", errors="replace") as handle:
            handle.write(line + "\n")


def fd_info(fd: int) -> str:
    st = os.fstat(fd)
    mode = st.st_mode
    if stat.S_ISCHR(mode):
        kind = "chr"
    elif stat.S_ISREG(mode):
        kind = "reg"
    elif stat.S_ISFIFO(mode):
        kind = "fifo"
    elif stat.S_ISSOCK(mode):
        kind = "sock"
    else:
        kind = "other"
    return f"{kind} mode={oct(mode)}"


def dump_env() -> None:
    log("argv0", sys.argv[0])
    log("executable", sys.executable)
    log("isatty stdin", os.isatty(0))
    log("isatty stdout", os.isatty(1))
    log("isatty stderr", os.isatty(2))
    log("stdin", fd_info(0))
    log("stdout", fd_info(1))
    log("stderr", fd_info(2))
    log("prefix", sys.prefix)
    log("base_prefix", sys.base_prefix)
    log("TCL_LIBRARY", repr(os.getenv("TCL_LIBRARY")))


class TkWindow(tk.Tk):
    pass


def test_window():
    dump_env()
    app = TkWindow()
    log("tcl_library", app.tk.getvar("tcl_library"))
    app.destroy()


if __name__ == "__main__":
    test_window()
