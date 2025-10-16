import sys
import os
from .Prompt_Generator import PromptGenerator
from .Validator import MentalHealthModel as GuardRailModel
from .Utils import *
from typing import Tuple
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def process_input_with_retrieval_continuous(user_input, conversation_history=[]) -> Tuple[str, int]:
    """
    Process user input with mental health validation and detailed service retrieval.
    """
    # Input validation
    if not user_input or not isinstance(user_input, str):
        return "Please provide a valid question about mental health services.", -1

    user_input = user_input.strip()
    if len(user_input) == 0:
        return "Please provide a question about mental health services.", -1

    if len(user_input) > 1000:
        return "Your message is quite long. Please try to be more concise for better assistance.", -1

    # Mental health validation using our new model
    try:
        validation_result = GuardRailModel().validate_input(user_input)
        if validation_result.is_trigger:
            # Log the trigger for monitoring
            print(f"Mental health trigger detected - Category: {validation_result.category}, "
                  f"Word: '{validation_result.matched_word}', Confidence: {validation_result.confidence:.2f}")

            # Return the mental health response immediately
            return validation_result.response, -1
    except Exception as e:
        print(f"Mental health validation error: {e}")
        # Continue with normal processing if validation fails

    # Continue with normal RAG processing
    try:

        # Get embeddings for the user input
        query_embedding = get_embeddings_vector(user_input)
        if query_embedding is None:
            return "I'm having trouble processing your request. Please try again.", -1

        # Get similar documents with full service details
        related_docs = get_topk_similar_docs(query_embedding)


        SIMILARITY_THRESHOLD = 0.8
        # Format the service information for better readability
        formatted_services = []
        counter = 0
        for docs_tuple in related_docs:
            score = docs_tuple['similarity']
            doc = docs_tuple['service']
            if score < SIMILARITY_THRESHOLD :
              continue
            service_text = f"Service {counter + 1}:\n"
            counter = counter + 1
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
        system_message = PromptGenerator.generate_system_prompt()
        # Build message history for context
        messages = [{"role": "system", "content": system_message}]

        # Add conversation history (limit to last 10 messages to manage token usage)
        recent_history = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
        messages.extend(recent_history)
        services_content = "\n".join(
            formatted_services) if formatted_services else "No specific services found for this query."

        user_message = PromptGenerator.generate_local_search_user_prompt(services_content, user_input)
        messages.append({"role": "user", "content": user_message})
        final_response = get_completion_from_messages(messages)
        return final_response, len(formatted_services)

    except Exception as e:
        print(f"Error in RAG processing: {e}")
        return f"""
          I'm experiencing some technical difficulties. Please try again, or if you need immediate help, 
          please contact Lifeline at 13 11 14 or emergency services at 000.
          """, -1

def combine_local_and_web(local_response: str, web_results: List[Dict], user_input: str) -> str:
    """
    Combine local RAG response with web search results
    """
    try:
        system_message = PromptGenerator.generate_system_prompt()
        messages = [{"role": "system", "content": system_message}]
        user_message = PromptGenerator.generate_web_and_local_search_user_prompt(local_response, web_results, user_input)
        messages.append({"role": "user", "content": user_message})
        final_response = get_completion_from_messages(messages)
        return final_response

    except Exception as e:
        print(f"Error combining responses: {e}")
        # Fallback to local response with web sources mentioned
        web_sources = [result['source'] for result in web_results]
        return f"{local_response}\n\nAdditional resources: {', '.join(web_sources)}"

def process_with_intelligent_fallback(user_input: str, conversation_history: List[Dict] = None) -> str:
    """
    Main method that processes user input with intelligent fallback to web search
    """
    RELATED_DOCUMENTS_THRESHOLD = 3

    if conversation_history is None:
        conversation_history = []
    try:
        # First try local RAG
        local_response, num_related_docs = process_input_with_retrieval_continuous(user_input, conversation_history)
        if num_related_docs == -1:
            return local_response
        if num_related_docs >= RELATED_DOCUMENTS_THRESHOLD:
            return local_response
        if check_require_web_search(user_input):
            web_results = web_search(user_input)
            if web_results:
                enhanced_response = combine_local_and_web(local_response, web_results, user_input)
                return enhanced_response
        return local_response

    except Exception as e:
        print(f"Enhanced RAG error: {e}")
        # Fallback to local RAG
        return process_input_with_retrieval_continuous(user_input, conversation_history)[0]


