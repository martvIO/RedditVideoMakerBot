import os
import schedule
import time
import subprocess
from datetime import datetime
from pynput import mouse, keyboard
import googleapiclient.discovery
from colorama import Fore, Style, init
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import toml
init(autoreset=True)  # Initialize colorama

# Configuration - same as your upload script
SCOPES = ["https://www.googleapis.com/auth/youtube", 
          "https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.force-ssl"]
TOKEN_FILE = 'token.pickle'
CLIENT_SECRETS_FILE = "client.json"
LOG_FILE = 'credential_check.log'

class InputBlocker:
    def __init__(self):
        self.blocking = False
        self.mouse_listener = None
        self.keyboard_listener = None
    
    def block_mouse(self, x, y, button, pressed):
        if self.blocking:
            return False  # Suppress mouse input
        return True
    
    def block_keyboard(self, key):
        if self.blocking:
            return False  # Suppress keyboard input
        return True
    
    def start_blocking(self):
        if self.blocking:
            return
        
        self.blocking = True
        log("Input blocking started")
        
        # Start listeners
        self.mouse_listener = mouse.Listener(
            on_click=self.block_mouse,
            suppress=True
        )
        self.keyboard_listener = keyboard.Listener(
            on_press=self.block_keyboard,
            suppress=True
        )
        
        self.mouse_listener.start()
        self.keyboard_listener.start()
    
    def stop_blocking(self):
        if not self.blocking:
            return
        
        self.blocking = False
        log("Input blocking stopped")
        
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
        
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None

# Global input blocker instance
input_blocker = InputBlocker()

def log(message):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.now()}: {message}\n")
    print(f"{datetime.now()}: {message}")

def run_scripts():
    # Path to the Python executable in the virtual environment
    venv_python = os.path.join(os.path.dirname(__file__), '.venv', 'Scripts', 'python.exe')

    if not os.path.isfile(venv_python):
        log(f"Python executable not found at {venv_python}")
        return

    try:
        # Start input blocking before running main.py
        log("Starting input blocking...")
        input_blocker.start_blocking()
        
        # Run main.py with input blocked
        log("Running main.py with input blocked...")
        main_result = subprocess.run([venv_python, "main.py"], check=True)
        log(f"main.py completed successfully with return code {main_result.returncode}.")
        
    except subprocess.CalledProcessError as e:
        log(f"An error occurred while running main.py: {e}")
        log(f"Return code: {e.returncode}")
    finally:
        # Always stop input blocking after main.py finishes (success or error)
        log("Stopping input blocking...")
        input_blocker.stop_blocking()
        
    # Small delay to ensure input is fully restored
    time.sleep(1)
    
    # Run upload.py (s.py) with normal input
    try:
        log("Running s.py with normal input...")
        upload_result = subprocess.run([venv_python, "s.py"], check=True)
        log(f"s.py completed successfully with return code {upload_result.returncode}.")
    except subprocess.CalledProcessError as e:
        log(f"An error occurred while running s.py: {e}")
        log(f"Return code: {e.returncode}")

def log_message(message, level="info", log_to_file=True):
    """Log message to console and optionally to file"""
    colors = {
        "info": Fore.CYAN,
        "success": Fore.GREEN,
        "warning": Fore.YELLOW,
        "error": Fore.RED
    }
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"
    
    # Print to console with color
    print(colors.get(level, Fore.WHITE) + formatted_message + Style.RESET_ALL)
    
    # Log to file if enabled
    if log_to_file:
        try:
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(f"{formatted_message}\n")
        except Exception as e:
            print(f"Failed to write to log file: {e}")

