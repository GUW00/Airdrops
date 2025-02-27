# **Airdrop Processing Tool**

This tool processes manually downloaded CSV files containing token holder data and calculates each holder’s airdrop amount based on their percentage holding. It supports two tokens (e.g., Shrooms and Spores) with fixed total pools (7,000,000 for Shrooms and 500,000,000 for Spores). The tool outputs a CSV file formatted for safewallet with the following columns: `token_type, token_address, reciever, amount`. The output file is automatically given a unique name (e.g., `Airdrop_1.csv`, `Airdrop_2.csv`, etc.) so that no file is overwritten.

## **File Structure**

Your project folder should contain the following files:

project-folder/  
├── .env  
├── config.py  
├── process\_airdrop.py  
└── README.md   \<-- (this guide)

## **File Descriptions**

### **1\. `.env`**

This file holds your configuration settings and sensitive data. Create a file named `.env` in your project folder with the following content (update the values as needed):

POLYSCAN\_API\_KEY=YOUR\_API\_KEY GOES HERE

### **2\. `config.py`**

This file loads your configuration settings from the `.env` file. Copy and paste the following code into `config.py`:

import os  
from dotenv import load\_dotenv

load\_dotenv()

POLYSCAN\_API\_KEY \= os.getenv("POLYSCAN\_API\_KEY")  
SHROOM\_LP=0x28DEf03d8DC0d186FaBAe9C46043e8eF9BfFCc28 SPORE\_LP=0x2a91571238303c6700A9336342c754e159243168 SHROOM\_CONTRACT=0xF3ABaa9eA255d38763A5D0Ae6286d6df53154dDC SPORE\_CONTRACT=0x089582AC20ea563c69408a79E1061de594b61bED SHROOM\_AIRDROP\_POOL=7000000 SPORE\_AIRDROP\_POOL=500000000

**Note:**

* `SHROOM_CONTRACT` and `SPORE_CONTRACT` are the actual token contract addresses.  
* `SRHOOM_LP` and `SPORE_LP` are the LP addresses (if needed).  
* `SHROOM_AIRDROP_POOL` is the total amount of Shrooms to distribute.  
* `SPORE_AIRDROP_POOL` is the total amount of Spores to distribute.  
* You can add additional tokens, remember to update **process\_airdrop.py**

### **3\. `process_airdrop.py`**

**This script processes your manually downloaded CSV files. It assumes the CSV files have at least two columns:**

* **address: The token holder’s address.**  
* **percentage: The percentage holding (e.g., "44%" or "44").**

**The script does the following:**

* **Converts the `percentage` values to decimals (e.g., "44%" becomes 0.44).**  
* **Calculate the airdrop amount for each address using the total pool (7,000,000 for Shrooms and 500,000,000 for Spores).**  
* **Rounds the result to the nearest integer.**  
* **Formats the output with columns: `token_type` (always "ERC20"), `token_address` (from config), `receiver`, and `amount`.**  
* **Saves the combined output to a uniquely named file (e.g., `Airdrop_1.csv`, `Airdrop_2.csv`, etc.) so that no file is overwritten.**

## **How to Use**

1. **Download Your CSV Files**  
   * **Obtain your token holder data for Shrooms and Spores (for example, from Polygonscan).**  
   * **Save the files as:**  
     * **`shroom_holders.csv`**  
     * **`spore_holders.csv`**  
   * **Ensure that each CSV contains an `address` column and a `percentage` column.**  
     * **The `percentage` column should contain values like "44%" or "44".**  
2. **Run the Tool**  
   **Open your terminal in the project directory and run: (I use VisualStudios)**  
   	**python process\_airdrop.py**

**The script will:**

* **Process each CSV file.**  
* **Convert percentage values to decimals (e.g., "44%" → 0.44).**  
* **Multiply by the total pool (7,000,000 for Shrooms or 500,000,000 for Spores) and round the result.**  
* **Format the output for SafeWallet.**  
* **Save the final output to a uniquely named file (e.g., `Airdrop_1.csv`).**  
  **If `Airdrop_1.csv` already exists, it will create `Airdrop_2.csv`, and so on.**

**Review the Output**  
**Open the generated CSV file (e.g., `Airdrop_1.csv`) to verify the results.**  
**Each row will display:**

* **`token_type`: "ERC20"**  
* **`token_address`: The contract address from your config.**  
* **`receiver`: The holder's address.**  
* **`amount`: The calculated airdrop amount (e.g., for a holder with 44% of Shrooms: 0.44 \* 7,000,000 ≈ 3,080,000).**

## **Customization & Troubleshooting**

* **Percentage Format:**  
  **The script strips the `%` symbol (if present) and divides the value by 100\. Ensure your CSV is formatted correctly.**  
* **Column Names:**  
  **Column names are converted to lowercase. If your CSV uses different column names, update the script accordingly.**  
* **Unique Filenames:**  
  **The output file is automatically given a unique name using the `get_unique_filename` function.**  
* **Dependencies:**  
  **Ensure you have installed `pandas` and `python-dotenv` using pip.**




