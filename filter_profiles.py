import yaml
import time
from instaloader import Instaloader, Profile
from dotenv import load_dotenv
import os


load_dotenv()
USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

scrape_limit = config.get("scrape_limit", 500)
delay_seconds = config.get("delay_seconds", 2)


with open("unique_users.txt", "r") as file:
    usernames = [line.strip() for line in file.readlines()]


cellphone_keywords = [
    "celular", "iphone", "samsung", "gsm", "reparacion", "reparação", "accesorios",
    "pantalla", "movil", "telefone", "funda", "carregador", "telemóvel", "telefono", "acessórios"
]
language_keywords = ["de", "para", "loja", "tienda", "con", "serviço", "equipos", "vendemos"]

insta_loader = Instaloader()

filtered_users = []

print("\n🔍 Filtering relevant users...")

for username in usernames:
    try:
        profile = Profile.from_username(insta_loader.context, username)
        bio = profile.biography.lower()
        full_name = profile.full_name.lower()
        external_url = profile.external_url or ""

        combined_text = f"{bio} {full_name}"

        if any(kw in combined_text for kw in cellphone_keywords) and any(lang_kw in combined_text for lang_kw in language_keywords):
            filtered_users.append(username)
            print(f"{username} passed the filter")
        
        time.sleep(delay_seconds)

    except Exception as e:
        print(f"❌ Error checking {username}: {e}")


with open("filtered_users.txt", "w") as file:
    for user in filtered_users:
        file.write(f"{user}\n")

print(f"\nTotal filtered users: {len(filtered_users)}")
print("Filtered list saved to filtered_users.txt")
