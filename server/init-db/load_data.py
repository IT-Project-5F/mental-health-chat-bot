#!/usr/bin/env python3
"""
Script to load CSV data into PostgreSQL database during Docker initialization
"""

import os
import sys
import psycopg2
import pandas as pd
from psycopg2.extras import execute_values

# Database connection from environment variables
conn_params = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'database': os.getenv('POSTGRES_DB', 'mental_health_db'),
    'user': os.getenv('POSTGRES_USER', 'mental_health_user'),
    'password': os.getenv('POSTGRES_PASSWORD', 'mental_health_password'),
    'port': '5432'
}

def load_raw_data(conn):
    """Load mental health services raw data"""
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM MentalHealthRawData")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"MentalHealthRawData table already has {count} records. Skipping data load.")
        cursor.close()
        return
    
    df = pd.read_csv('/data/mental_health_services_nwmphn_dataset.csv')
    
    # Replace NaN values with None for SQL NULL
    df = df.where(pd.notnull(df), None)
    
    data_list = []
    for index, row in df.iterrows():
        data_list.append((
            row.get('organisation_name'),
            row.get('campus_name'),
            row.get('service_name'),
            row.get('region_name'),
            row.get('email'),
            row.get('phone'),
            row.get('website'),
            row.get('notes'),
            row.get('expected_wait_time'),
            True if row.get('opening_hours_24_7') == "Yes" else False,
            True if row.get('opening_hours_standard') == "Yes" else False,
            True if row.get('opening_hours_extended') == "Yes" else False,
            row.get('op_hours_extended_details'),
            row.get('address'),
            row.get('suburb'),
            row.get('state'),
            row.get('postcode'),
            row.get('cost'),
            row.get('delivery_method'),
            row.get('level_of_care'),
            row.get('referral_pathway'),
            row.get('service_type'),
            row.get('target_population'),
            row.get('workforce_type')
        ))
    
    execute_values(
        cursor,
        """
        INSERT INTO MentalHealthRawData (
            organisation_name,
            campus_name,
            service_name,
            region_name,
            email,
            phone,
            website,
            notes,
            expected_wait_time,
            opening_hours_24_7,
            opening_hours_standard,
            opening_hours_extended,
            op_hours_extended_details,
            address,
            suburb,
            state,
            postcode,
            cost,
            delivery_method,
            level_of_care,
            referral_pathway,
            service_type,
            target_population,
            work_force_type
        ) VALUES %s
        """,
        data_list
    )
    
    cursor.close()
    conn.commit()
    print(f"Loaded {len(data_list)} records into MentalHealthRawData table")

def load_embeddings(conn):
    """Load mental health embeddings data"""
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM MentalHealthEmbeddings")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"MentalHealthEmbeddings table already has {count} records. Skipping data load.")
        cursor.close()
        return
    
    df = pd.read_csv('/data/mental_health_embedding.csv')
    
    data_list = [
        (row['index'], int(row['token_len']), row['embeddings'])
        for index, row in df.iterrows()
    ]
    
    execute_values(
        cursor,
        "INSERT INTO MentalHealthEmbeddings (record_index, tokens, embedding) VALUES %s",
        data_list
    )
    
    cursor.close()
    conn.commit()
    print(f"Loaded {len(data_list)} embeddings into MentalHealthEmbeddings table")

if __name__ == "__main__":
    try:
        conn = psycopg2.connect(**conn_params)
        
        print("Loading mental health raw data...")
        load_raw_data(conn)
        
        print("Loading mental health embeddings...")
        load_embeddings(conn)
        
        print("Database initialization completed successfully!")
    except Exception as e:
        print(f"Error during database initialization: {e}")
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()