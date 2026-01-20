# [astral-sh/python-build-standalone#939](https://github.com/astral-sh/python-build-standalone/issues/939) MRE

Minimal repro for python-build-standalone (PBS) Tcl/Tk `init.tcl` failures on
macOS. 

Direct run (no pytest) fails when:
- `sys.prefix != sys.base_prefix` and
- `stdin` is a non‑TTY character device (e.g. `/dev/null`, `/dev/zero`)

Pytest behavior:
- Default capture sets `stdin` to a non‑TTY char device → fail.
- With `-s`, it behaves like direct runs (pipe passes, non‑TTY char device fails).

Observed on macOS with PBS Python 3.12.x (Tcl 8.6), 3.13.x (Tcl 8.6),
and 3.14.2 (Tcl 9.0), so it is not version‑specific.

## Files

- `mre.py`: direct repro.
- `test_issue.py`: pytest repro with env logging via `PBS_TK_LOG`.

## Local run (copy/paste)

```bash
export UV_MANAGED_PYTHON=1
uv python install 3.14.2
```

### Direct MRE (no pytest)

```bash
# FAIL: venv-like prefix + stdin=/dev/null
uvx --python=3.14.2 python mre.py < /dev/null

# FAIL: venv-like prefix + stdin=/dev/zero
uvx --python=3.14.2 python mre.py < /dev/zero

# PASS: venv-like prefix + stdin is a pipe
printf '' | uvx --python=3.14.2 python mre.py

# PASS: venv-like prefix + stdin is a regular file
tmpfile=$(mktemp); uvx --python=3.14.2 python mre.py < "$tmpfile"; rm -f "$tmpfile"

# PASS: no venv-like prefix (base_prefix python)
~/.local/share/uv/python/cpython-3.14.2-macos-aarch64-none/bin/python mre.py < /dev/null
```

### Pytest (same code, different behavior)

```bash
# FAIL: pytest capture + stdin=/dev/null
uvx --python=3.14.2 --with-requirements requirements.txt python -m pytest -q test_issue.py < /dev/null

# FAIL: pytest capture + stdin is a pipe (pytest forces stdin to /dev/null)
printf '' | uvx --python=3.14.2 --with-requirements requirements.txt python -m pytest -q test_issue.py

# PASS: pytest -s (no capture) + stdin is FIFO
printf '' | uvx --python=3.14.2 --with-requirements requirements.txt python -m pytest -q -s test_issue.py

# FAIL: pytest -s + stdin=/dev/null
uvx --python=3.14.2 --with-requirements requirements.txt python -m pytest -q -s test_issue.py < /dev/null
```

## CI

One job per case on macOS, plus small Linux and Windows probes.
Linux and Windows pass under the same stdin conditions (so far).
Expected‑fail cases fail the job, so the workflow is intentionally red.
