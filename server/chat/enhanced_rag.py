import os
import openai
import requests
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class EnhancedRAGWithWebSearch:
    """
    Enhanced RAG system with intelligent web search fallback for mental health support
    """

    def __init__(self):
        self.openai_client = openai.OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
        self.web_search_api_key = os.getenv("SERPER_API_KEY")  # Using Serper for web search

    def process_with_intelligent_fallback(self, user_input: str, conversation_history: List[Dict] = None) -> str:
        """
        Main method that processes user input with intelligent fallback to web search
        """
        if conversation_history is None:
            conversation_history = []

        try:
            # First try local RAG
            local_response = self._try_local_rag(user_input, conversation_history)

            # If local RAG fails or we need web search, supplement with web search
            if self._needs_web_search(user_input) and self.web_search_api_key:
                web_results = self._web_search(user_input)
                if web_results:
                    enhanced_response = self._combine_local_and_web(local_response, web_results, user_input)
                    return enhanced_response

            return local_response

        except Exception as e:
            print(f"Enhanced RAG error: {e}")
            # Fallback to local RAG
            return self._try_local_rag(user_input, conversation_history)

    def _try_local_rag(self, user_input: str, conversation_history: List[Dict] = None) -> str:
        """
        Try to answer using local RAG system
        """
        try:
            # Import the existing RAG function to avoid circular imports
            from .rag_service import process_input_with_retrieval_continuous
            return process_input_with_retrieval_continuous(user_input, conversation_history or [])
        except Exception as e:
            print(f"Local RAG error: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again or contact support if the issue persists."

    def _needs_web_search(self, user_input: str) -> bool:
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

    def _web_search(self, query: str) -> List[Dict]:
        """
        Perform web search for mental health information
        """
        if not self.web_search_api_key:
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
                "X-API-KEY": self.web_search_api_key,
                "Content-Type": "application/json"
            }

            response = requests.post(url, json=payload, headers=headers, timeout=10)

            if response.status_code == 200:
                results = response.json()
                return self._process_search_results(results)
            else:
                print(f"Web search API error: {response.status_code}")
                return []

        except Exception as e:
            print(f"Web search error: {e}")
            return []

    def _process_search_results(self, search_results: Dict) -> List[Dict]:
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

    def _is_mental_health_relevant(self, result: Dict) -> bool:
        """
        Check if search result is relevant to mental health
        """
        relevant_domains = [
            "nih.gov", "nimh.nih.gov", "cdc.gov", "samhsa.gov", "psychologytoday.com",
            "nami.org", "mentalhealth.gov", "who.int", "apa.org", "therapist.com",
            "betterhelp.com", "talkspace.com", "psychcentral.com", "webmd.com",
            "mayo.clinic", "clevelandclinic.org"
        ]

        link = result.get("link", "").lower()
        title = result.get("title", "").lower()
        snippet = result.get("snippet", "").lower()

        # Check if domain is relevant
        domain_relevant = any(domain in link for domain in relevant_domains)

        # Check if content mentions mental health
        content_relevant = any(term in (title + snippet) for term in [
            "mental health", "therapy", "counseling", "depression", "anxiety",
            "psychiatr", "psycholog", "wellness", "support", "crisis", "suicide"
        ])

        return domain_relevant or content_relevant

    def _combine_local_and_web(self, local_response: str, web_results: List[Dict], user_input: str) -> str:
        """
        Combine local RAG response with web search results
        """
        try:
            # Create context from web results
            web_context = "\n".join([
                f"From {result['source']}: {result['snippet']}"
                for result in web_results
            ])

            # Use GPT to synthesize information
            synthesis_prompt = f"""
            You are a mental health support assistant. Combine the following information to provide a comprehensive, helpful response.

            User Question: {user_input}

            Local Database Response: {local_response}

            Additional Web Information:
            {web_context}

            Provide a unified response that:
            1. Prioritizes the local database information as it's specifically curated for mental health
            2. Supplements with relevant web information where helpful
            3. Maintains a supportive, professional tone
            4. Includes resource links when appropriate
            5. Stays focused on mental health support
            
            Output requirements:
            - Use plain text only (no Markdown, asterisks, or special formatting symbols).
            - Use clear field labels to highlight key information (for example: ORGANISATION, ADDRESS, PHONE, EMAIL, WEBSITE, SERVICE TYPE, COST, HOURS).
            - Keep the layout easy to scan and visually organized. 
            Response:
            """

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": synthesis_prompt}],
                max_tokens=500,
                temperature=0.3
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error combining responses: {e}")
            # Fallback to local response with web sources mentioned
            web_sources = [result['source'] for result in web_results]
            return f"{local_response}\n\nAdditional resources: {', '.join(web_sources)}"