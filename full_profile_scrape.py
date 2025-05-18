import re
import time
from instaloader import Instaloader, Profile
from dotenv import load_dotenv
import os


load_dotenv()
USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")


insta_loader = Instaloader()
insta_loader.login(USERNAME, PASSWORD)


with open("filtered_users.txt", "r") as file:
    usernames = [line.strip() for line in file.readlines()]


whatsapp_pattern = re.compile(r"(\+?\d{1,4}[-.\s]?\(?\d+\)?[-.\s]?\d+[-.\s]?\d+)")
group_link_pattern = re.compile(r"(chat\.whatsapp\.com\/[A-Za-z0-9]+)")

results = []

for username in usernames:
    try:
        profile = Profile.from_username(insta_loader.context, username)

        bio = profile.biography or ""
        full_name = profile.full_name or ""
        external_url = profile.external_url or ""
        followers = profile.followers
        profile_url = f"https://instagram.com/{username}"

      
        combined_text = f"{bio} {external_url}"

       
        whatsapp_numbers = whatsapp_pattern.findall(combined_text)
        group_links = group_link_pattern.findall(combined_text)

        results.append({
            "username": username,
            "full_name": full_name,
            "bio": bio,
            "external_url": external_url,
            "followers": followers,
            "profile_url": profile_url,
            "whatsapp_numbers": whatsapp_numbers,
            "group_links": group_links
        })

        print(f"Scraped {username}: {len(whatsapp_numbers)} WhatsApp numbers, {len(group_links)} group links")

        time.sleep(2)  # delay to avoid hitting rate limits

    except Exception as e:
        print(f"❌ Error scraping {username}: {e}")

# Save results to CSV
import csv

keys = results[0].keys() if results else []
with open("full_profile_data.csv", "w", newline="", encoding="utf-8") as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)

print(f"\nScraping done! {len(results)} profiles saved to full_profile_data.csv")
