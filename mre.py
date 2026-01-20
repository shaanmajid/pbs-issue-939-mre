import os
import stat
import sys
import tkinter as tk


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


print("argv0", sys.argv[0])
print("executable", sys.executable)
print("isatty stdin", os.isatty(0))
print("isatty stdout", os.isatty(1))
print("isatty stderr", os.isatty(2))
print("stdin", fd_info(0))
print("stdout", fd_info(1))
print("stderr", fd_info(2))
print("prefix", sys.prefix)
print("base_prefix", sys.base_prefix)
print("TCL_LIBRARY", repr(os.getenv("TCL_LIBRARY")))

app = tk.Tk()
print("tcl_library", app.tk.getvar("tcl_library"))
app.destroy()
print("Tk ok")
