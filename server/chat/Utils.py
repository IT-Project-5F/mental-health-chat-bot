import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .Validator import MentalHealthModel 
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import *
from database_config import engine, SessionLocal
from langchain_openai import OpenAIEmbeddings
import openai
from dotenv import load_dotenv

load_dotenv()
# Use OpenAI directly for chat completions
openai_client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def get_topk_similar_docs(query_embedding, k = 5):
    """Retrieve top k most similar documents based on cosine similarity"""
    if isinstance(query_embedding, np.ndarray):
        query_embedding = query_embedding.tolist()

    with Session(engine) as session:
        stmt = (
            select(EmbeddingStorage)
            .order_by(EmbeddingStorage.embedding.cosine_distance(query_embedding))
            .limit(k)
        )
        results = session.execute(stmt).scalars().all()
        return get_detailed_service_info(results)

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
       # print(response.choices[0].message.content)
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

