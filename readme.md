
🔧 Project Overview
The toolkit supports three main types of airdrops:

Kid Mooshie NFT Holders (airdrop_kid.py)

Bruh NFT Holders (airdrop_bruh.py)

Liquidity Providers (LP) for SHROOM and SPORE (airdrop_lp.py)

Each script pulls from a config.py file and reads CSV files containing address and quantity/percentage data to generate SafeWallet-compatible output files.

📁 Directory Structure
config.py: Stores all contract addresses and airdrop pool constants.

airdrop_kid.py: Handles fixed-rate airdrops for Kid Mooshie holders.

airdrop_bruh.py: Supports more complex logic including:

Combined CSV sources

Dynamic quantity normalization

Omission of blacklisted addresses

airdrop_lp.py: Proportionally distributes tokens based on LP share percentages.

kid_shroom/, Bruh/, LP/: Output folders for each respective script.

✅ Requirements
Python 3.8+

pandas

python-dotenv

Install dependencies using:

pip install pandas python-dotenv

⚙️ Configuration
Before running any script, make sure your .env file contains relevant API keys or environment variables if needed, and check that config.py includes the latest contract addresses and pool allocations:

Examples in config.py:

SHROOM_LP = "0x28DEf03d8DC0d186FaBAe9C46043e8eF9BfFCc28"
SPORE_LP = "0x2a91571238303c6700A9336342c754e159243168"
SHROOM_AIRDROP_POOL = 7000000
SPORE_AIRDROP_POOL = 500000000
BRUH_ALL = 100000
BRUH_CURRENT = 125000
JIMMY = 25000

📌 How to Use
Kid Airdrop

Place kid_holders.csv in the root directory.

Run: python airdrop_kid.py

Output: Kid_Airdrop_Shrooms_X.csv and Kid_Airdrop_Spores_X.csv in kid_shroom/

Bruh Airdrop

Place bruh_all.csv, bruh_mono.csv, bruh_color.csv, and jimmy.csv in the Bruh/ folder.

Run: python airdrop_bruh.py

Output: Airdrop_Bruh_X.csv in Bruh/

LP Airdrop

Place shroom_holders.csv and spore_holders.csv in the LP/ folder.

Run: python airdrop_lp.py

Output: Airdrop_LP_X.csv in LP/

🔐 Address Filtering
The following addresses are automatically excluded from airdrops:

0x000000000000000000000000000000000000dead

0x0000000000000000000000000000000000000000

Any additional blacklisted addresses can be added in airdrop_bruh.py under the OMIT_ADDRESSES list.

🔍 Features
Dynamic filename generation to prevent overwrites

Intelligent column handling and error checking

Built-in rounding adjustment to match exact pool totals

Lowercasing of addresses for consistent validation

SafeWallet-ready CSV formatting

Separation of output per airdrop category

📈 Example Airdrop Calculations
Kid Holders:

SHROOM = quantity × 20,000

SPORE = quantity × 1,500,000

Bruh Holders:

Airdrop is proportional to quantity share per group

Each subgroup (ALL, CURRENT, JIMMY) gets a different pool

LP Providers:

Airdrop = percentage × total pool (SHROOM or SPORE)

Any leftover (usually 0.1%) from rounding is added to the top address (treasury)