import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import Dict, List
import requests
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import *
from database_config import engine, SessionLocal
from langchain_openai import OpenAIEmbeddings
import openai
from dotenv import load_dotenv

# Use OpenAI directly for chat completions
openai_client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def get_topk_similar_docs(query_embedding, k=5):
    """Retrieve top k most similar documents with cosine similarity scores"""
    if isinstance(query_embedding, np.ndarray):
        query_embedding = query_embedding.tolist()

    with Session(engine) as session:
        distance = EmbeddingStorage.embedding.cosine_distance(query_embedding)
        # Build query
        stmt = (
            select(EmbeddingStorage, distance.label("distance"))
            .order_by(distance)
            .limit(k)
        )
        # Execute query
        detail_docs = session.execute(stmt).all()
        if not detail_docs:
            return []
        # Batch fetch service info for all documents at once
        docs_only = [doc for doc, _ in detail_docs]
        services = get_detailed_service_info(docs_only)

        # Build results with similarity filtering
        results = []
        for service, (_, dist) in zip(services, detail_docs):
            similarity = 1 - dist
            results.append({
                "service": service,
                "similarity": float(similarity)  # Ensure JSON serializable
            })

        return results

def get_detailed_service_info(embedding_records):
    """Retrieve detailed service information from related tables"""
    detailed_info = []

    with Session(engine) as session:
        for embedding_record in embedding_records:
            # Get the raw record
            raw_record = session.query(RawRecordStorage).filter_by(
                raw_record_storage_key=embedding_record.record_key
            ).first()

            if not raw_record:
                continue

            # Get related information
            org = session.query(Organisation).filter_by(
                organisation_key=raw_record.organisation_key
            ).first()

            service_campus = session.query(ServiceCampus).filter_by(
                service_campus_key=raw_record.campus_service_key
            ).first()

            if service_campus:
                service = session.query(Service).filter_by(
                    service_key=service_campus.service_key
                ).first()

                campus = session.query(Campus).filter_by(
                    campus_key=service_campus.campus_key
                ).first()
            else:
                service = None
                campus = None

            region = None
            if raw_record.region_key:
                region = session.query(Region).filter_by(
                    region_key=raw_record.region_key
                ).first()

            # Get optional related data
            cost = None
            if raw_record.cost_key:
                cost = session.query(Cost).filter_by(
                    cost_key=raw_record.cost_key
                ).first()

            delivery_method = None
            if raw_record.delivery_method_key:
                delivery_method = session.query(DeliveryMethod).filter_by(
                    delivery_method_key=raw_record.delivery_method_key
                ).first()

            level_of_care = None
            if raw_record.level_of_care_key:
                level_of_care = session.query(LevelOfCare).filter_by(
                    level_of_care_key=raw_record.level_of_care_key
                ).first()

            referral_pathway = None
            if raw_record.referral_pathway_key:
                referral_pathway = session.query(ReferralPathway).filter_by(
                    referral_pathway_key=raw_record.referral_pathway_key
                ).first()

            service_type = None
            if raw_record.service_type_key:
                service_type = session.query(ServiceType).filter_by(
                    service_type_key=raw_record.service_type_key
                ).first()

            target_population = None
            if raw_record.target_population_key:
                target_population = session.query(TargetPopulation).filter_by(
                    target_population_key=raw_record.target_population_key
                ).first()

            workforce_type = None
            if raw_record.workforce_type_key:
                workforce_type = session.query(WorkforceType).filter_by(
                    workforce_type_key=raw_record.workforce_type_key
                ).first()

            # Build detailed info dictionary
            service_info = {
                'organisation_name': org.organisation_name if org else None,
                'service_name': service.service_name if service else None,
                'campus_name': campus.campus_name if campus else None,
                'region_name': region.region_name if region else None,
                'email': service_campus.email if service_campus else None,
                'phone': service_campus.phone if service_campus else None,
                'website': service_campus.website if service_campus else None,
                'address': service_campus.address if service_campus else None,
                'suburb': service_campus.suburb if service_campus else None,
                'state': service_campus.state if service_campus else None,
                'postcode': service_campus.postcode if service_campus else None,
                'notes': service_campus.notes if service_campus else None,
                'expected_wait_time': service_campus.expected_wait_time if service_campus else None,
                'opening_hours_24_7': service_campus.op_hours_24_7 if service_campus else False,
                'opening_hours_standard': service_campus.op_hours_standard if service_campus else False,
                'opening_hours_extended': service_campus.op_hours_extended if service_campus else False,
                'op_hours_extended_details': service_campus.op_hours_extended_details if service_campus else None,
                'cost': cost.cost if cost else None,
                'delivery_method': delivery_method.delivery_method if delivery_method else None,
                'level_of_care': level_of_care.level_of_care if level_of_care else None,
                'referral_pathway': referral_pathway.referral_pathway if referral_pathway else None,
                'service_type': service_type.service_type if service_type else None,
                'target_population': target_population.target_population if target_population else None,
                'workforce_type': workforce_type.workforce_type if workforce_type else None,
            }

            detailed_info.append(service_info)

    return detailed_info