def check_youtube_credentials():
    """Check if YouTube credentials are valid and working"""
    log_message("=" * 50, "info")
    log_message("Starting YouTube credentials check...", "info")
    
    try:
        # Check if token file exists
        if not os.path.exists(TOKEN_FILE):
            log_message("Token file not found - credentials need to be set up", "error")
            return False
        
        if not os.path.exists(CLIENT_SECRETS_FILE):
            log_message("Client secrets file not found", "error")
            return False
        
        # Load credentials
        log_message("Loading credentials from token file...", "info")
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        
        # Check if credentials are valid
        if not credentials:
            log_message("Failed to load credentials", "error")
            return False
        
        if not credentials.valid:
            if credentials.expired and credentials.refresh_token:
                log_message("Credentials expired - attempting to refresh...", "warning")
                try:
                    credentials.refresh(Request())
                    
                    # Save refreshed credentials
                    with open(TOKEN_FILE, 'w') as token:
                        token.write(credentials.to_json())
                    
                    log_message("Credentials refreshed and saved successfully", "success")
                except Exception as e:
                    log_message(f"Failed to refresh credentials: {e}", "error")
                    return False
            else:
                log_message("Credentials invalid and cannot be refreshed", "error")
                return False
        
        # Test the credentials by making a simple API call
        log_message("Testing credentials with YouTube API...", "info")
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        
        youtube = googleapiclient.discovery.build(
            "youtube", "v3", 
            credentials=credentials, 
            cache_discovery=False
        )
        
        # Make a simple API call to test credentials
        request = youtube.channels().list(
            part="snippet,statistics",
            mine=True
        )
        
        response = request.execute()
        
        if 'items' in response and len(response['items']) > 0:
            channel = response['items'][0]
            channel_title = channel['snippet']['title']
            subscriber_count = channel['statistics'].get('subscriberCount', 'Hidden')
            
            log_message(f"✓ Credentials working! Connected to channel: {channel_title}", "success")
            log_message(f"✓ Subscriber count: {subscriber_count}", "success")
            
            # Check quota usage (approximate)
            log_message("✓ API call successful - credentials are fully functional", "success")
            return True
        else:
            log_message("API call successful but no channel data returned", "warning")
            return False
            
    except Exception as e:
        log_message(f"Error during credential check: {e}", "error")
        return False

def comprehensive_system_check():
    """Perform a more comprehensive check of the system"""
    log_message("Performing comprehensive system check...", "info")
    
    # Check file permissions
    files_to_check = [TOKEN_FILE, CLIENT_SECRETS_FILE]
    for file_path in files_to_check:
        if os.path.exists(file_path):
            if os.access(file_path, os.R_OK):
                log_message(f"✓ {file_path} is readable", "success")
            else:
                log_message(f"✗ {file_path} is not readable", "error")
        else:
            log_message(f"✗ {file_path} does not exist", "error")
    
    # Check internet connectivity (basic)
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        log_message("✓ Internet connectivity available", "success")
    except OSError:
        log_message("✗ No internet connectivity", "error")

def scheduled_check():
    """The function that gets called by the scheduler"""
    try:
        log_message("🔍 Hourly credential check started", "info")
        
        # Perform comprehensive check
        comprehensive_system_check()
        
        # Check credentials
        is_valid = check_youtube_credentials()
        
        if is_valid:
            log_message("✅ All systems operational - credentials are valid", "success")
        else:
            log_message("❌ ATTENTION: Credentials check failed!", "error")
            log_message("   -> Manual intervention may be required", "error")
            log_message("   -> Check logs and re-authenticate if necessary", "error")
        
        log_message("🔍 Hourly credential check completed", "info")
        log_message("=" * 50, "info")
        
    except Exception as e:
        log_message(f"Unexpected error during scheduled check: {e}", "error")




def main():
    # Schedule the script to run every hour
    schedule.every().day.at("14:00").do(run_scripts)
    schedule.every().hour.do()
    log("Scheduler with input blocking is starting...")
    log("Input will be blocked only while main.py is running")
        # Create log file if it doesn't exist
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.write(f"YouTube Credential Checker Log - Started {datetime.now()}\n")
            f.write("=" * 60 + "\n")
    
    log_message("YouTube Credential Checker started", "success")
    log_message(f"Log file: {LOG_FILE}", "info")
    log_message("Scheduled to run every hour", "info")
    
    # Schedule the check to run every hour
    schedule.every().hour.do(scheduled_check)
    
    # Run an initial check
    log_message("Running initial credential check...", "info")
    scheduled_check()
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        log("Scheduler interrupted by user")
        # Make sure to stop input blocking if interrupted
        input_blocker.stop_blocking()
    except Exception as e:
        log(f"Unexpected error in scheduler: {e}")
        # Make sure to stop input blocking on any error
        input_blocker.stop_blocking()
if __name__ == "__main__":
    main()