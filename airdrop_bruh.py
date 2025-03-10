import os
import pandas as pd
from config import BRUH_CONTRACT, BRUH_HOLDERS, BRUH_CURRENT

# Define correct input/output directory
INPUT_DIR = "Bruh"

# Ensure output folder exists
os.makedirs(INPUT_DIR, exist_ok=True)

# Addresses to omit
OMIT_ADDRESSES = [
    "0xF23D3f41077Ed564ED7B61de628afb2dE549130D".lower(),
    "0x000000000000000000000000000000000000dEaD".lower()
]

def get_unique_filename(prefix, ext=".csv"):
    """
    Generate a unique filename in the Bruh directory.
    Example: If Airdrop_Bruh_1.csv exists, it will return Airdrop_Bruh_2.csv, etc.
    """
    i = 1
    while os.path.exists(os.path.join(INPUT_DIR, f"{prefix}{i}{ext}")):
        i += 1
    return os.path.join(INPUT_DIR, f"{prefix}{i}{ext}")

def process_csv(csv_filename, total_pool):
    """
    Reads a CSV file, ensures 'quantity' column is valid, omits blacklisted addresses,
    and calculates the airdrop amount for each address.

    - token_type is always "erc20"
    - token_address is BRUH_CONTRACT
    - receiver is the address from the CSV
    - amount is calculated as: (quantity / total quantity) * total_pool
    
    Returns a formatted DataFrame.
    """
    file_path = os.path.join(INPUT_DIR, csv_filename)

    # Ensure file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    # Read the CSV file
    df = pd.read_csv(file_path)

    # Debug: Print detected column names
    print(f"Detected columns in {csv_filename}: {df.columns.tolist()}")

    # Normalize column names
    df.columns = [col.strip().lower() for col in df.columns]

    # Ensure required columns exist
    if "quantity" not in df.columns or "address" not in df.columns:
        raise KeyError(f"CSV {csv_filename} must contain 'address' and 'quantity' columns.")

    # Convert quantity to numeric, drop NaN values
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)

    # Convert addresses to lowercase for comparison
    df["address"] = df["address"].str.lower()

    # Omit blacklisted addresses
    df = df[~df["address"].isin(OMIT_ADDRESSES)]

    # Compute total quantity sum
    total_quantity = df["quantity"].sum()

    if total_quantity <= 0:
        raise ValueError(f"Total quantity in {csv_filename} is zero or negative after omitting addresses. Check your data.")

    # Compute individual airdrop amounts
    df["airdrop"] = ((df["quantity"] / total_quantity) * total_pool).round().astype(int)

    # Adjust rounding difference to ensure total matches exactly
    difference = total_pool - df["airdrop"].sum()
    if difference != 0:
        df.loc[df.index[0], "airdrop"] += difference

    # Remove rows where airdrop amount is 0
    df = df[df["airdrop"] > 0]

    # Format output for SafeWallet
    airdrop_df = pd.DataFrame({
        "token_type": "erc20",
        "token_address": BRUH_CONTRACT,
        "receiver": df["address"],
        "amount": df["airdrop"]
    })

    return airdrop_df

def main():
    """
    Processes BRUH airdrop from bruh_holders.csv and bruh_current.csv,
    then merges both datasets into a **single** airdrop CSV inside Bruh/.
    """
    # Process BRUH holders airdrop
    bruh_holders_df = process_csv("bruh_holders.csv", BRUH_HOLDERS)

    # Process BRUH current holders airdrop
    bruh_current_df = process_csv("bruh_current.csv", BRUH_CURRENT)

    # Merge both airdrops into one DataFrame
    final_df = pd.concat([bruh_holders_df, bruh_current_df], ignore_index=True)

    # Generate unique filename for the combined airdrop file
    output_filename = get_unique_filename("Airdrop_Bruh_")

    # Save the final merged airdrop CSV
    final_df.to_csv(output_filename, index=False)

    print(f"Final BRUH airdrop file created: {output_filename}")

if __name__ == "__main__":
    main()
