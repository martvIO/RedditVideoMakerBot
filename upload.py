import os
from posixpath import abspath, dirname
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from dateutil.tz import *
import os
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Define the video folder relative to the current directory
video_folder = os.path.join(os.getcwd(), "results", "ask+AskReddit")

# Get the latest video in the directory
def get_latest_video(directory):
    # Get all .mp4 files in the directory
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.mp4')]
    if not files:
        raise FileNotFoundError("No video files found in the specified directory.")
    # Find the most recently created/modified video
    latest_video = max(files, key=os.path.getctime)
    return latest_video

try:
    # Get the latest video from the folder
    latest_video_path = get_latest_video(video_folder)
    print("Latest video:", latest_video_path)
except FileNotFoundError as e:
    print(e)

class TikTokBot:
    def __init__(self):
        # Path to chromedriver.exe
        chrome_service = Service("chromedriver.exe")
        self.driver = webdriver.Chrome(service=chrome_service)
        self.executor_url = self.driver.command_executor._proxy_url
        self.session_id = self.driver.session_id
        print(self.executor_url, self.session_id)


    def upload_video(self,video_path, caption, tags):
        self.driver.get('https://tiktok.com')
        while True:
            try:
                cookies = self.driver.get_cookies()
                cookies = [i for i in cookies if i['name'] == 'sessionid']
                if not cookies:
                    # Adding the sessionid cookie if it does not exist
                    self.driver.add_cookie({
                        "domain": ".tiktok.com",
                        "expirationDate": 1746020998.610075,
                        "hostOnly": False,
                        "httpOnly": True,
                        "name": "sessionid",
                        "path": "/",
                        "secure": True,
                        "session": False,
                        "storeId": None,
                        "value": "46cba0e284fa7a4a850584d8300bf10f",
                        'sameSite': 'None'
                    })
                    print("Added missing sessionid cookie.")
                if cookies:
                    print('session:', cookies[0])
                    break
            except KeyError:
                print('Make sure to login')
                time.sleep(10)

        self.url = self.driver.current_url
        print(self.url)
        self.driver.refresh()
        # takes you to the upload page

        self.driver.get("https://www.tiktok.com/tiktokstudio/upload?from=creator_center")

        # Wait until the file input element is present, then send file path
        file_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file" and @accept="video/*"]'))
        )
        file_input.send_keys(video_path)

        time.sleep(2)
        # set caption
        caption_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div/div/div/div/div/div'))
        )
        for i in range(len(caption_input.text)):
            caption_input.send_keys(Keys.BACKSPACE)
        # Send caption text one character at a time with a delay
        for char in caption:
            caption_input.send_keys(char)
            time.sleep(0.2)  # Adjust delay as needed
        
        hashtag_btn = WebDriverWait(self.driver,20).until(
            EC.element_to_be_clickable((By.XPATH,'//button[@id="web-creation-caption-hashtag-button"]'))
        )
    
        caption_input.send_keys(Keys.SPACE)
        # Send each tag with '#' one character at a time, then press Enterc
        for tag in tags:
            hashtag_btn.click()
            time.sleep(0.2)
            for char in tag:
                caption_input.send_keys(char)
                time.sleep(1)
            time.sleep(3)
            # Press Enter after each tag
            caption_input.send_keys(Keys.ENTER)
            time.sleep(0.2)  # Optional: add a short delay after pressing Enter
        
        time.sleep(2)
        # Wait until the button is clickable
        button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-e2e="post_video_button"]'))
        )

        button.click()
        time.sleep(10)
        self.driver.quit()

        # Delete the uploaded video
        os.remove(video_path)

tags_list = [
    "askreddit", "reddit", "story", "stories", "funny", "viral", "motivation", "inspiration",
    "relatable", "entertainment", "lifehacks", "tips", "fyp", "tiktok", "daily", "discussion",
    "thoughts", "qna", "trend", "commentary"
]

latest_video = get_latest_video(video_folder)
filename = os.path.splitext(os.path.basename(latest_video))[0]
random_tags = random.sample(tags_list, 10)  # Select 10 random tags
caption = filename  # Set the caption as the filename

bot = TikTokBot()
bot.upload_video(latest_video, caption, random_tags)
