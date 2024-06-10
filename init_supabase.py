# initialize_supabase.py

import os
from dotenv import load_dotenv
from supabase import create_client, Client

def initialize_supabase():
    env_path = os.path.join(os.path.dirname(__file__), 'mysite', 'mysite', '.env')
    load_dotenv(env_path)  # Load environment variables from .env file
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        print("Please set the SUPABASE_URL and SUPABASE_KEY environment variables in the .env file.")
        return

    supabase = create_client(url, key)

    print('Supabase client initialized successfully!')

if __name__ == "__main__":
    initialize_supabase()
