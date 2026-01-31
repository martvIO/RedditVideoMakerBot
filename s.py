import os
import toml
import googleapiclient.discovery
import googleapiclient.http
from colorama import Fore, Style, init
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

init(autoreset=True)  # Initialize colorama

# Define scope for maximum access while minimizing re-authentication needs
SCOPES = ["https://www.googleapis.com/auth/youtube", 
          "https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.force-ssl"]
TOKEN_FILE = 'token.pickle'
CLIENT_SECRETS_FILE = "client.json"

def log_message(message, level="info"):
    colors = {
        "info": Fore.CYAN,
        "success": Fore.GREEN,
        "warning": Fore.YELLOW,
        "error": Fore.RED
    }
    print(colors.get(level, Fore.WHITE) + message + Style.RESET_ALL)

def authenticate_youtube():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    credentials = None

    # Load from token.json
    if os.path.exists(TOKEN_FILE):
        log_message("Loading existing credentials...", "info")
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # Check validity and refresh if needed
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            log_message("Refreshing expired credentials...", "warning")
            try:
                credentials.refresh(Request())
                log_message("Credentials refreshed successfully!", "success")
            except Exception as e:
                log_message(f"Failed to refresh: {e}. Re-authenticating...", "error")
                credentials = None

        if not credentials:
            log_message("Starting new auth flow...", "warning")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=8080, prompt='consent')

        # Save to token.json
        with open(TOKEN_FILE, 'w') as token:
            token.write(credentials.to_json())
        log_message("Saved new token.", "success")

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials, cache_discovery=False)
    return youtube

def upload_video(youtube, title, description, tags, made_for_kids, media_file):
    log_message(f"Starting upload for: {media_file}", "info")
    request_body = {
        "snippet": {
            "categoryId": "22",
            "title": title,
            "description": description,
            "tags": tags
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": made_for_kids
        }
    }

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=googleapiclient.http.MediaFileUpload(media_file, chunksize=-1, resumable=True)
    )

    response = None
    try:
        while response is None:
            status, response = request.next_chunk()
            if status:
                log_message(f"Upload {int(status.progress() * 100)}% complete", "info")

        log_message(f"Video uploaded successfully with ID: {response['id']}", "success")
        return True, response['id']

    except Exception as e:
        log_message(f"An error occurred during upload: {e}", "error")
        return False, None

import random

