"""
Configuration setup and validation module
"""

import sys
from pathlib import Path


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
