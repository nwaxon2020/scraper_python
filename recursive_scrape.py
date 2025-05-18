import yaml
import time
from instaloader import Instaloader, Profile
from dotenv import load_dotenv
import os


USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

scrape_limit = config.get("scrape_limit", 500)
delay_seconds = config.get("delay_seconds", 2)
enable_recursion = config.get("enable_recursion", False)


scraped_set = set()
if os.path.exists("already_scraped.txt"):
    with open("already_scraped.txt", "r") as f:
        scraped_set = set(line.strip() for line in f.readlines())


with open("filtered_users.txt", "r") as file:
    usernames = [line.strip() for line in file.readlines() if line.strip() not in scraped_set]

if not enable_recursion:
    print("Recursion disabled in config.yaml")
    exit()

insta_loader = Instaloader()
insta_loader.login(USERNAME, PASSWORD)

new_queue = set()

print(f"\n🔁 Recursively scraping {len(usernames)} new seed users...\n")

for username in usernames:
    try:
        profile = Profile.from_username(insta_loader.context, username)
        count = 0

        print(f"\n Scraping followers/following for {username}...")

        for follower in profile.get_followers():
            if count >= scrape_limit:
                break
            new_queue.add(follower.username)
            count += 1
            time.sleep(delay_seconds)

        for followee in profile.get_followees():
            if count >= scrape_limit:
                break
            new_queue.add(followee.username)
            count += 1
            time.sleep(delay_seconds)

        scraped_set.add(username)

    except Exception as e:
        print(f"❌ Error scraping {username}: {e}")

# Save new users to file
with open("unique_users_recursive.txt", "w") as file:
    for user in new_queue:
        file.write(f"{user}\n")

# Update scraped log
with open("already_scraped.txt", "w") as file:
    for user in scraped_set:
        file.write(f"{user}\n")

print(f"\nRecursively scraped users saved to unique_users_recursive.txt")

