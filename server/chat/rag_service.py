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
from path.to.enhanced_rag import EnchancedRAGWithWebSearch
from .Utils import *

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
        services_content = "\n".join(
            formatted_services) if formatted_services else "No specific services found for this query."

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


enhanced_rag = EnchancedRAGWithWebSearch()


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