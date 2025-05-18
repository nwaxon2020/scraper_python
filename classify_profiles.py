import csv

# Define keywords for each business type
CLASSIFICATION_KEYWORDS = {
    "Retailer": ["venta", "vendemos", "loja", "tienda", "store", "oferta"],
    "Reseller": ["mayoreo", "revendedor", "reseller", "por mayor"],
    "Distributor": ["distribuidor", "distribuidora", "wholesale", "importador"],
    "Repair Shop": ["reparacion", "repair", "tecnico", "servicio técnico", "arreglamos"]
}

def classify_user(text):
    text = text.lower()
    for category, keywords in CLASSIFICATION_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category
    return "Unknown"

# Read full scraped profiles
with open("full_scraped_profiles.csv", newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)

# Classify and add a new column
for row in rows:
    combined_text = f"{row['Name']} {row['Bio']}"
    row["Type"] = classify_user(combined_text)

# Write updated data to new CSV
fieldnames = rows[0].keys()
with open("classified_profiles.csv", "w", newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("✅ Classified profiles saved to classified_profiles.csv")