def generate_youtube_description(subreddit_title: str, subreddit_name: str = "AskReddit") -> str:
    # Expanded hook variations (30+ options)
    hooks = [
        f"You won't believe this story from r/{subreddit_name}... 👀",
        f"This r/{subreddit_name} story is absolutely wild! 🤯",
        f"Reddit never disappoints... This r/{subreddit_name} post is INSANE 🔥",
        f"Just found this gem on r/{subreddit_name}... 😱",
        f"When I read this on r/{subreddit_name}, my jaw dropped! 💯",
        f"This r/{subreddit_name} confession is something else... 🎭",
        f"Wait until you hear this r/{subreddit_name} story... 🍿",
        f"The internet is going crazy over this r/{subreddit_name} post! 📢",
        f"I can't stop thinking about this r/{subreddit_name} thread... 🤔",
        f"This might be the craziest r/{subreddit_name} story I've seen! 🚀",
        f"r/{subreddit_name} did it again with this one... 💀",
        f"You need to hear this r/{subreddit_name} confession! 🎬",
        f"This r/{subreddit_name} post has me shook! 😵",
        f"Reddit gold from r/{subreddit_name} right here! ⭐",
        f"I wasn't ready for this r/{subreddit_name} story... 🌊",
        f"The most unbelievable r/{subreddit_name} post you'll see today! 🎪",
        f"r/{subreddit_name} strikes again with this absolute BANGER! 💥",
        f"This r/{subreddit_name} thread is pure chaos... 🌪️",
        f"Just when you think you've seen it all on r/{subreddit_name}... 🎯",
        f"POV: You're scrolling r/{subreddit_name} and find THIS 📱",
        f"This r/{subreddit_name} user spilled ALL the tea! ☕",
        f"Warning: This r/{subreddit_name} story will blow your mind! ⚠️",
        f"The wildest r/{subreddit_name} confession of the year? 🏆",
        f"r/{subreddit_name} never misses and this proves it! 🎯",
        f"I had to share this r/{subreddit_name} story ASAP! ⚡",
        f"This r/{subreddit_name} post is going VIRAL for a reason! 📈",
        f"You're not going to believe what happened on r/{subreddit_name}... 🎢",
        f"Reddit user drops the most insane story on r/{subreddit_name}! 🎤",
        f"This r/{subreddit_name} tale is absolutely legendary! 👑",
        f"Breaking: r/{subreddit_name} just delivered another epic story! 📰",
        f"The comments on this r/{subreddit_name} post are GOLD! 💛",
        f"r/{subreddit_name} coming in hot with this story! 🔥🔥",
        f"This r/{subreddit_name} thread belongs in a museum! 🏛️",
        f"Everyone on r/{subreddit_name} is talking about this! 🗣️"
    ]
    
    # Expanded engagement prompts (30+ options)
    prompts = [
        "💬 What would YOU do in this situation? Share your thoughts below!",
        "👇 Drop your opinion in the comments - I'm curious what you think!",
        "💭 Let me know your take on this in the comments!",
        "🗣️ Comment your reaction - this one got me thinking!",
        "💬 What's your hot take? Tell me in the comments!",
        "👀 Am I the only one thinking this? Comment your thoughts!",
        "🤝 Team A or Team B? Let me know in the comments!",
        "💡 Share your perspective below - I want to hear it!",
        "🎤 Your turn! What do you think about this?",
        "📣 Sound off in the comments - what's your verdict?",
        "🔥 This is controversial! What side are you on?",
        "⬇️ Drop a comment and let's discuss this!",
        "💭 I need to know what you're thinking about this one!",
        "🗨️ Comment section is open - what's your story?",
        "👊 Hit me with your honest opinion below!",
        "🎯 What would you have done differently? Comment!",
        "💬 Let's debate this in the comments!",
        "🤔 Am I crazy or does this make sense? You tell me!",
        "📝 Write your thoughts in the comments - I'm reading!",
        "🌟 Share your similar experience below!",
        "💥 This one's wild! What's your reaction?",
        "🎭 How would you handle this? Comment now!",
        "⚡ Quick! First thought that came to mind - GO!",
        "🏃 Don't scroll past without commenting your take!",
        "💯 Rate this situation 1-10 in the comments!",
        "🔮 Predict what happens next in the comments!",
        "🎪 This story is nuts! What do you think?",
        "👑 Who's in the right here? Comment below!",
        "🌈 Everyone has a different opinion on this - what's yours?",
        "🎬 If this was a movie, how would it end? Comment!",
        "🚀 Your thoughts? Drop them below!",
        "💎 Comment your unpopular opinion on this!",
        "🎨 Paint me a picture - what would you do?",
        "⭐ Share your wisdom in the comments!",
        "🌊 Dive into the comments and share your story!"
    ]
    
    # Expanded CTAs (30+ options)
    ctas = [
        "👍 Like, 🔔 Subscribe & drop a comment if you enjoy Reddit stories!",
        "🔥 Smash that like button and subscribe for daily Reddit content!",
        "💙 If you loved this, hit subscribe for more Reddit shorts!",
        "⬆️ Subscribe and turn on notifications for more viral Reddit posts!",
        "🎯 Like & Subscribe if you want more crazy Reddit stories!",
        "✨ Don't forget to like and subscribe for your daily Reddit fix!",
        "🚀 Subscribe NOW for more mind-blowing Reddit content!",
        "💯 Hit that subscribe button for daily Reddit drama!",
        "🔔 Turn on ALL notifications so you never miss a story!",
        "⭐ Like this video and subscribe for more Reddit gold!",
        "🎪 Join the fam! Subscribe for wild Reddit stories daily!",
        "💥 Subscribe and help us hit [X] subscribers!",
        "👑 Become a subscriber and get your daily Reddit dose!",
        "🌟 Like, Subscribe, and share with someone who needs to see this!",
        "🎬 Subscribe for the best Reddit content on YouTube!",
        "⚡ Quick! Hit subscribe before you forget!",
        "🏆 Join [X] subscribers who love Reddit stories!",
        "💎 Subscribe for premium Reddit content every single day!",
        "🎯 Like if you enjoyed, Subscribe if you want more!",
        "🔥 Be part of the community - SUBSCRIBE NOW!",
        "📈 Help us grow! Like, Subscribe, and Comment!",
        "✅ Subscribe and let's build the best Reddit community together!",
        "🎊 Celebrate by hitting that subscribe button!",
        "💪 Show some love - Like & Subscribe!",
        "🌈 Subscribe for your daily dose of Reddit chaos!",
        "🎁 Gift yourself great content - Subscribe today!",
        "⚠️ Don't miss out! Subscribe for daily uploads!",
        "🔊 Subscribe and tell a friend about us!",
        "💝 Support the channel - Like, Subscribe, Share!",
        "🎮 Join the Reddit story squad - Subscribe!",
        "🍿 Grab some popcorn and subscribe for more!",
        "🚨 New videos daily! Subscribe to stay updated!",
        "🌍 Join our global community - Hit Subscribe!",
        "⏰ Never miss a video - Subscribe with notifications ON!",
        "🎉 Celebrating every new subscriber - Join us!"
    ]
    
    # Expanded link templates (25+ options)
    link_templates = [
        f"👉 Watch more Reddit Shorts: [Your Playlist Link Here]\n📌 Credit: Original post from r/{subreddit_name} on Reddit\n📲 Follow me on Reddit: u/YourRedditUsername",
        f"🔗 More stories like this: [Your Playlist Link Here]\n✅ Source: r/{subreddit_name}\n🌟 Join our community: u/YourRedditUsername",
        f"📺 Binge more Reddit content: [Your Playlist Link Here]\n🎯 Original thread: r/{subreddit_name}\n💫 Connect with me: u/YourRedditUsername",
        f"⚡ Full playlist here: [Your Playlist Link Here]\n📖 From the depths of r/{subreddit_name}\n🤝 Reddit fam: u/YourRedditUsername",
        f"🎬 Watch the full series: [Your Playlist Link Here]\n🔍 Found on: r/{subreddit_name}\n👥 Follow: u/YourRedditUsername",
        f"🌟 More epic stories: [Your Playlist Link Here]\n📍 Source: r/{subreddit_name}\n💬 Join the discussion: u/YourRedditUsername",
        f"🔥 Can't get enough? [Your Playlist Link Here]\n📚 Story from: r/{subreddit_name}\n🎯 Find me: u/YourRedditUsername",
        f"💎 Playlist of gems: [Your Playlist Link Here]\n🎭 Original post: r/{subreddit_name}\n✨ Reddit: u/YourRedditUsername",
        f"🚀 Explore more: [Your Playlist Link Here]\n📝 Credit to: r/{subreddit_name}\n🌊 Follow along: u/YourRedditUsername",
        f"⭐ Full collection: [Your Playlist Link Here]\n🏆 Posted on: r/{subreddit_name}\n💯 Connect: u/YourRedditUsername",
        f"🎪 Keep watching: [Your Playlist Link Here]\n📣 Courtesy of: r/{subreddit_name}\n🔔 Stay updated: u/YourRedditUsername",
        f"💥 More drama here: [Your Playlist Link Here]\n📌 Shoutout to: r/{subreddit_name}\n👋 Say hi: u/YourRedditUsername",
        f"🎯 Next video: [Your Playlist Link Here]\n🎁 Thanks to: r/{subreddit_name}\n🌈 Join me: u/YourRedditUsername",
        f"🔊 Playlist link: [Your Playlist Link Here]\n💡 Inspired by: r/{subreddit_name}\n🎊 Follow: u/YourRedditUsername",
        f"📱 See more: [Your Playlist Link Here]\n🌟 From: r/{subreddit_name}\n💝 Support: u/YourRedditUsername",
        f"🎬 Entire series: [Your Playlist Link Here]\n✏️ Story credit: r/{subreddit_name}\n🚀 Reddit profile: u/YourRedditUsername",
        f"🌍 Global playlist: [Your Playlist Link Here]\n📖 Source material: r/{subreddit_name}\n⚡ Quick link: u/YourRedditUsername",
        f"🎮 Gaming & more: [Your Playlist Link Here]\n🎤 Original by: r/{subreddit_name}\n🎨 Creative hub: u/YourRedditUsername",
        f"🍿 Binge-worthy content: [Your Playlist Link Here]\n🏅 Props to: r/{subreddit_name}\n🎭 Theatre: u/YourRedditUsername",
        f"📚 Story archive: [Your Playlist Link Here]\n🎯 Featuring: r/{subreddit_name}\n🌟 Main page: u/YourRedditUsername",
        f"💫 Star content: [Your Playlist Link Here]\n🔥 Hot from: r/{subreddit_name}\n👑 Royal profile: u/YourRedditUsername",
        f"🎊 Party playlist: [Your Playlist Link Here]\n💬 Discussed on: r/{subreddit_name}\n🎉 Celebrate: u/YourRedditUsername",
        f"🏆 Award-worthy: [Your Playlist Link Here]\n📣 Announced at: r/{subreddit_name}\n💪 Power user: u/YourRedditUsername",
        f"⚠️ Must-watch: [Your Playlist Link Here]\n🌊 Surfaced from: r/{subreddit_name}\n🔱 Trident: u/YourRedditUsername",
        f"🎁 Gift of content: [Your Playlist Link Here]\n💎 Mined from: r/{subreddit_name}\n🌈 Rainbow road: u/YourRedditUsername",
        f"🚨 Alert! More here: [Your Playlist Link Here]\n📰 Breaking from: r/{subreddit_name}\n📡 Broadcast: u/YourRedditUsername"
    ]
    
    # Randomly select components
    hook = random.choice(hooks)
    summary = f"{subreddit_title.strip()}"
    hashtags = "#Shorts #RedditShorts #" + subreddit_name
    prompt = random.choice(prompts)
    cta = random.choice(ctas)
    links = random.choice(link_templates)
    
    # Final description formatted
    description = f"""{hook}

{summary}

{prompt}

{cta}

{hashtags}

---
{links}
"""
    
    return description.strip()

