#!/usr/bin/env python3
import platform
import subprocess
import sys

# https://stackoverflow.com/a/58026969/5494277
in_venv = getattr(sys, "real_prefix", getattr(sys, "base_prefix", sys.prefix)) != sys.prefix
pip_call = [sys.executable, "-m", "pip"]
try:
    subprocess.check_call([*pip_call, "--version"])
except subprocess.CalledProcessError as ex:
    raise RuntimeError("Issues with \"pip\" package detected! Follow the official instructions to install - https://pip.pypa.io/en/stable/installation/")
pip_install = pip_call + ["install"]

is_pi = platform.machine().startswith("arm") or platform.machine().startswith("aarch")
if sys.version_info[0] != 3:
    raise RuntimeError("Demo script requires Python 3 to run (detected : Python %d)" % sys.version_info[0])
if is_pi and sys.version_info[1] in (7, 9):
    print("[WARNING] There are no prebuilt wheels for Python 3.{} for OpenCV, building process on this device may be long and unstable".format(sys.version_info[1]))

if not in_venv:
    pip_install.append("--user")

subprocess.check_call([*pip_install, "pip", "-U"])
# temporary workaroud for issue between main and develop
subprocess.check_call([*pip_call, "uninstall", "depthai", "--yes"])
subprocess.check_call([*pip_install, "-r", "requirements.txt"])

try:
    subprocess.check_call([*pip_install, "-r", "requirements-optional.txt"], stderr=subprocess.DEVNULL)
except subprocess.CalledProcessError as ex:
    print(f"Optional dependencies were not installed. This is not an error.")
