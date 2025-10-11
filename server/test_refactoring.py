#!/usr/bin/env python3
"""
Comprehensive test script for database refactoring
Tests table creation, data ingestion, and retrieval
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from models import *
    from database_config import engine
    from chat.rag_service import (
        get_embeddings_vector,
        get_top3_similar_docs,
        process_input_with_retrieval_continuous
    )
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all dependencies are installed and the database is running.")
    sys.exit(1)

load_dotenv()

# Test colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_test_header(test_name):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}Testing: {test_name}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.YELLOW}ℹ {message}{Colors.END}")

def test_database_connection():
    """Test 1: Database Connection"""
    print_test_header("Database Connection")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print_success(f"Connected to PostgreSQL: {version}")

            # Test pgvector extension
            result = conn.execute(text("SELECT extname FROM pg_extension WHERE extname = 'vector'"))
            if result.fetchone():
                print_success("pgvector extension is enabled")
            else:
                print_error("pgvector extension is NOT enabled")
                return False
        return True
    except Exception as e:
        print_error(f"Database connection failed: {e}")
        return False

def test_table_creation():
    """Test 2: Table Creation"""
    print_test_header("Table Creation")
    try:
        inspector = inspect(engine)
        expected_tables = [
            'organisation', 'region', 'service', 'campus', 'service_campus',
            'target_population', 'level_of_care', 'service_type', 'cost',
            'referral_pathway', 'workforce_type', 'delivery_method',
            'postcode', 'service_region', 'raw_record_storage', 'embedding_table'
        ]

        existing_tables = inspector.get_table_names()

        all_present = True
        for table in expected_tables:
            if table in existing_tables:
                print_success(f"Table '{table}' exists")
            else:
                print_error(f"Table '{table}' is MISSING")
                all_present = False

        print_info(f"Total tables found: {len(existing_tables)}")
        return all_present
    except Exception as e:
        print_error(f"Table inspection failed: {e}")
        return False

def test_data_ingestion():
    """Test 3: Data Ingestion"""
    print_test_header("Data Ingestion")

    try:
        with Session(engine) as session:
            # Check main entity counts
            tables_to_check = [
                (Organisation, "Organisations"),
                (Service, "Services"),
                (Campus, "Campuses"),
                (ServiceCampus, "ServiceCampus records"),
                (Region, "Regions"),
                (RawRecordStorage, "Raw records"),
            ]

            all_populated = True
            for model, name in tables_to_check:
                count = session.query(model).count()
                if count > 0:
                    print_success(f"{name}: {count} records")
                else:
                    print_error(f"{name}: NO DATA")
                    all_populated = False

            # Check specific relationships
            print_info("\nChecking relationships:")

            # Get a sample raw record
            raw_record = session.query(RawRecordStorage).first()
            if raw_record:
                # Check if foreign keys are properly set
                checks = [
                    (raw_record.organisation_key is not None, "Organisation link"),
                    (raw_record.campus_service_key is not None, "ServiceCampus link"),
                ]

                for check, name in checks:
                    if check:
                        print_success(f"{name} is set")
                    else:
                        print_error(f"{name} is NOT set")

                # Test JOIN query
                result = session.query(
                    Organisation.organisation_name,
                    ServiceCampus.email,
                    ServiceCampus.phone
                ).join(
                    RawRecordStorage,
                    RawRecordStorage.organisation_key == Organisation.organisation_key
                ).join(
                    ServiceCampus,
                    ServiceCampus.service_campus_key == RawRecordStorage.campus_service_key
                ).first()

                if result:
                    print_success(f"JOIN query successful: {result[0][:30]}...")
                else:
                    print_error("JOIN query returned no results")
            else:
                print_error("No raw records found to test relationships")
                all_populated = False

            return all_populated
    except Exception as e:
        print_error(f"Data ingestion test failed: {e}")
        return False

def test_embedding_storage():
    """Test 4: Embedding Storage"""
    print_test_header("Embedding Storage")

    try:
        with Session(engine) as session:
            # Check embedding count
            embedding_count = session.query(EmbeddingStorage).count()

            if embedding_count > 0:
                print_success(f"Embeddings stored: {embedding_count}")

                # Check embedding-to-raw-record link
                embedding = session.query(EmbeddingStorage).first()
                if embedding and embedding.record_key:
                    # Verify the linked raw record exists
                    raw_record = session.query(RawRecordStorage).filter_by(
                        raw_record_storage_key=embedding.record_key
                    ).first()

                    if raw_record:
                        print_success("Embedding linked to raw record correctly")
                        print_info(f"Raw record index: {raw_record.csv_record_index}")
                    else:
                        print_error("Embedding record_key doesn't match any raw record")
                        return False

                    # Check embedding vector dimension
                    if embedding.embedding:
                        print_info(f"Embedding dimension: {len(embedding.embedding)}")
                    else:
                        print_error("Embedding vector is empty")
                        return False
                else:
                    print_error("Embedding has no record_key")
                    return False
            else:
                print_error("No embeddings found")
                return False

            return True
    except Exception as e:
        print_error(f"Embedding storage test failed: {e}")
        return False

def test_retrieval_system():
    """Test 5: Retrieval System"""
    print_test_header("Retrieval System")

    try:
        # Test embedding generation
        test_query = "I need help with anxiety"
        print_info(f"Test query: '{test_query}'")

        embedding = get_embeddings_vector(test_query)
        if embedding and len(embedding) > 0:
            print_success(f"Query embedding generated: dimension {len(embedding)}")
        else:
            print_error("Failed to generate query embedding")
            return False

        # Test similarity search
        similar_docs = get_top3_similar_docs(embedding)
        if similar_docs and len(similar_docs) > 0:
            print_success(f"Retrieved {len(similar_docs)} similar documents")

            # Check structure of returned documents
            first_doc = similar_docs[0]
            required_fields = ['organisation_name', 'service_name', 'phone', 'email']

            for field in required_fields:
                if field in first_doc:
                    value = first_doc[field]
                    if value:
                        print_success(f"Field '{field}': {str(value)[:50]}...")
                    else:
                        print_info(f"Field '{field}': None/Empty")
                else:
                    print_error(f"Field '{field}' is MISSING")

            # Test full service details retrieval
            if 'cost' in first_doc and 'delivery_method' in first_doc:
                print_success("Lookup table data retrieved successfully")
            else:
                print_error("Lookup table data not properly retrieved")
        else:
            print_error("No similar documents retrieved")
            return False

        return True
    except Exception as e:
        print_error(f"Retrieval system test failed: {e}")
        return False

def test_end_to_end_rag():
    """Test 6: End-to-End RAG Service"""
    print_test_header("End-to-End RAG Service")

    try:
        test_queries = [
            "I need mental health support for depression",
            "What services are available 24/7?",
            "Find services in Melbourne"
        ]

        for query in test_queries:
            print_info(f"\nTesting query: '{query}'")

            response = process_input_with_retrieval_continuous(query)

            if response and len(response) > 0:
                print_success(f"Response generated ({len(response)} chars)")
                print_info(f"Response preview: {response[:200]}...")
            else:
                print_error("Empty or no response generated")
                return False

        # Test with conversation history
        print_info("\nTesting with conversation history")
        history = [
            {"role": "user", "content": "I need help"},
            {"role": "assistant", "content": "I can help you find mental health services."}
        ]

        response = process_input_with_retrieval_continuous(
            "What about anxiety services?",
            conversation_history=history
        )

        if response:
            print_success("Response with history generated successfully")
        else:
            print_error("Failed to generate response with history")
            return False

        return True
    except Exception as e:
        print_error(f"End-to-end RAG test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}DATABASE REFACTORING COMPREHENSIVE TEST SUITE{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")

    tests = [
        ("Database Connection", test_database_connection),
        ("Table Creation", test_table_creation),
        ("Data Ingestion", test_data_ingestion),
        ("Embedding Storage", test_embedding_storage),
        ("Retrieval System", test_retrieval_system),
        ("End-to-End RAG", test_end_to_end_rag),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {e}")
            results.append((test_name, False))

    # Summary
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}TEST SUMMARY{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")

    passed = sum(1 for _, result in results if result)
    failed = len(results) - passed

    for test_name, result in results:
        if result:
            print(f"{Colors.GREEN}✓ {test_name}: PASSED{Colors.END}")
        else:
            print(f"{Colors.RED}✗ {test_name}: FAILED{Colors.END}")

    print(f"\n{Colors.BOLD}Total: {passed}/{len(results)} tests passed{Colors.END}")

    if passed == len(results):
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! Database refactoring is working correctly!{Colors.END}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}⚠ {failed} test(s) failed. Please review the errors above.{Colors.END}")

    return passed == len(results)

if __name__ == "__main__":
    # First ensure tables exist
    print_info("Creating tables if they don't exist...")
    Base.metadata.create_all(bind=engine)

    success = run_all_tests()
    sys.exit(0 if success else 1)