if __name__ == "__main__":
    # Load config
    log_message("Loading configuration...", "info")
    config = toml.load("config.toml")

    videos_folder = r"C:\\Users\\martv\\Documents\\GitHub\\RedditVideoMakerBot\\results\\ask+AskReddit"
    videos_folders = []
    for dir in os.listdir(os.path.join(os.getcwd(), 'results')):
        videos_folders.append(os.path.join(os.getcwd(), 'results', dir))
    print(videos_folders)
    video_tags = config["video"]["tags"]
    status_made_for_kids = config["video"].get("made_for_kids", False)
    
    # Get manga title from config if available
    title = config["video"].get("title", "New Video")

    youtube = authenticate_youtube()

    videos = []
    # Get all video files from the folder
    for folder in videos_folders:
        for v in os.listdir(folder):
            if v.endswith((".mp4", ".mov", ".avi")):
                videos.append(os.path.join(folder, v))
    print(videos)
    if not videos:
        log_message("No videos found in the specified folder.", "warning")
        exit(0)
    
    log_message(f"Found {len(videos)} video(s) for upload.", "info")
    
    # Process each video
    for video in videos:
        video_path = video
        
        # Generate title - use filename without extension if no manga title in config
        temp_title = os.path.splitext(video)[0]
        video_title = temp_title if len(temp_title) <= 100 else title
        log_message(f"Preparing to upload: {video_title}", "info")
        # Upload the video
        success, video_id = upload_video(
            youtube,
            video_title,
            generate_youtube_description(video_title),
            video_tags,
            status_made_for_kids,
            video_path
        )
        
        # If upload was successful, delete the file
        if success:
            try:
                os.remove(video_path)
                log_message(f"Successfully deleted: {video_path}", "success")
            except Exception as e:
                log_message(f"Error deleting {video_path}: {e}", "error")
        else:
            log_message(f"Skipping deletion of {video_path} due to failed upload", "warning")
            
    log_message("Processing complete!", "success")