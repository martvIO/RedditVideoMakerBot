#!/usr/bin/env python
"""
Setup script for Reddit Video Maker Bot
This script installs all required dependencies and performs necessary setup checks
before running the main application.
Works on Windows, macOS, and Linux.
"""

import sys
import platform
from pathlib import Path
from subprocess import run, CalledProcessError, PIPE


# ============================================================================
# PLATFORM UTILITIES
# ============================================================================

def get_platform_info():
    """Get detailed platform information"""
    return {
        'os': platform.system(),
        'os_version': platform.version(),
        'architecture': platform.machine(),
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'is_windows': platform.system() == 'Windows',
        'is_mac': platform.system() == 'Darwin',
        'is_linux': platform.system() == 'Linux',
    }


def get_pip_command():
    """Get the appropriate pip command for the current platform"""
    return [sys.executable, '-m', 'pip']


# ============================================================================
# PYTHON VERSION CHECK
# ============================================================================

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


# ============================================================================
# DEPENDENCIES INSTALLATION
# ============================================================================

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


# ============================================================================
# FFMPEG INSTALLATION
# ============================================================================

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


# ============================================================================
# CONFIGURATION SETUP
# ============================================================================

def setup_config():
    """Set up configuration file from template"""
    print("\n[4/5] Setting up configuration file...")
    
    try:
        from utils import settings
    except ImportError:
        print("ERROR: Cannot import 'utils.settings' module.")
        print("Please ensure you're running this script from the project root directory.")
        sys.exit(1)
    
    directory = Path().absolute()
    config_template = f"{directory}/utils/.config.template.toml"
    config_file = f"{directory}/config.toml"
    
    # Check if template exists
    if not Path(config_template).exists():
        print(f"ERROR: Configuration template not found at: {config_template}")
        print("Please ensure the project files are intact.")
        sys.exit(1)
    
    # Check and create config
    config = settings.check_toml(config_template, config_file)
    
    if config is False:
        print("ERROR: Failed to set up configuration file")
        sys.exit(1)
    
    if Path(config_file).exists():
        print(f"✓ Configuration file ready at: {config_file}")
    else:
        print(f"✓ Configuration created at: {config_file}")
    
    print("\n  IMPORTANT: Please edit config.toml to add your settings:")
    print("  - Reddit API credentials")
    print("  - TTS (Text-to-Speech) preferences")
    print("  - Video settings")
    
    return config


def validate_config(config):
    """Validate critical configuration settings"""
    print("\n[5/5] Validating configuration...")
    
    warnings = []
    errors = []
    
    # Check Reddit credentials
    try:
        reddit_config = config.get("reddit", {}).get("creds", {})
        if not reddit_config.get("client_id") or reddit_config.get("client_id") == "":
            warnings.append("Reddit client_id is not set")
        if not reddit_config.get("client_secret") or reddit_config.get("client_secret") == "":
            warnings.append("Reddit client_secret is not set")
    except Exception:
        warnings.append("Reddit credentials section may be incomplete")
    
    # Check TTS settings
    try:
        tts_config = config.get("settings", {}).get("tts", {})
        voice_choice = tts_config.get("voice_choice", "")
        
        # TikTok voice requires sessionid
        if voice_choice == "tiktok":
            sessionid = tts_config.get("tiktok_sessionid", "")
            if not sessionid or sessionid == "":
                errors.append(
                    "TikTok voice requires a sessionid! "
                    "Check the documentation on how to obtain one."
                )
        
        # ElevenLabs voice requires API key
        elif voice_choice == "elevenlabs":
            api_key = tts_config.get("elevenlabs_api_key", "")
            if not api_key or api_key == "":
                warnings.append("ElevenLabs API key is not set")
    
    except Exception:
        warnings.append("TTS configuration section may be incomplete")
    
    # Display warnings
    if warnings:
        print("\n  ⚠ WARNINGS:")
        for warning in warnings:
            print(f"    - {warning}")
        print("\n  The script may not work correctly until these are configured.")
    
    # Display errors and exit if any
    if errors:
        print("\n  ✗ ERRORS:")
        for error in errors:
            print(f"    - {error}")
        print("\n  Please fix these errors in config.toml before running the main script.")
        sys.exit(1)
    
    if not warnings and not errors:
        print("✓ Configuration validated successfully")
    else:
        print("\n✓ Configuration validation complete (with warnings)")
    
    print("\n  You can modify settings in: config.toml")


# ============================================================================
# MAIN SETUP FUNCTION
# ============================================================================

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
