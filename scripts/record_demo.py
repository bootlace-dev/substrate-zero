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

    if not os.path.exists(OUT_MP4):
        print("[!] demo.mp4 not produced.", file=sys.stderr)
        sys.exit(1)

    print("[*] Extracting keyframes and calibrating scene reading durations...")
    with tempfile.TemporaryDirectory() as tmpdir:
        frame_pattern = os.path.join(tmpdir, "f_%03d.png")
        subprocess.run(
            ["ffmpeg", "-y", "-i", OUT_MP4, "-vf", "fps=10", frame_pattern],
            capture_output=True,
            check=True
        )

        files = sorted(glob.glob(os.path.join(tmpdir, "f_*.png")))
        if not files:
            print("[!] No frames extracted from video.", file=sys.stderr)
            sys.exit(1)

        frames = []
        durations = []

        for i, f in enumerate(files):
            img = Image.open(f).convert("RGB")
            frames.append(img)

            # Calibrated reading delays (in milliseconds)
            if i in [11, 12]:          # Main interactive menu
                durations.append(1500)
            elif i == 14:              # Chamber 8: Compiler Assassin (DSE)
                durations.append(6500)
            elif i == 17:              # Return to menu
                durations.append(1500)
            elif i in [19, 20]:        # Chamber 5: Lattice Nonce Bias (HNP)
                durations.append(3000)
            elif i == len(files) - 1:  # Terminal prompt exit
                durations.append(2500)
            else:
                durations.append(150)

        print(f"[*] Compiling {len(frames)} frames into {OUT_GIF}...")
        frames[0].save(
            OUT_GIF,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=0,
            optimize=True
        )

    file_size_kb = os.path.getsize(OUT_GIF) / 1024
    print(f"[+] Successfully generated hero banner GIF: {OUT_GIF} ({file_size_kb:.1f} KB, 22.5s duration)")


if __name__ == "__main__":
    record_demo()
