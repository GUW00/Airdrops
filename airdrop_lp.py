import os
import pandas as pd
from config import SHROOM_CONTRACT, SPORE_CONTRACT, SHROOM_AIRDROP_POOL, SPORE_AIRDROP_POOL

# Define output directory for the final CSV (remains "LP")
OUTPUT_DIR = "LP"

# Ensure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_unique_filename(prefix, ext=".csv"):
    """
    Generate a unique filename in the LP directory.
    Example: If Airdrop_LP_1.csv exists, it will return Airdrop_LP_2.csv, etc.
    """
    i = 1
    while os.path.exists(os.path.join(OUTPUT_DIR, f"{prefix}{i}{ext}")):
        i += 1
    return os.path.join(OUTPUT_DIR, f"{prefix}{i}{ext}")

def process_csv(csv_file, total_pool):
    """
    Reads a CSV file, converts the 'percentage' column to a decimal,
    and calculates the airdrop amount = percentage * total_pool.
    
    The CSV must contain:
      - 'percentage': the percentage holding (e.g., "44%" or "44")
      - 'address': the token holder's address.
      
    Rows with unwanted addresses or airdrop amounts 0 or less are omitted.
    """
    df = pd.read_csv(csv_file)
    
    # Normalize column names to lowercase.
    df.columns = [col.lower() for col in df.columns]

    # Ensure required columns exist.
    if 'percentage' not in df.columns:
        raise KeyError(f"CSV {csv_file} must contain a 'percentage' column.")
    if 'address' not in df.columns:
        raise KeyError(f"CSV {csv_file} must contain an 'address' column.")

    # Omit unwanted addresses (ignoring case).
    omit_addresses = [
        "0x0000000000000000000000000000000000000000",
        "0x44574D53474729F2949a7eCfb68b0641cFDA4aA8"
    ]
    df = df[~df['address'].str.lower().isin([addr.lower() for addr in omit_addresses])]

    # Remove any '%' symbol and convert the percentage to a decimal.
    df['percentage'] = df['percentage'].astype(str).str.replace('%', '').astype(float) / 100.0

    # Calculate the airdrop amount and round to the nearest integer.
    df['airdrop'] = (df['percentage'] * total_pool).round().astype(int)

    # Omit any addresses with airdrop 0 or less.
    df = df[df['airdrop'] > 0]

    return df

def format_for_safewallet(df, token_contract):
    """
    Creates a DataFrame with the required output columns for SafeWallet:
      - token_type: always "erc20"
      - token_address: the token's contract address (from config)
      - receiver: the token holder's address
      - amount: the calculated airdrop amount.
    """
    return pd.DataFrame({
        "token_type": "erc20",
        "token_address": token_contract,
        "receiver": df["address"],
        "amount": df["airdrop"]
    })

def main():
    """
    Processes LP airdrops for SHROOM and SPORE liquidity providers and saves them in LP/.
    """
    # Update file paths to point to the correct location.
    # Since the script is run from D:\Github\Smart-Contracts\Airdrop,
    # and the CSVs are in the LP folder within that directory, use "LP".
    base_path = "LP"
    shroom_csv_path = os.path.join(base_path, "shroom_holders.csv")
    spore_csv_path = os.path.join(base_path, "spore_holders.csv")
    
    # Process the Shrooms LP CSV (pool = 7,000,000)
    shroom_df = process_csv(shroom_csv_path, SHROOM_AIRDROP_POOL)
    # Adjust Shrooms amounts to exactly match the pool.
    diff_shroom = SHROOM_AIRDROP_POOL - shroom_df['airdrop'].sum()
    if diff_shroom != 0:
        shroom_df.loc[shroom_df.index[0], 'airdrop'] += diff_shroom

    # Process the Spores LP CSV (pool = 500,000,000)
    spore_df = process_csv(spore_csv_path, SPORE_AIRDROP_POOL)
    # Adjust Spores amounts to exactly match the pool.
    diff_spore = SPORE_AIRDROP_POOL - spore_df['airdrop'].sum()
    if diff_spore != 0:
        spore_df.loc[spore_df.index[0], 'airdrop'] += diff_spore

    # Format each output for SafeWallet.
    shroom_out = format_for_safewallet(shroom_df, SHROOM_CONTRACT)
    spore_out = format_for_safewallet(spore_df, SPORE_CONTRACT)

    # Combine both datasets.
    final_df = pd.concat([shroom_out, spore_out], ignore_index=True)

    # Generate a unique output filename (e.g., LP/Airdrop_LP_1.csv).
    output_filename = get_unique_filename("Airdrop_LP_")

    # Save the final CSV inside LP.
    final_df.to_csv(output_filename, index=False)

    print(f"Final LP airdrop file created: {output_filename}")

if __name__ == "__main__":
    main()
