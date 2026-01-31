# Reddit Video Maker Bot - Setup Guide

Complete installation and setup instructions for Windows, macOS, and Linux.

---

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Setup Instructions](#detailed-setup-instructions)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Platform-Specific Notes](#platform-specific-notes)
- [Manual Setup](#manual-setup)
- [Getting Help](#getting-help)

---

## Prerequisites

### Required Software

1. **Python 3.10 or 3.11** (Required)
   - Download from: https://www.python.org/downloads/
   - ⚠️ **Important**: Python 3.12+ is NOT supported yet
   - During installation on Windows, check "Add Python to PATH"

2. **FFmpeg** (Will be installed during setup)
   - The setup script will help you install this

3. **Git** (Optional, for cloning the repository)
   - Download from: https://git-scm.com/downloads

---

## Quick Start

### Windows

1. Open Command Prompt or PowerShell in the project folder
2. Run one of these commands:
   ```cmd
   setup.bat
   ```
   OR
   ```cmd
   python setup.py
   ```

### macOS / Linux

1. Open Terminal in the project folder
2. Run one of these commands:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
   OR
   ```bash
   python3 setup.py
   ```

3. Follow the on-screen instructions

---

## Detailed Setup Instructions

### Step 1: Download the Project

**Option A: Using Git (Recommended)**
```bash
git clone https://github.com/YOUR_USERNAME/RedditVideoMakerBot.git
cd RedditVideoMakerBot
```

**Option B: Download ZIP**
1. Download the project as a ZIP file
2. Extract it to a folder
3. Open terminal/command prompt in that folder

### Step 2: Run the Setup Script

The setup script will:
1. ✅ Verify Python version (3.10 or 3.11 required)
2. ✅ Install Python dependencies from `requirements.txt`
3. ✅ Check/install FFmpeg
4. ✅ Create configuration file from template
5. ✅ Validate your settings

**Choose your setup version:**

#### Standalone Version (Recommended)
- Single file, easiest to use
- File: `setup.py`
- Run: `python setup.py` (Windows) or `python3 setup.py` (Mac/Linux)

#### Modular Version
- Organized into multiple modules
- Files: `setup_modular.py` + `setup_utils/` folder
- Rename `setup_modular.py` to `setup.py` before running
- Run: `python setup.py` (Windows) or `python3 setup.py` (Mac/Linux)

### Step 3: Configure Your Settings

After setup completes, you need to edit `config.toml`:

1. Open `config.toml` in a text editor
2. Add your Reddit API credentials (see [Getting Reddit API Keys](#getting-reddit-api-keys))
3. Configure TTS (Text-to-Speech) settings
4. Customize video settings (optional)

### Step 4: Run the Bot

**Windows:**
```cmd
python main.py
```

**macOS/Linux:**
```bash
python3 main.py
```

---

## Configuration

### Getting Reddit API Keys

1. Go to: https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in the form:
   - **Name**: Your app name (e.g., "My Video Bot")
   - **App type**: Select "script"
   - **Description**: Optional
   - **About URL**: Leave blank
   - **Redirect URI**: http://localhost:8080
4. Click "Create app"
5. Copy your credentials:
   - **client_id**: The string under "personal use script"
   - **client_secret**: The "secret" value

### Editing config.toml

Open `config.toml` and update these sections:

```toml
[reddit.creds]
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
username = "YOUR_REDDIT_USERNAME"
password = "YOUR_REDDIT_PASSWORD"

[reddit.thread]
subreddit = "AskReddit"  # Subreddit to pull from
post_id = ""  # Leave empty for random, or specify a post ID

[settings.tts]
voice_choice = "pyttsx"  # Options: pyttsx, tiktok, elevenlabs, etc.
# If using tiktok:
# tiktok_sessionid = "YOUR_SESSION_ID"
# If using elevenlabs:
# elevenlabs_api_key = "YOUR_API_KEY"
```

### TTS (Text-to-Speech) Options

1. **pyttsx** (Free, offline, no API key needed)
   - Best for testing
   - Lower quality voices

2. **TikTok TTS** (Free, requires session ID)
   - Good quality
   - See documentation for getting session ID

3. **ElevenLabs** (Paid, requires API key)
   - Highest quality
   - Natural-sounding voices
   - Sign up at: https://elevenlabs.io/

---

## Troubleshooting

### Common Issues

#### ❌ "Python is not recognized"

**Problem:** Python is not in your system PATH

**Solution:**
- **Windows**: Reinstall Python and check "Add Python to PATH"
- **Mac/Linux**: Python 3 should be installed by default. Try `python3` instead of `python`

#### ❌ "No module named 'setup_utils'"

**Problem:** The `setup_utils` folder is missing (only for modular version)

**Solution:**
- Use the standalone `setup.py` instead (recommended)
- OR download the complete `setup_utils/` folder

#### ❌ "ModuleNotFoundError" when running main.py

**Problem:** Python dependencies weren't installed

**Solution:**
```bash
# Windows
python -m pip install -r requirements.txt

# Mac/Linux
python3 -m pip install -r requirements.txt
```

#### ❌ "FFmpeg not found"

**Problem:** FFmpeg is not installed or not in PATH

**Solution:**
- **Windows**: 
  ```cmd
  choco install ffmpeg
  ```
  Or download manually and add to PATH

- **Mac**:
  ```bash
  brew install ffmpeg
  ```

- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt-get install ffmpeg
  ```

#### ❌ "TikTok voice requires a sessionid"

**Problem:** You selected TikTok TTS but didn't provide session ID

**Solution:**
- Change `voice_choice` to `"pyttsx"` in config.toml
- OR get a TikTok session ID (see documentation)
- OR use a different TTS option

#### ❌ Permission errors (Mac/Linux)

**Problem:** Script doesn't have execute permissions

**Solution:**
```bash
chmod +x setup.sh
chmod +x setup.py
```

### Version Issues

#### Multiple Python Versions Installed

If you have multiple Python versions:

**Windows:**
```cmd
py -3.10 setup.py
# or
py -3.11 setup.py
```

**Mac/Linux:**
```bash
python3.10 setup.py
# or
python3.11 setup.py
```

#### Wrong Python Version

**Problem:** You have Python 3.9 or 3.12+

**Solution:**
- Install Python 3.10 or 3.11
- Use pyenv to manage multiple Python versions:
  ```bash
  # Install pyenv, then:
  pyenv install 3.10.11
  pyenv local 3.10.11
  ```

---

## Platform-Specific Notes

### Windows

**FFmpeg Installation Options:**

1. **Chocolatey** (Recommended):
   ```cmd
   choco install ffmpeg
   ```

2. **winget**:
   ```cmd
   winget install ffmpeg
   ```

3. **Manual**:
   - Download from: https://ffmpeg.org/download.html#build-windows
   - Extract to `C:\ffmpeg`
   - Add `C:\ffmpeg\bin` to system PATH

**Adding to PATH:**
1. Search "Environment Variables" in Start Menu
2. Click "Environment Variables"
3. Under "System Variables", find "Path"
4. Click "Edit" → "New"
5. Add the ffmpeg bin folder path
6. Click "OK" on all dialogs
7. Restart Command Prompt

### macOS

**FFmpeg Installation:**

**Method 1 - Homebrew** (Recommended):
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install FFmpeg
brew install ffmpeg
```

**Method 2 - MacPorts**:
```bash
sudo port install ffmpeg
```

**Python Installation:**
```bash
# Using Homebrew
brew install python@3.10
```

### Linux

**FFmpeg Installation:**

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Fedora/RHEL:**
```bash
sudo dnf install ffmpeg
```

**Arch Linux:**
```bash
sudo pacman -S ffmpeg
```

**Python Installation:**

**Ubuntu/Debian:**
```bash
sudo apt-get install python3.10 python3-pip
```

**Fedora:**
```bash
sudo dnf install python3.10 python3-pip
```

---

## Manual Setup

If you prefer to set up manually without the setup script:

### 1. Install Python 3.10 or 3.11
Download from: https://www.python.org/downloads/

### 2. Install FFmpeg
Follow platform-specific instructions above

### 3. Install Python Dependencies
```bash
# Windows
python -m pip install -r requirements.txt

# Mac/Linux
python3 -m pip install -r requirements.txt
```

### 4. Create Configuration File
```bash
# Copy template to config.toml
cp utils/.config.template.toml config.toml
```

### 5. Edit Configuration
Open `config.toml` and add your settings

### 6. Run the Bot
```bash
# Windows
python main.py

# Mac/Linux
python3 main.py
```

---

## File Structure

After setup, your project should look like this:

```
RedditVideoMakerBot/
├── setup.py                    # Setup script (standalone version)
├── setup.bat                   # Windows launcher
├── setup.sh                    # Linux/Mac launcher
├── setup_modular.py            # Modular setup script (optional)
├── setup_utils/                # Setup utilities (for modular version)
│   ├── __init__.py
│   ├── platform_utils.py
│   ├── version_check.py
│   ├── dependencies.py
│   ├── ffmpeg_setup.py
│   └── config_setup.py
├── main.py                     # Main application
├── config.toml                 # Your configuration (created by setup)
├── requirements.txt            # Python dependencies
├── utils/                      # Utility modules
│   ├── .config.template.toml   # Configuration template
│   └── ...
├── reddit/                     # Reddit integration
├── video_creation/             # Video creation modules
└── ...
```

---

## Getting Help

### Resources

- 📖 **Documentation**: https://reddit-video-maker-bot.netlify.app/
- 💬 **Discord**: [Join the community]
- 🐛 **GitHub Issues**: [Report bugs or request features]
- 📺 **Video Tutorial**: [Link to tutorial if available]

### Before Asking for Help

Please provide:
1. Your operating system (Windows/Mac/Linux)
2. Python version: `python --version`
3. Error message (full text)
4. What you were trying to do
5. Steps you've already tried

### Common Questions

**Q: Can I use Python 3.12?**
A: Not yet. The bot currently only supports Python 3.10 and 3.11.

**Q: Do I need a Reddit Premium account?**
A: No, a free Reddit account works fine.

**Q: How long does it take to create a video?**
A: Depends on your computer and video length, typically 2-10 minutes.

**Q: Can I monetize videos created with this bot?**
A: Check Reddit's terms of service and the subreddit rules where you're pulling content from.

**Q: The video quality is poor, how do I improve it?**
A: Adjust settings in `config.toml` under `[settings.video]`

**Q: Can I run this on a server/VPS?**
A: Yes, but you'll need to configure a headless environment for browser automation.

---

## Next Steps

After successful setup:

1. ✅ Test the bot with a simple post
2. ✅ Customize your video settings
3. ✅ Experiment with different subreddits
4. ✅ Try different TTS voices
5. ✅ Set up automatic scheduling (optional)

---

## License

This setup guide is part of the Reddit Video Maker Bot project.
See the main README for license information.

---

## Credits

Setup scripts created to simplify the installation process across all platforms.

---

**Happy Video Making! 🎬**

For issues or suggestions about this setup process, please open an issue on GitHub.