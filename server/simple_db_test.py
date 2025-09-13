#!/usr/bin/env python3
"""
Simple database connectivity test
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

try:
    import psycopg2
    from sqlalchemy import create_engine, text, inspect

    # Database connection parameters
    DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER', 'mental_health_user')}:" \
                   f"{os.getenv('POSTGRES_PASSWORD', 'mental_health_password')}@" \
                   f"{os.getenv('POSTGRES_HOST', 'localhost')}:" \
                   f"{os.getenv('POSTGRES_PORT', '5432')}/" \
                   f"{os.getenv('POSTGRES_DB', 'mental_health_db')}"

    print("Testing database connection...")
    print(f"Connecting to: {DATABASE_URL.replace(os.getenv('POSTGRES_PASSWORD', 'password'), '***')}")

    # Test SQLAlchemy connection
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"✓ PostgreSQL version: {version[:50]}...")

        # Check if pgvector is installed
        result = conn.execute(text("SELECT extname FROM pg_extension WHERE extname = 'vector'"))
        if result.fetchone():
            print("✓ pgvector extension is enabled")
        else:
            print("✗ pgvector extension is NOT enabled")

        # List existing tables
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"✓ Found {len(tables)} tables:")
        for table in sorted(tables):
            print(f"  - {table}")

        # If we have normalized tables, check record counts
        if 'organisation' in tables:
            print("\nRecord counts in normalized tables:")
            for table in ['organisation', 'service', 'campus', 'service_campus', 'raw_record_storage', 'embedding_table']:
                if table in tables:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.fetchone()[0]
                    print(f"  {table}: {count} records")

    print("✓ Database test completed successfully!")

except ImportError as e:
    print(f"✗ Missing dependency: {e}")
    print("Please install required packages:")
    print("pip install psycopg2-binary sqlalchemy python-dotenv")

except Exception as e:
    print(f"✗ Database connection failed: {e}")
    print("Make sure PostgreSQL is running and environment variables are set correctly")