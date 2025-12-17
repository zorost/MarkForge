#!/usr/bin/env python3
"""
MarkForge - macOS Build Script
Builds the desktop application for macOS using PyInstaller.
"""

import subprocess
import sys
import os
from pathlib import Path

# Ensure we're in the right directory
os.chdir(Path(__file__).parent)

def build():
    """Build MarkForge for macOS."""
    print("=" * 60)
    print("Building MarkForge for macOS...")
    print("=" * 60)
    
    # Clean previous builds
    subprocess.run(["rm", "-rf", "build", "dist"], check=False)
    
    # Run PyInstaller
    result = subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        "MarkForge.spec"
    ])
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✅ Build successful!")
        print("App location: dist/MarkForge.app")
        print("=" * 60)
        
        # Copy to Applications
        print("\nInstalling to /Applications...")
        subprocess.run(["rm", "-rf", "/Applications/MarkForge.app"], check=False)
        subprocess.run(["cp", "-R", "dist/MarkForge.app", "/Applications/"])
        print("✅ MarkForge installed to /Applications/")
        
        # Open the app
        subprocess.run(["open", "/Applications/MarkForge.app"])
    else:
        print("\n❌ Build failed!")
        sys.exit(1)


if __name__ == '__main__':
    build()
