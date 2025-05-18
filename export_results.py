from pyairtable import Table
import csv

AIRTABLE_API_KEY = "your_airtable_api_key"
BASE_ID = "your_airtable_base_id"
TABLE_NAME = "Profiles"

table = Table(AIRTABLE_API_KEY, BASE_ID, TABLE_NAME)

with open("classified_profiles.csv", newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            table.create({
                "Username": row["Username"],
                "Name": row["Name"],
                "Bio": row["Bio"],
                "WhatsApp": row["WhatsApp Number"],
                "Group Link": row["Group Link"],
                "Type": row["Type"],
                "Region": row["Region"],
                "Followers": row["Followers"],
                "Profile URL": row["Profile URL"],
                "External Link": row["External Link"]
            })
        except Exception as e:
            print(f"❌ Failed to export {row['Username']}: {e}")

print("✅ Exported to Airtable")
