"""
Verify environment variables and Supabase connection.

This script:
1. Loads the .env file
2. Checks if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY exist
3. Tests the Supabase connection
"""

import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

def verify_env_variables():
    """Check if required environment variables are set."""
    print("Checking environment variables...")
    print("-" * 50)
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    url_set = supabase_url is not None and supabase_url != ""
    key_set = supabase_key is not None and supabase_key != ""
    
    print(f"SUPABASE_URL: {'✓ Set' if url_set else '✗ Not set'}")
    print(f"SUPABASE_SERVICE_ROLE_KEY: {'✓ Set' if key_set else '✗ Not set'}")
    print("-" * 50)
    
    return url_set and key_set

def test_connection():
    """Test Supabase connection."""
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not supabase_url or not supabase_key:
            print("\nCannot test connection: Missing environment variables")
            return False
        
        print("\nTesting Supabase connection...")
        supabase = create_client(supabase_url, supabase_key)
        
        # Try a simple query to test connection (limit 1 to be fast)
        # We'll just check if we can access the table without fetching data
        try:
            # This will fail if table doesn't exist or connection is bad
            supabase.table("properties").select("*", count="exact").limit(0).execute()
            print("✓ Connection successful!")
            return True
        except Exception as e:
            # If it's a table not found error, connection is still good
            if "relation" in str(e).lower() or "does not exist" in str(e).lower():
                print("✓ Connection successful! (Table may not exist yet)")
                return True
            else:
                print(f"✗ Connection failed: {str(e)}")
                return False
                
    except Exception as e:
        print(f"✗ Connection failed: {str(e)}")
        return False

def main():
    """Main execution function."""
    print("=" * 50)
    print("ENVIRONMENT VARIABLE VERIFICATION")
    print("=" * 50)
    
    env_ok = verify_env_variables()
    
    if env_ok:
        connection_ok = test_connection()
        if connection_ok:
            print("\n✓ All checks passed!")
        else:
            print("\n✗ Connection test failed")
    else:
        print("\n✗ Missing required environment variables")
        print("Please check your .env file")

if __name__ == "__main__":
    main()

