"""
Export Boston Parcel Data from Supabase to CSV.

This script:
1. Loads environment variables from .env file
2. Connects to Supabase using service role key
3. Fetches ALL rows from 'properties' table with pagination
4. Exports to data/raw/boston_properties.csv
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import time

# Load environment variables
load_dotenv()

def get_supabase_client() -> Client:
    """Create and return Supabase client."""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url:
        raise ValueError("SUPABASE_URL not found in environment variables")
    if not supabase_key:
        raise ValueError("SUPABASE_SERVICE_ROLE_KEY not found in environment variables")
    
    return create_client(supabase_url, supabase_key)

def fetch_all_properties(supabase: Client, batch_size: int = 1000) -> pd.DataFrame:
    """
    Fetch all rows from properties table with pagination.
    
    Args:
        supabase: Supabase client instance
        batch_size: Number of rows to fetch per request
    
    Returns:
        pandas DataFrame with all properties
    """
    all_data = []
    offset = 0
    total_fetched = 0
    
    print(f"Starting data export from 'properties' table...")
    print(f"Fetching in batches of {batch_size} rows...")
    
    while True:
        try:
            # Fetch batch with pagination using range (inclusive both ends)
            # range(from, to) where both are inclusive
            to_index = offset + batch_size - 1
            response = supabase.table("properties").select("*").range(offset, to_index).execute()
            
            batch_data = response.data
            
            if not batch_data:
                print(f"No more data to fetch.")
                break
            
            all_data.extend(batch_data)
            total_fetched += len(batch_data)
            
            print(f"Fetched {len(batch_data)} rows (Total: {total_fetched})")
            
            # If we got fewer rows than batch_size, we've reached the end
            if len(batch_data) < batch_size:
                break
            
            offset += batch_size
            
            # Add delay to avoid rate limiting
            time.sleep(1)
            
        except Exception as e:
            print(f"Error fetching data at offset {offset}: {str(e)}")
            raise
    
    print(f"\nTotal rows fetched: {total_fetched}")
    
    # Convert to DataFrame
    if not all_data:
        print("Warning: No data found in properties table")
        return pd.DataFrame()
    
    df = pd.DataFrame(all_data)
    return df

def export_to_csv(df: pd.DataFrame, output_path: Path):
    """Export DataFrame to CSV file."""
    # Create directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Export to CSV
    df.to_csv(output_path, index=False)
    print(f"\nData exported successfully to: {output_path}")

def main():
    """Main execution function."""
    try:
        # Get Supabase client
        print("Connecting to Supabase...")
        supabase = get_supabase_client()
        print("Connection successful!\n")
        
        # Fetch all properties
        df = fetch_all_properties(supabase)
        
        if df.empty:
            print("No data to export.")
            return
        
        # Print statistics
        print("\n" + "="*50)
        print("DATA STATISTICS")
        print("="*50)
        print(f"Total rows: {len(df)}")
        print(f"Total columns: {len(df.columns)}")
        print(f"Shape: {df.shape}")
        print(f"\nColumns: {', '.join(df.columns.tolist())}")
        print("="*50)
        
        # Export to CSV
        output_path = Path("data/raw/boston_properties.csv")
        export_to_csv(df, output_path)
        
        print("\nExport completed successfully!")
        
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

