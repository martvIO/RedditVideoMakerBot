"""
Python dependencies installation module
"""

import sys
from pathlib import Path
from subprocess import run, CalledProcessError
from setup_utils.platform_utils import get_pip_command


def install_requirements():
    """Install Python packages from requirements.txt"""
    print("\n[2/5] Installing Python dependencies...")
    
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("WARNING: requirements.txt not found in current directory.")
        print("Please ensure you're running this script from the project root directory.")
        response = input("Continue without installing dependencies? (y/n): ").lower()
        if response != 'y':
            sys.exit(1)
        return
    
    try:
        pip_cmd = get_pip_command()
        
        print("  Upgrading pip...")
        run(
            pip_cmd + ['install', '--upgrade', 'pip'],
            check=True,
            capture_output=True
        )
        print("  ✓ pip upgraded")
        
        print("  Installing requirements...")
        run(
            pip_cmd + ['install', '-r', 'requirements.txt'],
            check=True
        )
        print("✓ Python dependencies installed successfully")
        
    except CalledProcessError as e:
        print(f"ERROR: Failed to install Python dependencies")
        print(f"Error details: {e}")
        print("\nTry running manually:")
        print(f"  {' '.join(get_pip_command())} install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Unexpected error during installation: {e}")
        sys.exit(1)
