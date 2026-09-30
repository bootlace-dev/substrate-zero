#!/usr/bin/env python3
"""
Automated Hero Banner GIF Generator for Substrate Zero.
Executes VHS tape recording and compiles calibrated animated GIF with
proper reading pauses for terminal demonstration.
"""

import os
import sys
import glob
import shutil
import tempfile
import subprocess
from PIL import Image

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TAPE_FILE = os.path.join(REPO_ROOT, "scripts", "demo.tape")
ASSETS_DIR = os.path.join(REPO_ROOT, "assets")
OUT_GIF = os.path.join(ASSETS_DIR, "demo.gif")
OUT_MP4 = os.path.join(ASSETS_DIR, "demo.mp4")


def record_demo():
    print("[*] Recording terminal screencast via VHS...")
    vhs_bin = shutil.which("vhs") or "/home/bootlace/bin/vhs"
    if not os.path.exists(vhs_bin):
        print(f"[!] VHS binary not found at {vhs_bin}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(ASSETS_DIR, exist_ok=True)
    res = subprocess.run([vhs_bin, TAPE_FILE], cwd=REPO_ROOT)
    if res.returncode != 0:
        print("[!] VHS recording failed.", file=sys.stderr)
        sys.exit(res.returncode)

    if not os.path.exists(OUT_MP4) or not os.path.exists(OUT_GIF):
        print("[!] Demo asset recording failed.", file=sys.stderr)
        sys.exit(1)

    mp4_kb = os.path.getsize(OUT_MP4) / 1024
    gif_kb = os.path.getsize(OUT_GIF) / 1024
    print(f"[+] Successfully generated hero banner screencasts:")
    print(f"    - MP4: {OUT_MP4} ({mp4_kb:.1f} KB)")
    print(f"    - GIF: {OUT_GIF} ({gif_kb:.1f} KB)")


if __name__ == "__main__":
    record_demo()
