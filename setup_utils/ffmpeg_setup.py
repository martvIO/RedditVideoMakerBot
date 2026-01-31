"""
FFmpeg installation and verification module
Handles FFmpeg setup across Windows, macOS, and Linux
"""

import sys
import platform
from subprocess import run, CalledProcessError, PIPE
from pathlib import Path


def check_ffmpeg_installed():
    """Check if FFmpeg is already installed on the system"""
    try:
        result = run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            # Extract version from output
            version_line = result.stdout.split('\n')[0]
            return True, version_line
        return False, None
    except FileNotFoundError:
        return False, None


def install_ffmpeg_windows():
    """Install FFmpeg on Windows"""
    print("\n  Installing FFmpeg on Windows...")
    print("  Please follow one of these methods:\n")
    print("  Method 1 - Using Chocolatey (Recommended):")
    print("    1. Install Chocolatey from: https://chocolatey.org/install")
    print("    2. Run: choco install ffmpeg")
    print("\n  Method 2 - Manual Installation:")
    print("    1. Download FFmpeg from: https://ffmpeg.org/download.html#build-windows")
    print("    2. Extract the archive")
    print("    3. Add the 'bin' folder to your system PATH")
    print("\n  Method 3 - Using winget:")
    print("    Run: winget install ffmpeg")
    
    response = input("\n  Have you installed FFmpeg? (y/n): ").lower()
    if response != 'y':
        print("  Please install FFmpeg and run this setup script again.")
        sys.exit(1)


def install_ffmpeg_mac():
    """Install FFmpeg on macOS"""
    print("\n  Installing FFmpeg on macOS...")
    
    # Check if Homebrew is installed
    try:
        run(['brew', '--version'], capture_output=True, check=True)
        print("  ✓ Homebrew detected")
        
        print("  Installing FFmpeg via Homebrew...")
        try:
            run(['brew', 'install', 'ffmpeg'], check=True)
            print("  ✓ FFmpeg installed successfully")
            return
        except CalledProcessError:
            print("  WARNING: Homebrew installation failed")
    except (FileNotFoundError, CalledProcessError):
        print("  Homebrew not found.")
    
    print("\n  Please install FFmpeg using one of these methods:\n")
    print("  Method 1 - Using Homebrew (Recommended):")
    print("    1. Install Homebrew: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
    print("    2. Run: brew install ffmpeg")
    print("\n  Method 2 - Using MacPorts:")
    print("    Run: sudo port install ffmpeg")
    print("\n  Method 3 - Manual Installation:")
    print("    Download from: https://ffmpeg.org/download.html#build-mac")
    
    response = input("\n  Have you installed FFmpeg? (y/n): ").lower()
    if response != 'y':
        print("  Please install FFmpeg and run this setup script again.")
        sys.exit(1)


def install_ffmpeg_linux():
    """Install FFmpeg on Linux"""
    print("\n  Installing FFmpeg on Linux...")
    
    # Detect Linux distribution
    try:
        with open('/etc/os-release', 'r') as f:
            os_info = f.read().lower()
    except FileNotFoundError:
        os_info = ""
    
    # Try automatic installation based on distro
    installed = False
    
    # Ubuntu/Debian
    if 'ubuntu' in os_info or 'debian' in os_info:
        print("  Detected Ubuntu/Debian-based system")
        try:
            print("  Running: sudo apt-get update && sudo apt-get install -y ffmpeg")
            run(['sudo', 'apt-get', 'update'], check=True)
            run(['sudo', 'apt-get', 'install', '-y', 'ffmpeg'], check=True)
            print("  ✓ FFmpeg installed successfully")
            installed = True
        except CalledProcessError:
            print("  WARNING: Automatic installation failed")
    
    # Fedora/RHEL/CentOS
    elif 'fedora' in os_info or 'rhel' in os_info or 'centos' in os_info:
        print("  Detected Fedora/RHEL-based system")
        try:
            print("  Running: sudo dnf install -y ffmpeg")
            run(['sudo', 'dnf', 'install', '-y', 'ffmpeg'], check=True)
            print("  ✓ FFmpeg installed successfully")
            installed = True
        except CalledProcessError:
            print("  WARNING: Automatic installation failed")
    
    # Arch Linux
    elif 'arch' in os_info or 'manjaro' in os_info:
        print("  Detected Arch-based system")
        try:
            print("  Running: sudo pacman -S --noconfirm ffmpeg")
            run(['sudo', 'pacman', '-S', '--noconfirm', 'ffmpeg'], check=True)
            print("  ✓ FFmpeg installed successfully")
            installed = True
        except CalledProcessError:
            print("  WARNING: Automatic installation failed")
    
    if not installed:
        print("\n  Please install FFmpeg manually:")
        print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("  Fedora/RHEL:   sudo dnf install ffmpeg")
        print("  Arch Linux:    sudo pacman -S ffmpeg")
        
        response = input("\n  Have you installed FFmpeg? (y/n): ").lower()
        if response != 'y':
            print("  Please install FFmpeg and run this setup script again.")
            sys.exit(1)


def install_ffmpeg():
    """Check and install FFmpeg if needed"""
    print("\n[3/5] Checking FFmpeg installation...")
    
    # Check if FFmpeg is already installed
    is_installed, version = check_ffmpeg_installed()
    
    if is_installed:
        print(f"✓ FFmpeg is already installed")
        print(f"  {version}")
        return
    
    print("  FFmpeg is not installed or not in PATH")
    
    # Try using the project's ffmpeg_install if available
    try:
        from utils.ffmpeg_install import ffmpeg_install
        print("  Using project's FFmpeg installer...")
        ffmpeg_install()
        
        # Verify installation
        is_installed, version = check_ffmpeg_installed()
        if is_installed:
            print(f"✓ FFmpeg installed successfully")
            print(f"  {version}")
            return
    except ImportError:
        pass
    except Exception as e:
        print(f"  Project installer failed: {e}")
    
    # Platform-specific installation
    current_os = platform.system()
    
    if current_os == 'Windows':
        install_ffmpeg_windows()
    elif current_os == 'Darwin':
        install_ffmpeg_mac()
    elif current_os == 'Linux':
        install_ffmpeg_linux()
    else:
        print(f"  Unsupported operating system: {current_os}")
        print("  Please install FFmpeg manually from: https://ffmpeg.org/download.html")
        sys.exit(1)
    
    # Final verification
    is_installed, version = check_ffmpeg_installed()
    if not is_installed:
        print("\n  ERROR: FFmpeg installation could not be verified.")
        print("  Please ensure FFmpeg is installed and available in your PATH.")
        sys.exit(1)
    
    print(f"✓ FFmpeg is ready")
    print(f"  {version}")
