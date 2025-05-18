import yaml

def load_seed_usernames():
    with open ("config.yaml", "r") as file:
        config = yaml.safe_load(file)
        return config.get("seed_usernames", [])
    

if __name__ == "__main__":
    seeds = load_seed_usernames()
    print("\nSEED USERNAMES:")
    for username in seeds:
        print(f"- {username}")