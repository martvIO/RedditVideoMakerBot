import os
import schedule
import time
import subprocess
from datetime import datetime

# Setup logging
log_file = 'scheduler.log'

def log(message):
    with open(log_file, 'a') as f:
        f.write(f"{datetime.now()}: {message}\n")

def run_scripts():
    # Path to the Python executable in the virtual environment
    venv_python = os.path.join(os.path.dirname(__file__), '.venv', 'Scripts', 'python.exe')

    if not os.path.isfile(venv_python):
        log(f"Python executable not found at {venv_python}")
        return

    # Run main.py
    log("Running main.py...")
    try:
        main_result = subprocess.run([venv_python, "main.py"], check=True)
        log(f"main.py completed successfully with return code {main_result.returncode}.")
        
        # Run upload.py
        log("Running upload.py...")
        upload_result = subprocess.run([venv_python, "upload.py"], check=True)
        log(f"upload.py completed successfully with return code {upload_result.returncode}.")
    except subprocess.CalledProcessError as e:
        log(f"An error occurred while running the script: {e}")
        log(f"Return code: {e.returncode}")

# Schedule the script to run every hour
schedule.every().hour.do(run_scripts)

if __name__ == "__main__":
    log("Scheduler is starting...")
    while True:
        schedule.run_pending()
        time.sleep(60)
