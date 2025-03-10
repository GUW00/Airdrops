import os
import pandas as pd
from config import KID_CONTRACT, SHROOM_CONTRACT, SPORE_CONTRACT

# Define the output directory
OUTPUT_DIR = "kid_shroom"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_unique_filename(prefix, ext=".csv"):
    """
    Generate a unique filename in the kid_shroom directory.
    Example: If Kid_Airdrop_Shrooms_1.csv exists, it will return Kid_Airdrop_Shrooms_2.csv, etc.
    """
    i = 1
    while os.path.exists(os.path.join(OUTPUT_DIR, f"{prefix}{i}{ext}")):
        i += 1
    return os.path.join(OUTPUT_DIR, f"{prefix}{i}{ext}")

# Read the kid_holders.csv file, expected to have columns: address, quantity
df = pd.read_csv("kid_holders.csv")

# Convert quantity to numeric; non-numeric values become NaN
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

# Drop rows where quantity is NaN (or you could fill them with 0 if that makes sense)
df = df.dropna(subset=["quantity"])

# Create the airdrop rows for Shrooms:
# - token_type is always "erc20"
# - token_address is SHROOM_CONTRACT from config
# - receiver is the address from the CSV
# - amount is quantity * 20,000 (rounded to nearest integer)
shrooms_df = pd.DataFrame({
    "token_type": "erc20",
    "token_address": SHROOM_CONTRACT,
    "receiver": df["address"],
    "amount": (df["quantity"] * 20000).round(0).astype(int)
})

# Create the airdrop rows for Spores:
# - token_type is always "erc20"
# - token_address is SPORE_CONTRACT from config
# - receiver is the address from the CSV
# - amount is quantity * 1,500,000 (rounded to nearest integer)
spores_df = pd.DataFrame({
    "token_type": "erc20",
    "token_address": SPORE_CONTRACT,
    "receiver": df["address"],
    "amount": (df["quantity"] * 1500000).round(0).astype(int)
})

# Generate unique output filenames for each file in kid_shroom folder
shrooms_filename = get_unique_filename("Kid_Airdrop_Shrooms_")
spores_filename = get_unique_filename("Kid_Airdrop_Spores_")

# Write the separate DataFrames to CSV inside kid_shroom
shrooms_df.to_csv(shrooms_filename, index=False)
spores_df.to_csv(spores_filename, index=False)

print(f"Kid Shrooms airdrop file created: {shrooms_filename}")
print(f"Kid Spores airdrop file created: {spores_filename}")
