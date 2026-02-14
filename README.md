# [astral-sh/python-build-standalone#939](https://github.com/astral-sh/python-build-standalone/issues/939) MRE

This repository validates the fix in
[astral-sh/python-build-standalone#958](https://github.com/astral-sh/python-build-standalone/pull/958)
for macOS `init.tcl` failures in tkinter.

The reproducer in `mre.py` uses a minimal script:
- force `stdin` to `/dev/null` (non-TTY character device)
- call `_tkinter.create()`

## CI

Workflow: `.github/workflows/repro.yml`

The CI matrix runs on macOS (`macos-14`) for Python `3.10` through `3.14`, and
builds PBS from two refs:

- [`astral-sh/python-build-standalone@main`](https://github.com/astral-sh/python-build-standalone/tree/main)
  expected MRE result: fail
- [`shaanmajid/python-build-standalone@fix/tkinter-tcl-library-env`](https://github.com/shaanmajid/python-build-standalone/tree/fix/tkinter-tcl-library-env)
  expected MRE result: pass

Each job:
1. builds PBS from source
2. creates a venv from the built Python
3. verifies trigger conditions (`sys.prefix != sys.base_prefix` and non-TTY character-device `stdin`)
4. runs `mre.py` and asserts expected fail/pass behavior
