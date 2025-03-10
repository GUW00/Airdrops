Airdrop Processing Tool - Quick Start Guide
This tool automates the processing of manually downloaded CSV files containing token holder data.
It calculates each holder’s airdrop amount based on their percentage holding or fixed allocations.
The tool supports Shrooms, Spores, and BRUH token airdrops and ensures that each output file
is formatted for SafeWallet.

✅ Supports weekly, monthly, and liquidity pool (LP) airdrops
✅ Automatically assigns a unique filename to prevent overwriting
✅ Ensures airdrop amounts match exactly with the allocated total pools
✅ Excludes unwanted or zero-value addresses from the final CSV

How to Use This Tool
Follow these simple steps to run the airdrop scripts:

1. Install Python
Download the latest version of Python 3.8+ from https://www.python.org
During installation, check "Add Python to PATH".
2. Set Up Your Project
Clone or download the repository from GitHub.
Navigate to the project folder.
3. Install Dependencies
Install the required Python packages:

pip install pandas python-dotenv

4. Configure Your .env File
Create a .env file in the project folder and add the following:

5. Update Your config.py
Ensure config.py contains the correct contract addresses and pool allocations:

SHROOM_LP = "0x28DEf03d8DC0d186FaBAe9C46043e8eF9BfFCc28"
SPORE_LP = "0x2a91571238303c6700A9336342c754e159243168"
SHROOM_CONTRACT = "0x924B16Dfb993EEdEcc91c6D08b831e94135dEaE1"
SPORE_CONTRACT = "0x089582AC20ea563c69408a79E1061de594b61bED"
KID_CONTRACT = "0x9c92B882aC7aeff58414D874de60d30381991BaD"
SHROOM_AIRDROP_POOL = 7000000
SPORE_AIRDROP_POOL = 500000000
BRUH_CONTRACT = "0xa52410B8b3Ce16d3f0E607ce8f86b3b4AC30fE2F"
BRUH_HOLDERS = 125000
BRUH_CURRENT = 125000

File Structure
Your project folder should look like this:

Airdrops/
├── .env
├── config.py
├── airdrop_kid.py
├── airdrop_bruh.py
├── airdrop_lp.py
├── kid_shroom/ (Contains Kid Shroom Airdrop files)
├── LP/ (Contains LP Airdrop files)
├── Bruh/ (Contains Bruh Airdrop files)
└── README.txt (this guide)

Running the Airdrop Scripts
Each script processes manually downloaded CSV files and outputs a SafeWallet-formatted CSV file.

1. Weekly Airdrop
Processes shroom_holders.csv and spore_holders.csv, distributing tokens based on percentage holdings.

Download the Shroom LP Holders and rename it to shroom.holders.csv
https://polygonscan.com/token/0x28def03d8dc0d186fabae9c46043e8ef9bffcc28#balances

Download the SPORER LP Holders and rename it to spore.holders.csv
https://polygonscan.com/token/0x2a91571238303c6700a9336342c754e159243168#balances

Output:
Airdrop_X.csv (stored in Airdrops/)

2. Monthly Airdrop
Processes kid_holders.csv and distributes tokens based on fixed multipliers.

Download the Kid Shroom Holders and rename it to Kid_holders.csv
https://www.signorcrypto.com/toolkit/snapshot
Address = 0x9c92B882aC7aeff58414D874de60d30381991BaD

Input
kid_holders.csv
Output:
Kid_Airdrop_Shrooms_X.csv
Kid_Airdrop_Spores_X.csv
Stored in kid_shroom/ folder.

3. BRUH Token Airdrop
Processes bruh_holders.csv and bruh_current.csv into a single output file.

Download the Bruh Holders and rename it to bruh_holders.csv
https://www.signorcrypto.com/toolkit/snapshot
Address = 0xeE0Db7c640b5A27405384Abf62db1985d12F0256

Download the Bruh Holders and rename it to bruh_current.csv
https://www.signorcrypto.com/toolkit/snapshot
Address = 0xeE0Db7c640b5A27405384Abf62db1985d12F0256
Token IDs = Current Edition

Input:
bruh_holders.csv
bruh_current.csv
Output:
Airdrop_Bruh_X.csv
Stored in Bruh/ folder.

Fixing CSV Errors
If you get a KeyError: 'percentage', check that your CSV file contains a percentage column.
If you get KeyError: 'quantity', check that your CSV contains address and quantity columns.
Ensure column names do not have extra spaces.
Ensuring Unique File Names
Generated airdrop files will never overwrite existing files. The script automatically assigns unique filenames like:

Airdrop_1.csv
Airdrop_2.csv
Airdrop_3.csv

Example Run (Step-by-Step)
Download CSVs
shroom_holders.csv and spore_holders.csv from Polygonscan or another data source.
Run the script
Open your terminal or command prompt.
Navigate to the project folder.
Run the appropriate script based on the airdrop type.
Check the output
The generated CSV will be saved in the respective folder.
This tool ensures airdrops are processed quickly, accurately, and securely.