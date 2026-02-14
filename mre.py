import _tkinter
import os


tmpfile = open(os.devnull, encoding="utf-8")
os.dup2(tmpfile.fileno(), 0)
_tkinter.create()
print("ok")
