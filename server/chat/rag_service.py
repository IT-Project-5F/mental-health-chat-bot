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
from .enhanced_rag import EnhancedRAGWithWebSearch

load_dotenv()
openai_client = openai.OpenAI()

def get_top3_similar_docs(query_embedding, k=3):
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
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting completion: {e}")
        return "I'm having trouble processing your request right now. Please try again later."

def get_embeddings_vector(text): 
    """Get embeddings vector for text"""
    try:
        embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
        response = embedding_model.embed_query(text)
        return response
    except Exception as e:
        print(f"Error getting embeddings: {e}")
        return None

def process_input_with_retrieval_continuous(user_input, conversation_history=[]):
    """
    Process user input with mental health validation and detailed service retrieval.
    """
    # Input validation
    if not user_input or not isinstance(user_input, str):
        return "Please provide a valid question about mental health services."
    
    user_input = user_input.strip()
    if len(user_input) == 0:
        return "Please provide a question about mental health services."
    
    if len(user_input) > 1000:
        return "Your message is quite long. Please try to be more concise for better assistance."
    
    # Mental health validation using our new model
    try:

        validation_result = MentalHealthModel().validate_input(user_input)
        print(validation_result)
        if validation_result.is_trigger:
            # Log the trigger for monitoring
            print(f"Mental health trigger detected - Category: {validation_result.category}, "
                  f"Word: '{validation_result.matched_word}', Confidence: {validation_result.confidence:.2f}")
            
            # Return the mental health response immediately
            return validation_result.response
    except Exception as e:
        print(f"Mental health validation error: {e}")
        # Continue with normal processing if validation fails
    
    # Continue with normal RAG processing
    try:
        delimiter = "```"

        # Get embeddings for the user input
        query_embedding = get_embeddings_vector(user_input)
        if query_embedding is None:
            return "I'm having trouble processing your request. Please try again."

        # Get similar documents with full service details
        related_docs = get_top3_similar_docs(query_embedding)

        # Default assessment values for standard RAG processing
        assessment = {
            'confidence': 0.8,
            'reason': 'Using local database search'
        }
        sources_used = ['Local mental health database']

        system_message = f"""
        You are a friendly and helpful mental health services assistant. \
        You can answer questions about mental health services in Australia. \
        You respond in a warm, supportive, and technically credible tone. \
        Use the conversation history to maintain context and provide personalized responses. \
        Reference previous conversations when relevant. \
        Always prioritize the user's wellbeing in your responses. \

        Current situation:
        - RAG Confidence: {assessment['confidence']:.1%}
        - Reason for approach: {assessment['reason']}
        - Sources used: {', '.join(sources_used) if sources_used else 'none'}

        Instructions:
        1. If database has specific services, prioritize those with contact details
        2. If using web information, mention it's from online sources
        3. If no good matches found, be honest and suggest alternatives
        4. Always provide crisis resources if needed (Lifeline: 13 11 14)
        """

        # Build message history for context
        messages = [{"role": "system", "content": system_message}]

        # Add conversation history (limit to last 10 messages to manage token usage)
        recent_history = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
        messages.extend(recent_history)

        # Format the service information for better readability
        formatted_services = []
        for i, doc in enumerate(related_docs, 1):
            service_text = f"Service {i}:\n"
            if doc['organisation_name']:
                service_text += f"  Organisation: {doc['organisation_name']}\n"
            if doc['service_name']:
                service_text += f"  Service: {doc['service_name']}\n"
            if doc['campus_name']:
                service_text += f"  Campus: {doc['campus_name']}\n"
            if doc['phone']:
                service_text += f"  Phone: {doc['phone']}\n"
            if doc['email']:
                service_text += f"  Email: {doc['email']}\n"
            if doc['website']:
                service_text += f"  Website: {doc['website']}\n"
            if doc['address']:
                service_text += f"  Address: {doc['address']}"
                if doc['suburb']:
                    service_text += f", {doc['suburb']}"
                if doc['state']:
                    service_text += f" {doc['state']}"
                if doc['postcode']:
                    service_text += f" {doc['postcode']}"
                service_text += "\n"
            if doc['notes']:
                service_text += f"  Notes: {doc['notes']}\n"
            if doc['expected_wait_time']:
                service_text += f"  Wait Time: {doc['expected_wait_time']}\n"
            if doc['cost']:
                service_text += f"  Cost: {doc['cost']}\n"
            if doc['service_type']:
                service_text += f"  Service Type: {doc['service_type']}\n"
            if doc['target_population']:
                service_text += f"  Target Population: {doc['target_population']}\n"
            if doc['opening_hours_24_7']:
                service_text += f"  Hours: 24/7\n"
            elif doc['opening_hours_extended']:
                service_text += f"  Hours: Extended"
                if doc['op_hours_extended_details']:
                    service_text += f" ({doc['op_hours_extended_details']})"
                service_text += "\n"
            elif doc['opening_hours_standard']:
                service_text += f"  Hours: Standard business hours\n"

            formatted_services.append(service_text)

        # Add current user input and retrieved documents
        services_content = "\n".join(formatted_services) if formatted_services else "No specific services found for this query."
        
        user_message = f"""
        User question: {delimiter}{user_input}{delimiter}
        
        Please provide a helpful response based on the following relevant mental health services information:
        
        {services_content}
        
        If the services don't directly match the user's needs, provide general guidance and suggest they contact services directly or look for more specific resources.
        """
        
        messages.append({"role": "user", "content": user_message})

        final_response = get_completion_from_messages(messages)
        
        return final_response
        
    except Exception as e:
        print(f"Error in RAG processing: {e}")
        return f"""
          I'm experiencing some technical difficulties. Please try again, or if you need immediate help, 
          please contact Lifeline at 13 11 14 or emergency services at 000.
          """
        

enhanced_rag = EnhancedRAGWithWebSearch()

def process_input_with_fallback(user_input, conversation_history=[]):
    """
    Enhanced version of your existing function with intelligent web fallback
    """
    if not user_input or not isinstance(user_input, str):
        return "Please provide a valid question about mental health services."
    
    user_input = user_input.strip()
    if len(user_input) == 0:
        return "Please provide a question about mental health services."
    
    if len(user_input) > 1000:
        return "Your message is quite long. Please try to be more concise for better assistance."
    
    # Keep your mental health trigger validation
    try:
        validation_result = MentalHealthModel().validate_input(user_input)
        if validation_result.is_trigger:
            print(f"Mental health trigger detected - Category: {validation_result.category}")
            return validation_result.response
    except Exception as e:
        print(f"Mental health validation error: {e}")
    
    # Replace your RAG logic with the enhanced system
    try:
        return enhanced_rag.process_with_intelligent_fallback(
            user_input=user_input,
            conversation_history=conversation_history
        )
    except Exception as e:
        print(f"Enhanced RAG error: {e}")
        # Fallback to your original logic if enhanced system fails
        return process_input_with_retrieval_continuous(user_input, conversation_history)