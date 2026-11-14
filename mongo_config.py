"""
MongoDB connection module for CutPro
Loads MONGO_URI from environment (Render) or .env (local)
"""
import os
from pathlib import Path

# Load .env file if it exists (local dev only — harmless if missing)
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    pass  # dotenv not installed — that's fine on Render

MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise RuntimeError("❌ MONGO_URI not set. Add it in Render Environment Variables.")

print("🔌 Connecting to MongoDB...")

from pymongo import MongoClient, ASCENDING, DESCENDING
import certifi

client = MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=10000
)

# Test connection
try:
    client.admin.command('ping')
    print("✅ MongoDB connected")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    raise

# Database + collections
db = client['cutpro']
users_col = db['users']
history_col = db['history']
skp_col = db['sketchup_parts']

# Indexes
users_col.create_index([('username', ASCENDING)], unique=True)
history_col.create_index([('username', ASCENDING), ('timestamp', DESCENDING)])

print("✅ Collections ready: users, history, sketchup_parts")