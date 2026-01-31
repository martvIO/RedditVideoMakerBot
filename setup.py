#!/usr/bin/env python
"""
Setup script for Reddit Video Maker Bot
This script installs all required dependencies and performs necessary setup checks
before running the main application.
Works on Windows, macOS, and Linux.
"""

import sys
import os
from pathlib import Path

# Add the script directory to Python path to find setup_utils
script_dir = Path(__file__).parent.absolute()
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

from setup_utils.version_check import check_python_version
from setup_utils.dependencies import install_requirements
from setup_utils.ffmpeg_setup import install_ffmpeg
from setup_utils.config_setup import setup_config, validate_config
from setup_utils.platform_utils import get_platform_info


def main():
    """Run all setup steps"""
    system_info = get_platform_info()
    
    print("=" * 70)
    print("Reddit Video Maker Bot - Setup Script")
    print("=" * 70)
    print(f"Platform: {system_info['os']} ({system_info['architecture']})")
    print(f"Python: {system_info['python_version']}")
    print("=" * 70)
    
    # Step 1: Check Python version
    check_python_version()
    
    # Step 2: Install Python dependencies
    install_requirements()
    
    # Step 3: Install/check FFmpeg
    install_ffmpeg()
    
    # Step 4: Set up configuration
    config = setup_config()
    
    # Step 5: Validate configuration
    validate_config(config)
    
    print("\n" + "=" * 70)
    print("✓ Setup completed successfully!")
    print("\nYou can now run the main script:")
    if system_info['os'] == 'Windows':
        print("  python main.py")
    else:
        print("  python3 main.py")
        print("  or")
        print("  ./main.py")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user. Exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERROR: Setup failed with error: {e}")
        print("\nFor help, visit: https://reddit-video-maker-bot.netlify.app/")
        raise
