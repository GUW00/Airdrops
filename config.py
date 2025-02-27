# config.py
import os
from dotenv import load_dotenv

load_dotenv()

POLYSCAN_API_KEY = os.getenv("POLYSCAN_API_KEY")
SHROOM_CONTRACT = os.getenv("SHROOM_CONTRACT")
SPORE_CONTRACT = os.getenv("SPORE_CONTRACT")
SHROOM_LP = os.getenv("SRHOOM_LP")
SPORE_LP = os.getenv("SPORE_LP")
SHROOM_AIRDROP_POOL = float(os.getenv("SHROOM_AIRDROP_POOL", 7000000))
SPORE_AIRDROP_POOL = float(os.getenv("SPORE_AIRDROP_POOL", 500000000))
