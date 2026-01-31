"""
Platform utilities for cross-platform compatibility
"""

import sys
import platform


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


def get_shell_command(command):
    """Get the appropriate shell command for the current platform"""
    if platform.system() == 'Windows':
        return f'cmd /c {command}'
    return command


def get_python_command():
    """Get the appropriate Python command for the current platform"""
    if platform.system() == 'Windows':
        return 'python'
    return 'python3'


def get_pip_command():
    """Get the appropriate pip command for the current platform"""
    return [sys.executable, '-m', 'pip']
