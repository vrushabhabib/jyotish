#!/bin/bash
# pyswisseph fails to build with the system setuptools on this image ("install_layout" error).
# Building the wheel inside a clean virtual environment works; the wheel is then installed system-wide.
set -e
D=${TMPDIR:-/tmp}/swe_build
python3 -m venv "$D/venv" >/dev/null
"$D/venv/bin/pip" install -q setuptools wheel
"$D/venv/bin/pip" wheel -q pyswisseph -w "$D/whl"
pip install -q "$D"/whl/pyswisseph-*.whl --break-system-packages
python3 -c "import swisseph as s; print('Swiss Ephemeris', s.version)"
