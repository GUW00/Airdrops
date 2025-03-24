import os
import pandas as pd
from config import BRUH_CONTRACT, BRUH_ALL, BRUH_CURRENT, JIMMY

# Define input/output directory
INPUT_DIR = "Bruh"

# Ensure output folder exists
os.makedirs(INPUT_DIR, exist_ok=True)

# Addresses to omit (all lowercase)
OMIT_ADDRESSES = [
    "0xf23d3f41077ed564ed7b61de628afb2de549130d",  # explicitly omitted address
    "0x000000000000000000000000000000000000dead"
]

def get_unique_filename(prefix, ext=".csv"):
    """
    Generate a unique filename in the Bruh directory.
    For example, if Airdrop_Bruh_1.csv exists, returns Airdrop_Bruh_2.csv, etc.
    """
    i = 1
    while os.path.exists(os.path.join(INPUT_DIR, f"{prefix}{i}{ext}")):
        i += 1
    return os.path.join(INPUT_DIR, f"{prefix}{i}{ext}")

def rename_quantity_column(df, fname):
    """
    If the DataFrame does not have a 'quantity' column, then
    rename the non-'address' column to 'quantity'. This assumes that any numeric
    header (or the only header besides 'address') represents quantity.
    """
    if "quantity" not in df.columns:
        # Find candidate columns (all columns except 'address')
        candidates = [col for col in df.columns if col != "address"]
        # Prefer columns that are fully numeric in their name (e.g., "9")
        numeric_candidates = [col for col in candidates if col.isdigit()]
        if numeric_candidates:
            df = df.rename(columns={numeric_candidates[0]: "quantity"})
        elif len(candidates) == 1:
            df = df.rename(columns={candidates[0]: "quantity"})
        else:
            raise KeyError(f"CSV {fname} must contain 'address' and 'quantity' columns.")
    return df

def process_csv(csv_filename, total_pool):
    """
    Processes a single CSV file:
      - Reads the CSV from INPUT_DIR.
      - Normalizes column names and converts the 'quantity' column to numeric.
      - If no 'quantity' column is found, renames the candidate column to 'quantity'.
      - Omits blacklisted addresses.
      - Computes each address's airdrop as (quantity / total quantity) * total_pool.
      - Adjusts for any rounding difference so that the sum equals total_pool.
      - Removes any rows with an airdrop amount of 0.
      - Formats the DataFrame for SafeWallet with columns: token_type, token_address, receiver, amount.
    """
    file_path = os.path.join(INPUT_DIR, csv_filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    df = pd.read_csv(file_path)
    print(f"Detected columns in {csv_filename}: {df.columns.tolist()}")

    # Normalize column names: trim and lower-case them
    df.columns = [col.strip().lower() for col in df.columns]

    # If 'quantity' is missing, try to rename the candidate column to 'quantity'
    df = rename_quantity_column(df, csv_filename)

    if "address" not in df.columns or "quantity" not in df.columns:
        raise KeyError(f"CSV {csv_filename} must contain 'address' and 'quantity' columns.")

    # Convert quantity to numeric and fill NaN with 0
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
    # Normalize addresses to lowercase
    df["address"] = df["address"].str.lower()
    # Omit blacklisted addresses
    df = df[~df["address"].isin(OMIT_ADDRESSES)]

    total_quantity = df["quantity"].sum()
    if total_quantity <= 0:
        raise ValueError(f"Total quantity in {csv_filename} is zero or negative after omitting addresses.")

    # Calculate individual airdrop amounts
    df["airdrop"] = ((df["quantity"] / total_quantity) * total_pool).round().astype(int)
    # Adjust rounding difference to ensure sum equals total_pool
    difference = total_pool - df["airdrop"].sum()
    if difference != 0:
        df.loc[df.index[0], "airdrop"] += difference

    # Remove rows with airdrop amount of 0
    df = df[df["airdrop"] > 0]

    # Format output for SafeWallet
    return pd.DataFrame({
        "token_type": "erc20",
        "token_address": BRUH_CONTRACT,
        "receiver": df["address"],
        "amount": df["airdrop"]
    })

def process_combined_csv(filenames, total_pool):
    """
    Processes multiple CSV files (e.g. bruh_mono.csv and bruh_color.csv):
      - Reads each CSV from INPUT_DIR and processes them similarly to process_csv.
      - Concatenates the data from the provided filenames.
      - Computes the shared airdrop for the combined dataset using total_pool.
      - Adjusts for rounding differences.
      - Returns a formatted DataFrame.
    """
    dfs = []
    for fname in filenames:
        file_path = os.path.join(INPUT_DIR, fname)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        df = pd.read_csv(file_path)
        print(f"Detected columns in {fname}: {df.columns.tolist()}")
        df.columns = [col.strip().lower() for col in df.columns]
        df = rename_quantity_column(df, fname)
        if "address" not in df.columns or "quantity" not in df.columns:
            raise KeyError(f"CSV {fname} must contain 'address' and 'quantity' columns.")
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
        df["address"] = df["address"].str.lower()
        df = df[~df["address"].isin(OMIT_ADDRESSES)]
        dfs.append(df)
    
    combined = pd.concat(dfs, ignore_index=True)
    total_quantity = combined["quantity"].sum()
    if total_quantity <= 0:
        raise ValueError("Total quantity in combined CSVs is zero or negative after omitting addresses.")

    combined["airdrop"] = ((combined["quantity"] / total_quantity) * total_pool).round().astype(int)
    difference = total_pool - combined["airdrop"].sum()
    if difference != 0:
        combined.loc[combined.index[0], "airdrop"] += difference

    combined = combined[combined["airdrop"] > 0]

    return pd.DataFrame({
        "token_type": "erc20",
        "token_address": BRUH_CONTRACT,
        "receiver": combined["address"],
        "amount": combined["airdrop"]
    })

def main():
    """
    Main processing function:
      - Processes BRUH_ALL from 'bruh_all.csv' with a 100,000 pool.
      - Processes BRUH_CURRENT from a combination of 'bruh_mono.csv' and 'bruh_color.csv' with a 100,000 pool.
      - Processes JIMMY from 'jimmy.csv' with a 25,000 pool.
      - Merges all results and writes to a uniquely named CSV file in the Bruh directory.
    """
    # Process BRUH_ALL airdrop
    bruh_all_df = process_csv("bruh_all.csv", BRUH_ALL)
    
    # Process BRUH_CURRENT airdrop (combined from bruh_mono.csv and bruh_color.csv)
    bruh_current_df = process_combined_csv(["bruh_mono.csv", "bruh_color.csv"], BRUH_CURRENT)
    
    # Process JIMMY airdrop from jimmy.csv
    jimmy_df = process_csv("jimmy.csv", JIMMY)
    
    # Merge all airdrops into one DataFrame
    final_df = pd.concat([bruh_all_df, bruh_current_df, jimmy_df], ignore_index=True)
    
    output_filename = get_unique_filename("Airdrop_Bruh_")
    final_df.to_csv(output_filename, index=False)
    print(f"Final BRUH airdrop file created: {output_filename}")

if __name__ == "__main__":
    main()
