import os
import pandas as pd
from config import SHROOM_CONTRACT, SPORE_CONTRACT, SHROOM_AIRDROP_POOL, SPORE_AIRDROP_POOL

def process_csv(csv_file, total_pool):
    """
    Reads a CSV file, converts the 'percentage' column to a decimal,
    and calculates the airdrop amount = percentage * total_pool.
    
    The CSV must contain:
      - 'percentage': the percentage holding (e.g., "44%" or "44")
      - 'address': the token holder's address
      
    For example, "44%" or "44" becomes 0.44, and then 0.44 * total_pool.
    """
    df = pd.read_csv(csv_file)
    # Normalize column names to lowercase.
    df.columns = [col.lower() for col in df.columns]
    
    # Ensure required columns exist.
    if 'percentage' not in df.columns:
        raise KeyError("CSV must contain a 'percentage' column.")
    if 'address' not in df.columns:
        raise KeyError("CSV must contain an 'address' column.")
    
    # Remove any '%' symbol and convert the percentage to a decimal.
    df['percentage'] = df['percentage'].astype(str).str.replace('%', '').astype(float) / 100.0
    
    # Calculate the airdrop amount and round to the nearest integer.
    df['airdrop'] = (df['percentage'] * total_pool).round().astype(int)
    return df

def format_for_safewallet(df, token_contract):
    """
    Creates a DataFrame with the required output columns for safewallet:
      - token_type: always "ERC20"
      - token_address: the token's contract address (from config)
      - receiver: the token holder's address
      - amount: the calculated airdrop amount
      
    Returns the formatted DataFrame.
    """
    out_df = pd.DataFrame()
    out_df['receiver'] = df['address']
    out_df['amount'] = df['airdrop']
    out_df['token_type'] = 'ERC20'
    out_df['token_address'] = token_contract
    # Reorder columns.
    return out_df[['token_type', 'token_address', 'receiver', 'amount']]

def get_unique_filename(base_name, extension=".csv"):
    """
    Returns a unique filename by appending an increasing number.
    For example, if Airdrop_1.csv exists, it will try Airdrop_2.csv, etc.
    """
    counter = 1
    while True:
        filename = f"{base_name}_{counter}{extension}"
        if not os.path.exists(filename):
            return filename
        counter += 1

def main():
    """
    Main function to process token holder CSV files and generate the final airdrop CSV.
    
    Steps:
      1. Process the 'shroom_holders.csv' using the SHROOM_AIRDROP_POOL.
      2. Process the 'spore_holders.csv' using the SPORE_AIRDROP_POOL.
      3. Format the output for safewallet (with columns: token_type, token_address, receiver, amount).
      4. Combine the outputs and save to a unique file (e.g., Airdrop_1.csv).
    """
    # Process the Shrooms CSV (pool = 7,000,000)
    shroom_df = process_csv("shroom_holders.csv", SHROOM_AIRDROP_POOL)
    # Process the Spores CSV (pool = 500,000,000)
    spore_df = process_csv("spore_holders.csv", SPORE_AIRDROP_POOL)
    
    # Format each output for safewallet.
    shroom_out = format_for_safewallet(shroom_df, SHROOM_CONTRACT)
    spore_out = format_for_safewallet(spore_df, SPORE_CONTRACT)
    
    # Combine both datasets.
    final_df = pd.concat([shroom_out, spore_out], ignore_index=True)
    
    # Generate a unique output filename (e.g., Airdrop_1.csv, Airdrop_2.csv, etc.)
    output_filename = get_unique_filename("Airdrop")
    
    # Save the final CSV.
    final_df.to_csv(output_filename, index=False)
    print(f"Final airdrop CSV generated: {output_filename}")

if __name__ == "__main__":
    main()
