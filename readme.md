# **Airdrop Processing Tool**

This tool processes manually downloaded CSV files containing token holder data and calculates each holder’s airdrop amount based on their percentage holding. It supports two tokens (e.g., Shrooms and Spores) with fixed total pools (7,000,000 for Shrooms and 500,000,000 for Spores). The tool outputs a CSV file formatted for safewallet with the following columns: token\_type, token\_address, reciever, amount. The output file is automatically given a unique name (e.g., Airdrop\_1.csv, Airdrop\_2.csv, etc.) so that no file is overwritten.

## **File Structure**

Your project folder should contain the following files:

project-folder/  
├── .env  
├── config.py  
├── airdrop\_weekly.py 
├── airdrop\_monthly.py 
└── README.md   \<-- (this guide)

## **File Descriptions**

### **1\. .env**

This file holds your configuration settings and sensitive data. Create a file named .env in your project folder with the following content (update the values as needed):

POLYSCAN\_API\_KEY=YOUR\_API\_KEY GOES HERE

### **2\. config.py**

This file loads your configuration settings from the .env file. Copy and paste the following code into config.py:

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

* address: The token holder’s address.  
* percentage: The percentage holding (e.g., "44%" or "44").

**The script does the following:**

* Converts the percentage values to decimals (e.g., "44%" becomes 0.44).  
* Calculate the airdrop amount for each address using the total pool (7,000,000 for Shrooms and 500,000,000 for Spores).  
* Rounds the result to the nearest integer.  
* Formats the output with columns: token\_type (always "ERC20"), token\_address (from config), receiver, and amount.  
* Saves the combined output to a uniquely named file (e.g., Airdrop\_1.csv, Airdrop\_2.csv, etc.) so that no file is overwritten.

## **Setting Up Your Project (For VS and Python Beginners)**

1. Install Python  
   • Download the latest version (3.8 or above) from python.org.  
   • Run the installer and check “Add Python to PATH” during installation.  
2. Install Visual Studio Code (Optional but Recommended)  
   • Download VS Code from code.visualstudio.com and install it.  
   • Install the official Python extension by Microsoft via the Extensions view (Ctrl+Shift+X).  
3. Set Up Your Project  
   • Clone or download the repository (e.g., from GitHub: [https://github.com/GUW00/Airdrops](https://github.com/GUW00/Airdrops)).  
   • Open the project folder in VS Code.  
4. (Optional) Create a Virtual Environment  
   • Open the terminal in your project folder and run:  
   python \-m venv venv  
   • Activate the virtual environment: \- Windows: venv\\Scripts\\activate  
   \- MacOS/Linux: source venv/bin/activate  
5. Install Required Python Packages  
   • In the terminal, run:  
   pip install pandas python-dotenv  
6. Configure Your Project  
   • Verify the settings in config.py (contract addresses, total pool values, etc.).  
   • Ensure you have the required input CSV files (see next section).

---

## **How to Use the Tool**

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

**• Percentage Format:**

* The script removes any "%" symbol and divides the value by 100\. Ensure your CSV percentage values are properly formatted.

**• Column Names:**

* The script converts column names to lowercase. If your CSV uses different column names, update the script accordingly.

**• Unique Filenames:**

* The output file uses a function (get\_unique\_filename) to ensure that each generated file has a unique name.

**• Dependencies:**

* Make sure you have installed the necessary packages (pandas and python-dotenv).

