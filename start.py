import base64
from cmath import log
import json
from pathlib import Path 
import os
import shutil
import uuid
import requests
from cryptography.fernet import Fernet
from app import run_scripts, main as app_main
DEBUG = True
PRODUCT_NAME = "Reddit Video Generator"
APPDATA_DIR = Path(os.getenv('APPDATA')) / 'Terra PDF'
LICENSE_PATH = APPDATA_DIR / 'RedditVideoGenerator.lic'

MOBO_UUID = str(uuid.UUID(int=uuid.getnode()))
INSTANCE_NAME = MOBO_UUID.split("-")[-1]
FERNET_KEY = base64.urlsafe_b64encode(bytes(MOBO_UUID, 'utf-8')[-32:])

def activate_licence(license_key: str) -> bool:
    """Activate the application using the provided licence key."""
    if license_key == None or license_key == '':
        return False
    
    activated = False
    
    try:
        data = {
            'license_key': license_key,
            'instance_name': INSTANCE_NAME,
        }
        
        r = requests.post(
            'https://api.lemonsqueezy.com/v1/licenses/activate',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
            },
            data=data
        )
        
        r = r.json()
        
        if r["activated"] == True:
            activated = True
            if not APPDATA_DIR.exists():
                APPDATA_DIR.mkdir(parents=True)
                
            if LICENSE_PATH.exists() and LICENSE_PATH.is_dir():
                shutil.rmtree(LICENSE_PATH,ignore_errors=True)
                
            with open(LICENSE_PATH, 'wb') as license_file:
                f = Fernet(FERNET_KEY)
                
                license_data = {
                    "license_key": license_key,
                    "instance_id": r["instance"]["id"],
                }
                
                license_file.write(f.encrypt(bytes(json.dumps(license_data), 'utf-8')))
                
            activated = True
        else:
            print("Activation failed ")
    except Exception as e:
        if DEBUG:
            print(f"Activation error: {e}")
    finally:
        return activated
    
def validate_license(license_key: str = None, instance_id: str = None) -> bool:
    valid = False
    try:
        if license_key is None:
            if not LICENSE_PATH.exists():
                print("License file not found.")
                
            with open(LICENSE_PATH, 'rb') as license_file:
                f =Fernet(FERNET_KEY)
                data = f.decrypt(license_file.read())
                license_data = json.loads(data.decode('utf-8'))
                
                license_key = license_data["license_key"]
                instance_id = license_data["instance_id"]
                
        if license_key is None or instance_id is None:
            return False
        
        data = {
            "license_key": license_key,
            "instance_id": instance_id,
        } 
        
        r = requests.post(
            'https://api.lemonsqueezy.com/v1/licenses/validate',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
            },
            data=data
        )
        
        r = r.json()
        
        if r['valid'] == True and r['instance']['id'] == instance_id and r['meta']['product_name'] == f'{PRODUCT_NAME}':
            valid = True
        else:
            print("License validation failed.")
    except Exception as e:
        if DEBUG:
            print(f"Validation error: {e}") 
    finally:
        return valid

def main():
    # Example usage
    if not validate_license():
        license_key = input("Enter your license key: ")
        if activate_licence(license_key):
            print("License activated successfully.")
            if validate_license():
                print("License is valid.")
            else:
                print("License is invalid.")
        else:
            print("License activation failed.")
        return
    # Path to the Python executable in the virtual environment
    venv_python = os.path.join(os.path.dirname(__file__), '.venv', 'Scripts', 'python.exe')

    if not os.path.isfile(venv_python):
        log(f"Python executable not found at {venv_python}")
        return
    print("License is valid.")
    input_choice = int(input("Do you want to run the script now without uploading to youtube (1) or run it on the schedule (2)? "))
    print("important: don't turn off the pc when running on schedule")
    if input_choice == 1:
        run_scripts()
    elif input_choice == 2:
        app_main()
    else:
        print("Invalid choice. Exiting.")
if __name__ == "__main__":
    main()