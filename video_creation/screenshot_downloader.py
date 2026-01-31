import re
from pathlib import Path
from typing import Final
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rich.progress import track
from utils import settings
from utils.console import print_step, print_substep
from utils.imagenarator import imagemaker
from selenium.webdriver.edge.options import Options
op = Options()
from selenium.webdriver.edge.options import Options
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

    
    options = Options()
    options.add_argument("--window-size=425,800")
    driver = webdriver.Edge(options=options)  # Use Edge instead of Chrome
    driver.get("https://reddit.com")
    driver.implicitly_wait(5)
    c = {'name': 'reddit_session','value': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpsVFdYNlFVUEloWktaRG1rR0pVd1gvdWNFK01BSjBYRE12RU1kNzVxTXQ4IiwidHlwIjoiSldUIn0.eyJzdWIiOiJ0Ml90MHVzaWh6byIsImp0aSI6IlNJeWVQN3JfbW9DUmRvb1l0NFdSaHRYM01uWm9pUSIsImV4cCI6MTc2NTYzMzg1NS4wNzEzNTEsImlhdCI6MTc0OTk5NTQ1NS4wNzEzNTEsImNpZCI6ImNvb2tpZSIsInNjcCI6ImVKeUtqZ1VFQUFEX193RVZBTGsiLCJ2MSI6IjIyNzQ0MjI2MzY0MzYsMjAyNC0xMS0wMVQxMDo0ODo1OCw5NWRhODZkYjVhODBkNDg5YjU2ZDE4ZWQ2NTBhNDQ2YTE5YmUxYjk4IiwibGNhIjoxNjY0NzUwMjg3MDAwLCJmbG8iOjJ9.GI2EFvU2sDcGBv_08jKpfdQvfrVqX5z52Rz-fNh77QNKlfBvwMNSKZuZYe28WgGY40s76fOS6Ws9wAZJ8ezDV8aRcNgAGON0kT1p0TewXY2L2Zp3O-6i1690uRJVg_meeO_ekSXpErG0f9HLbv6gc2ooLn7lE33m4RRjOJIirpTos_ZdSb2eZPQ51XEeLY5-08A_aMRDo-twTgM3NrDHx8URp1r8rNke6I2jmrbnXhEer3PkDHPTxgFobc0Gibr7usKTHDiaaid3qsFFYnH4akfrzCvMPQFz0BiQyFj4DSzbizpQZQGa3rSMfkuJSBVDXyjeGUuS69V9R6elJLlmXg', 'domain': '.reddit.com', 'path': '/'}
    # Navigate to the Reddit post
    driver.add_cookie({'name': 'reddit_session','value': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpsVFdYNlFVUEloWktaRG1rR0pVd1gvdWNFK01BSjBYRE12RU1kNzVxTXQ4IiwidHlwIjoiSldUIn0.eyJzdWIiOiJ0Ml90MHVzaWh6byIsImp0aSI6IlNJeWVQN3JfbW9DUmRvb1l0NFdSaHRYM01uWm9pUSIsImV4cCI6MTc2NTYzMzg1NS4wNzEzNTEsImlhdCI6MTc0OTk5NTQ1NS4wNzEzNTEsImNpZCI6ImNvb2tpZSIsInNjcCI6ImVKeUtqZ1VFQUFEX193RVZBTGsiLCJ2MSI6IjIyNzQ0MjI2MzY0MzYsMjAyNC0xMS0wMVQxMDo0ODo1OCw5NWRhODZkYjVhODBkNDg5YjU2ZDE4ZWQ2NTBhNDQ2YTE5YmUxYjk4IiwibGNhIjoxNjY0NzUwMjg3MDAwLCJmbG8iOjJ9.GI2EFvU2sDcGBv_08jKpfdQvfrVqX5z52Rz-fNh77QNKlfBvwMNSKZuZYe28WgGY40s76fOS6Ws9wAZJ8ezDV8aRcNgAGON0kT1p0TewXY2L2Zp3O-6i1690uRJVg_meeO_ekSXpErG0f9HLbv6gc2ooLn7lE33m4RRjOJIirpTos_ZdSb2eZPQ51XEeLY5-08A_aMRDo-twTgM3NrDHx8URp1r8rNke6I2jmrbnXhEer3PkDHPTxgFobc0Gibr7usKTHDiaaid3qsFFYnH4akfrzCvMPQFz0BiQyFj4DSzbizpQZQGa3rSMfkuJSBVDXyjeGUuS69V9R6elJLlmXg', 'domain': 'reddit.com', 'path': '/'})
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
        print(reddit_object["comments"])
        # Stop if we have reached the screenshot_num
        if idx >= screenshot_num:
            break

        # Navigate to each comment URL
        print(comment)
        comment_id = comment["comment_id"]
        url = f"https://embed.reddit.com/r/AskReddit/comments/{reddit_object['thread_id']}/comment/{comment_id}/?embed=true&utm_medium=widgets&utm_source=embedv2&utm_term=23&theme=dark&showusername=false&showedits=false&showmedia=false&showmore=false&depth=1&utm_name=comment_embed&embed_host_url=https%3A%2F%2Fpublish.reddit.com%2Fembed"
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
        # Wait for the element to be present
        comment_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body"))
        )

        # Take a screenshot of the comment
        comment_path = f"assets/temp/{reddit_id}/png/comment_{idx}.png"
        comment_element.screenshot(comment_path)

    # Close the WebDriver instance
    driver.quit()

    print_substep("Screenshots downloaded Successfully.", style="bold green")
