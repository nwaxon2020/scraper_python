import yaml
import time
from instaloader import Instaloader, Profile
from dotenv import load_dotenv
import os


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

seed_usernames = config.get("seed_usernames", [])
scrape_limit = config.get("scrape_limit", 500)
delay_seconds = config.get("delay_seconds", 2)

load_dotenv()
USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

insta_loader = Instaloader()
#insta_loader.login(USERNAME, PASSWORD)

unique_queue = set()

for username in seed_usernames:
    try:
        profile = Profile.from_username(insta_loader.context, username)
       
        count = 0

        print("\n✔✔ -- Getting Followers ❤❤...")
        for follower in profile.get_followers():
            if count >= scrape_limit:
                break
            unique_queue.add(follower.username)
            count += 1
            time.sleep(delay_seconds)
        
        print("\n✔✔ -- Getting Following 👍👍...")
        for following in profile.get_followees():
            if count >= scrape_limit:
                break
            unique_queue.add(following.username)
            count += 1
            time.sleep(delay_seconds)

    except Exception as e:
        print(f"❌ There was an error scrapping {username}: {e}")


with open ("unique_users.txt", "w") as file:
    for user in unique_queue:
        file.write(f"{user}\n")


print(f"Total unique_users: {len(unique_queue)}")
print("File Saved to unique_users.txt")