def get_completion_from_messages(messages, model="gpt-4o", temperature=0, max_tokens=1000):
    """Get completion from OpenAI API"""
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting completion: {e}")
        return "I'm having trouble processing your request right now. Please try again later."

def get_embeddings_vector(text):
    """Get embeddings vector for text - tries OpenAI first, falls back to OpenRouter"""
    try:
        import requests

        # Try OpenAI first (works from most regions, cheaper)
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "text-embedding-3-small",
            "input": text
        }

        response = requests.post(
            "https://api.openai.com/v1/embeddings",
            headers=headers,
            json=data,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            return result['data'][0]['embedding']

        print(f"Error getting embeddings: {response.status_code} - {response.text}")
        return None

    except Exception as e:
        print(f"Error getting embeddings: {e}")
        import traceback
        traceback.print_exc()
        return None

def check_require_web_search(user_input: str) -> bool:
        """
        Determine if the query needs web search based on keywords
        """
        web_search_indicators = [
            "latest", "recent", "new", "current", "updated", "2024", "2025",
            "near me", "in my area", "location", "address", "phone number",
            "reviews", "ratings", "cost", "price", "insurance",
            "emergency", "crisis", "urgent", "immediate help"
        ]
        return any(indicator in user_input.lower() for indicator in web_search_indicators)

def check_mental_health_website(result: Dict) -> bool:
    relevant_domains = {
        "nih.gov", "nimh.nih.gov", "cdc.gov", "samhsa.gov", "psychologytoday.com",
        "nami.org", "mentalhealth.gov", "who.int", "apa.org", "therapist.com",
        "betterhelp.com", "talkspace.com", "psychcentral.com", "webmd.com",
        "mayo.clinic", "clevelandclinic.org"
    }

    keywords = {
        "mental health", "therapy", "counseling", "depression", "anxiety",
        "psychiatr", "psycholog", "wellness", "support", "crisis", "suicide"
    }

    link = result.get("link", "").lower()
    title = result.get("title", "").lower()
    snippet = result.get("snippet", "").lower()

    # Check if domain is relevant
    if any(domain in link for domain in relevant_domains):
        return True

    # Check if content mentions mental health keywords
    content = title + " " + snippet
    if any(keyword in content for keyword in keywords):
        return True
    return False

def process_search_results(self, search_results: Dict) -> List[Dict]:
        """
        Process and filter web search results for mental health relevance
        """
        processed_results = []

        # Get organic results
        organic_results = search_results.get("organic", [])

        for result in organic_results[:3]:  # Take top 3 results
            # Filter for mental health related sites
            if self._is_mental_health_relevant(result):
                processed_results.append({
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", ""),
                    "link": result.get("link", ""),
                    "source": result.get("displayLink", "")
                })

        return processed_results

def web_search(query: str) -> List[Dict]:
    """
    Perform web search for mental health information
    """
    serper_web_search_keys = os.getenv("SERPER_API_KEY")
    if not serper_web_search_keys:
        print("No web search API key configured - skipping web search")
        return []
    try:
        # Using Serper API for web search
        url = "https://google.serper.dev/search"
        # Enhance query for better mental health results
        enhanced_query = f"mental health {query} services support therapy counseling"
        payload = {
            "q": enhanced_query,
            "num": 5,
            "gl": "us",  # Country
            "hl": "en"   # Language
        }
        headers = {
            "X-API-KEY": serper_web_search_keys,
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            results = response.json()
            return process_search_results(results)
        else:
            print(f"Web search API error: {response.status_code}")
            return []

    except Exception as e:
        print(f"Web search error: {e}")
        return []
