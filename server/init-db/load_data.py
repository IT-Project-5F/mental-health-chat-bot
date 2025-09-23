#!/usr/bin/env python3
"""
Script to load CSV data into PostgreSQL database during Docker initialization
"""

import os
import sys
import psycopg2
import pandas as pd
import ast
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector

# Database connection from environment variables
conn_params = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'database': os.getenv('POSTGRES_DB', 'mental_health_db'),
    'user': os.getenv('POSTGRES_USER', 'mental_health_user'),
    'password': os.getenv('POSTGRES_PASSWORD', 'password'),
    'port': '5432'
}

def load_normalized_data(conn):
    """Load mental health services data into normalized tables"""
    cursor = conn.cursor()

    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM raw_record_storage")
    count = cursor.fetchone()[0]

    if count > 0:
        print(f"Database already has {count} records. Skipping data load.")
        cursor.close()
        return

    df = pd.read_csv('/data/mental_health_services_nwmphn_dataset.csv')
    df["index"] = range(1, len(df) + 1)

    # Replace NaN values with None for SQL NULL
    df = df.where(pd.notnull(df), None)

    # Initialize dictionaries to cache inserted records
    organisations = {}
    campuses = {}
    services = {}
    regions = {}

    for _, row in df.iterrows():
        # Insert Organisation
        org_name = row['organisation_name']
        if org_name and org_name not in organisations:
            cursor.execute(
                "INSERT INTO organisation (organisation_name) VALUES (%s) RETURNING organisation_key",
                (org_name,)
            )
            organisations[org_name] = cursor.fetchone()[0]
        org_key = organisations.get(org_name)

        # Insert Region
        region_name = row.get('region_name')
        region_key = None
        if region_name and region_name not in regions:
            cursor.execute(
                "INSERT INTO region (region_name) VALUES (%s) RETURNING region_key",
                (region_name,)
            )
            regions[region_name] = cursor.fetchone()[0]
        if region_name:
            region_key = regions.get(region_name)

        # Insert Campus
        campus_name = row['campus_name']
        campus_key_name = f"{campus_name}_{org_key}"
        if campus_name and campus_key_name not in campuses:
            cursor.execute(
                "INSERT INTO campus (organisation_key, campus_name) VALUES (%s, %s) RETURNING campus_key",
                (org_key, campus_name)
            )
            campuses[campus_key_name] = cursor.fetchone()[0]
        campus_key = campuses.get(campus_key_name)

        # Insert Service
        service_name = row['service_name']
        service_key_name = f"{service_name}_{org_key}"
        if service_name and service_key_name not in services:
            cursor.execute(
                "INSERT INTO service (organisation_key, service_name) VALUES (%s, %s) RETURNING service_key",
                (org_key, service_name)
            )
            services[service_key_name] = cursor.fetchone()[0]
        service_key = services.get(service_key_name)

        # Insert ServiceCampus
        cursor.execute("""
            INSERT INTO service_campus (
                service_key, campus_key, email, phone, website, notes,
                expected_wait_time, op_hours_24_7, op_hours_standard,
                op_hours_extended, op_hours_extended_details, address,
                suburb, state, postcode
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING service_campus_key
        """, (
            service_key, campus_key, row.get('email'), row.get('phone'),
            row.get('website'), row.get('notes'), row.get('expected_wait_time'),
            row.get('opening_hours_24_7') == "Yes",
            row.get('opening_hours_standard') == "Yes",
            row.get('opening_hours_extended') == "Yes",
            row.get('op_hours_extended_details'), row.get('address'),
            row.get('suburb'), row.get('state'), row.get('postcode')
        ))
        sc_key = cursor.fetchone()[0]

        # Insert lookup table records
        cost_key = None
        if row.get('cost'):
            cursor.execute(
                "INSERT INTO cost (service_campus_key, cost) VALUES (%s, %s) RETURNING cost_key",
                (sc_key, row['cost'])
            )
            cost_key = cursor.fetchone()[0]

        delivery_method_key = None
        if row.get('delivery_method'):
            cursor.execute(
                "INSERT INTO delivery_method (service_campus_key, delivery_method) VALUES (%s, %s) RETURNING delivery_method_key",
                (sc_key, row['delivery_method'])
            )
            delivery_method_key = cursor.fetchone()[0]

        level_of_care_key = None
        if row.get('level_of_care'):
            cursor.execute(
                "INSERT INTO level_of_care (service_campus_key, level_of_care) VALUES (%s, %s) RETURNING level_of_care_key",
                (sc_key, row['level_of_care'])
            )
            level_of_care_key = cursor.fetchone()[0]

        referral_pathway_key = None
        if row.get('referral_pathway'):
            cursor.execute(
                "INSERT INTO referral_pathway (service_campus_key, referral_pathway) VALUES (%s, %s) RETURNING referral_pathway_key",
                (sc_key, row['referral_pathway'])
            )
            referral_pathway_key = cursor.fetchone()[0]

        service_type_key = None
        if row.get('service_type'):
            cursor.execute(
                "INSERT INTO service_type (service_campus_key, service_type) VALUES (%s, %s) RETURNING service_type_key",
                (sc_key, row['service_type'])
            )
            service_type_key = cursor.fetchone()[0]

        target_population_key = None
        if row.get('target_population'):
            cursor.execute(
                "INSERT INTO target_population (service_campus_key, target_population) VALUES (%s, %s) RETURNING target_population_key",
                (sc_key, row['target_population'])
            )
            target_population_key = cursor.fetchone()[0]

        workforce_type_key = None
        if row.get('workforce_type'):
            cursor.execute(
                "INSERT INTO workforce_type (service_campus_key, workforce_type) VALUES (%s, %s) RETURNING workforce_type_key",
                (sc_key, row['workforce_type'])
            )
            workforce_type_key = cursor.fetchone()[0]

        # Insert RawRecordStorage
        cursor.execute("""
            INSERT INTO raw_record_storage (
                csv_record_index, organisation_key, campus_service_key,
                region_key, cost_key, delivery_method_key, level_of_care_key,
                referral_pathway_key, service_type_key, target_population_key,
                workforce_type_key
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['index'], org_key, sc_key, region_key, cost_key,
            delivery_method_key, level_of_care_key, referral_pathway_key,
            service_type_key, target_population_key, workforce_type_key
        ))

    cursor.close()
    conn.commit()
    print(f"Loaded {len(df)} records into normalized database")

def load_embeddings(conn):
    """Load mental health embeddings data"""
    cursor = conn.cursor()
    register_vector(conn)

    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM embedding_table")
    count = cursor.fetchone()[0]

    if count > 0:
        print(f"Embedding table already has {count} records. Skipping data load.")
        cursor.close()
        return

    df = pd.read_csv('/data/mental_health_embedding.csv')

    for _, row in df.iterrows():
        csv_record_index = row.get('index')

        # Find the corresponding raw record
        cursor.execute(
            "SELECT raw_record_storage_key FROM raw_record_storage WHERE csv_record_index = %s",
            (csv_record_index,)
        )
        result = cursor.fetchone()

        if not result:
            print(f"Warning: No RawRecordStorage found for index {csv_record_index}")
            continue

        record_key = result[0]

        # Parse embedding vector
        if isinstance(row['embeddings'], str):
            try:
                embedding_vector = ast.literal_eval(row['embeddings'])
            except (ValueError, SyntaxError) as e:
                print(f"Error parsing embedding for index {csv_record_index}: {e}")
                continue
        else:
            embedding_vector = row['embeddings']

        # Insert embedding
        cursor.execute(
            "INSERT INTO embedding_table (record_key, token, embedding) VALUES (%s, %s, %s)",
            (record_key, int(row['token_len']), embedding_vector)
        )

    # Create vector index
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS embedding_idx
        ON embedding_table
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100)
    """)
    cursor.execute("ANALYZE embedding_table")

    cursor.close()
    conn.commit()
    print(f"Loaded {len(df)} embeddings into database")

if __name__ == "__main__":
    try:
        conn = psycopg2.connect(**conn_params)

        print("Loading normalized mental health data...")
        load_normalized_data(conn)

        print("Loading mental health embeddings...")
        load_embeddings(conn)

        print("Database initialization completed successfully!")
    except Exception as e:
        print(f"Error during database initialization: {e}")
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()