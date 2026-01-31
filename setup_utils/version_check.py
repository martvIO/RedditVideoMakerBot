"""
Python version checking module
"""

import sys


def check_python_version():
    """Verify Python version is 3.10 or 3.11"""
    print("\n[1/5] Checking Python version...")
    
    if sys.version_info.major != 3 or sys.version_info.minor not in [10, 11]:
        print(
            f"ERROR: This program only works on Python 3.10 or 3.11.\n"
            f"You are running Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}\n"
            f"Please install Python 3.10 or 3.11 and try again.\n"
        )
        print("Download Python from: https://www.python.org/downloads/")
        sys.exit(1)
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
