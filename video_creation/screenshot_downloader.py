from fnmatch import translate
import json
import re
from pathlib import Path
from typing import Dict, Final
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService  # Changed import for Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options  # Changed import for Edge options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rich.progress import track

from utils import settings
from utils.console import print_step, print_substep
from utils.imagenarator import imagemaker
from utils.videos import save_data

__all__ = ["get_screenshots_of_reddit_posts"]

def get_screenshots_of_reddit_posts(reddit_object: dict, screenshot_num: int):
    """Downloads screenshots of reddit posts as seen on the web. Downloads to assets/temp/png

    Args:
        reddit_object (Dict): Reddit object received from reddit/subreddit.py
        screenshot_num (int): Number of screenshots to download
    """
    # settings values
    W: Final[int] = int(settings.config["settings"]["resolution_w"])
    H: Final[int] = int(settings.config["settings"]["resolution_h"])
    lang: Final[str] = settings.config["reddit"]["thread"]["post_lang"]
    storymode: Final[bool] = settings.config["settings"]["storymode"]

    print_step("Downloading screenshots of reddit posts...")
    reddit_id = re.sub(r"[^\w\s-]", "", reddit_object["thread_id"])
    Path(f"assets/temp/{reddit_id}/png").mkdir(parents=True, exist_ok=True)

    # Configure background colors based on settings
    if settings.config["settings"]["theme"] == "dark":
        bgcolor = (33, 33, 36, 255)
        txtcolor = (240, 240, 240)
        transparent = False
    elif settings.config["settings"]["theme"] == "transparent":
        bgcolor = (0, 0, 0, 0) if storymode else (33, 33, 36, 255)
        txtcolor = (255, 255, 255) if storymode else (240, 240, 240)
        transparent = storymode
    else:
        bgcolor = (255, 255, 255, 255)
        txtcolor = (0, 0, 0)
        transparent = False

    if storymode and settings.config["settings"]["storymodemethod"] == 1:
        print_substep("Generating images...")
        return imagemaker(
            theme=bgcolor,
            reddit_obj=reddit_object,
            txtclr=txtcolor,
            transparent=transparent,
        )

    options = webdriver.EdgeOptions()
    options.add_argument("--window-size=425,800")
    driver = webdriver.Edge(options=options)  # Use Edge instead of Chrome
    
    # Navigate to the Reddit post
    driver.get(reddit_object["thread_url"])
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Wait for page to load
    driver.implicitly_wait(5)

    # Take a screenshot of the post content
    post_content_path = f"assets/temp/{reddit_id}/png/title.png"
    try:
        post_content = driver.find_element(By.XPATH, '/html/body/shreddit-app/div[1]/div[1]/div/main/shreddit-post')
        post_content.screenshot(post_content_path)
    except Exception as e:
        print_substep("Something went wrong!", style="red")
        print(e)

    # Handle comments
    for idx, comment in enumerate(
        track(reddit_object["comments"][:screenshot_num], "Downloading screenshots...")
    ):
        # Stop if we have reached the screenshot_num
        if idx >= screenshot_num:
            break

        # Navigate to each comment URL
        print(comment)
        comment_id = comment["comment_id"]
        url = f"https://new.reddit.com/svc/shreddit/comment/t1_{comment_id}"
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Wait for the element to be present
        comment_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/shreddit-app/shreddit-comment"))
        )

        # Take a screenshot of the comment
        comment_path = f"assets/temp/{reddit_id}/png/comment_{idx}.png"
        comment_element.screenshot(comment_path)

    # Close the WebDriver instance
    driver.quit()

    print_substep("Screenshots downloaded Successfully.", style="bold green")
