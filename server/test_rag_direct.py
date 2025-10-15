#!/usr/bin/env python3
"""
Direct test of RAG functionality with new normalized database
"""

import sys
import os
sys.path.append('/app')

try:
    from chat.Utils import get_topk_similar_docs, get_embeddings_vector, process_input_with_retrieval_continuous

    print("=== Testing New Normalized Database RAG System ===\n")

    # Test 1: Generate embedding for test query
    test_query = "I need help with anxiety and depression"
    print(f"Test Query: '{test_query}'")

    embedding = get_embeddings_vector(test_query)
    if embedding:
        print(f"✓ Generated embedding: dimension {len(embedding)}")
    else:
        print("✗ Failed to generate embedding")
        sys.exit(1)

    # Test 2: Get similar services
    print("\n--- Testing Similar Services Retrieval ---")
    similar_docs = get_topk_similar_docs(embedding)

    if similar_docs:
        print(f"✓ Retrieved {len(similar_docs)} similar services")

        for i, doc in enumerate(similar_docs, 1):
            print(f"\nService {i}:")
            print(f"  Organisation: {doc.get('organisation_name', 'N/A')}")
            print(f"  Service: {doc.get('service_name', 'N/A')}")
            print(f"  Campus: {doc.get('campus_name', 'N/A')}")
            print(f"  Phone: {doc.get('phone', 'N/A')}")
            print(f"  Email: {doc.get('email', 'N/A')}")
            print(f"  Cost: {doc.get('cost', 'N/A')}")
            print(f"  Service Type: {doc.get('service_type', 'N/A')}")
    else:
        print("✗ No similar services found")
        sys.exit(1)

    # Test 3: Full RAG pipeline
    print(f"\n--- Testing Full RAG Pipeline ---")
    response = process_input_with_retrieval_continuous(test_query)

    if response and len(response) > 0:
        print(f"✓ Generated response ({len(response)} characters)")
        print(f"Response preview: {response[:300]}...")
    else:
        print("✗ Failed to generate response")
        sys.exit(1)

    print(f"\n🎉 ALL TESTS PASSED! The normalized database refactoring is working correctly!")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)