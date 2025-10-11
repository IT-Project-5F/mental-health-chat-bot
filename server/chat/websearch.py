import os
from typing import List, Dict, Optional
from langchain_tavily import TavilySearch
from langchain.agents import Tool
from dotenv import load_dotenv
import logging
import json
from .Utils import *

load_dotenv()
logger = logging.getLogger(__name__)

class LangChainTavilySearch:
    def __init__(self):
        """Initialize Tavily through LangChain"""
        api_key = os.getenv('TAVILY_API_KEY')
        if not api_key:
            logger.warning("Tavily API key not found")
            self.search_tool = None
        else:
            # Initialize LangChain's Tavily tool
            self.search_tool = TavilySearch(
                max_results=5,
                search_depth="advanced",
                include_domains=[
                    "health.gov.au",
                    "beyondblue.org.au", 
                    "headspace.org.au",
                    "lifeline.org.au",
                    "blackdoginstitute.org.au",
                    "sane.org",
                    "mindspot.org.au"
                ],
                include_answer=True,
                include_raw_content=False
            )
    
    def search(self, query: str, require_mental_health: bool = True) -> List[Dict]:
        """
        Perform web search using LangChain's Tavily integration
        """
        if not self.search_tool:
            logger.error("Tavily search tool not initialized")
            return []
        
        try:
            if require_mental_health:
                enhanced_query = f"{query} mental health australia services support"
            else:
                enhanced_query = query
            
            # Execute search through LangChain
            results = self.search_tool.invoke({"query": enhanced_query})
            
            if isinstance(results, str):
                try:
                    results = json.loads(results)
                except:
                    # If it's not JSON, wrap it
                    return [{
                        'title': 'Search Result',
                        'content': results,
                        'url': 'Web Search',
                        'score': 0.5
                    }]
            
            formatted_results = []
            for result in results:
                if isinstance(result, dict):
                    formatted_results.append({
                        'title': result.get('title', 'No title'),
                        'content': result.get('content', result.get('snippet', '')),
                        'url': result.get('url', ''),
                        'score': result.get('score', 0.5)
                    })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Tavily search error: {str(e)}")
            return []
    
    def format_for_llm(self, results: List[Dict]) -> str:
        """Format search results for LLM consumption"""
        if not results:
            return "No web search results available."
        
        formatted = "Web Search Information:\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"[{i}] {result['title']}\n"
            formatted += f"    {result['content'][:200]}...\n"
            formatted += f"    Source: {result['url']}\n\n"
        
        return formatted


class EnhancedRAGWithWebSearch:
    """
    Main RAG service with automatic fallback to web search
    """
    def __init__(self):
        self.web_search = LangChainTavilySearch()
        self.min_confidence_threshold = 0.3
        self.empty_result_threshold = 0.1
        
    def assess_rag_quality(self, docs: List[Dict], user_query: str) -> Dict:
        """
        Assess if RAG results are sufficient for the query
        
        Returns dict with:
        - needs_web_search: bool
        - confidence: float
        - reason: str
        """
        # No results at all
        if not docs:
            return {
                'needs_web_search': True,
                'confidence': 0.0,
                'reason': 'No matching services found in database'
            }
        
        # Check for empty or minimal content
        total_content = sum(
            len(str(doc.get('service_name', ''))) +
            len(str(doc.get('notes', ''))) +
            len(str(doc.get('organisation_name', '')))
            for doc in docs
        )
        
        if total_content < 50:  # Very little actual content
            return {
                'needs_web_search': True,
                'confidence': 0.1,
                'reason': 'Database results have minimal information'
            }
        
        # Check if results have actionable information
        has_contact = any(
            doc.get('phone') or doc.get('email') or doc.get('website')
            for doc in docs
        )
        
        has_service_details = any(
            doc.get('service_name') and doc.get('organisation_name')
            for doc in docs
        )
        
        # Query asks for general information not in database
        general_info_keywords = [
            'what is', 'how does', 'explain', 'symptoms', 
            'treatment', 'causes', 'types of', 'difference between',
            'latest', 'recent', 'new', 'research'
        ]
        
        query_lower = user_query.lower()
        asks_general_info = any(keyword in query_lower for keyword in general_info_keywords)
        
        # Calculate confidence score
        confidence = 0.0
        if has_contact:
            confidence += 0.4
        if has_service_details:
            confidence += 0.3
        if len(docs) >= 3:
            confidence += 0.3
            
        # Determine if web search needed
        needs_web = False
        reason = "Database has sufficient information"
        
        if confidence < self.min_confidence_threshold:
            needs_web = True
            reason = "Low confidence in database results"
        elif asks_general_info and confidence < 0.7:
            needs_web = True
            reason = "Query requires general information beyond service listings"
        elif not has_contact and not has_service_details:
            needs_web = True
            reason = "Database results lack actionable information"
            
        return {
            'needs_web_search': needs_web,
            'confidence': confidence,
            'reason': reason
        }
    
    def process_with_intelligent_fallback(
        self, 
        user_input: str, 
        conversation_history: List = []
    ) -> str:
        """
        Process query with automatic web search when RAG is insufficient
        """
        logger.info(f"Processing query: {user_input[:100]}...")
        
        from chat.rag_service import get_embeddings_vector, get_top3_similar_docs
        
        query_embedding = get_embeddings_vector(user_input)
        rag_docs = get_top3_similar_docs(query_embedding, k=3)
        
        assessment = self.assess_rag_quality(rag_docs, user_input)
        logger.info(f"RAG Assessment: {assessment}")
        
        context_parts = []
        sources_used = []
        
        if rag_docs:
            context_parts.append("=== Database Services ===")
            context_parts.append(self.format_rag_docs(rag_docs))
            sources_used.append("database")
        
        if assessment['needs_web_search']:
            logger.info(f"Triggering web search: {assessment['reason']}")
            
            web_results = self.web_search.search(user_input)
            
            if web_results:
                context_parts.append("\n=== Web Search Information ===")
                context_parts.append(self.web_search.format_for_llm(web_results))
                sources_used.append("web")
                
                # Add disclaimer
                context_parts.append(
                    "\nNote: Web information should be verified with official services."
                )
        
        full_context = "\n".join(context_parts) if context_parts else "No information found."
        
        system_message = f"""
        You are a helpful mental health services assistant for Australia.
        
        Current situation:
        - RAG Confidence: {assessment['confidence']:.1%}
        - Reason for approach: {assessment['reason']}
        - Sources used: {', '.join(sources_used) if sources_used else 'none'}
        
        Instructions:
        1. If database has specific services, prioritize those with contact details
        2. If using web information, mention it's from online sources
        3. If no good matches found, be honest and suggest alternatives
        4. Always be supportive and provide crisis resources if needed
        """
        
        from chat.rag_service import get_completion_from_messages
        
        messages = [
            {"role": "system", "content": system_message},
            *conversation_history[-10:],  # Last 10 messages for context
            {"role": "user", "content": f"Query: {user_input}\n\nAvailable Information:\n{full_context}"}
        ]
        
        response = get_completion_from_messages(messages)
        
        # Add source attribution if we used web
        if 'web' in sources_used and 'database' not in sources_used:
            response += "\n\n*This information was retrieved from web sources as no specific services were found in our database. Please verify details directly with the services.*"
        elif 'web' in sources_used and 'database' in sources_used:
            response += "\n\n*Response includes both database services and supplementary web information.*"
            
        return response
    
    def format_rag_docs(self, docs: List[Dict]) -> str:
        """Format RAG documents for context"""
        if not docs:
            return "No services found in database."
            
        formatted = []
        for i, doc in enumerate(docs, 1):
            service_info = f"Service {i}:\n"
            
            fields = [
                ('Organisation', 'organisation_name'),
                ('Service', 'service_name'),
                ('Phone', 'phone'),
                ('Email', 'email'),
                ('Website', 'website'),
                ('Address', 'address'),
                ('Notes', 'notes')
            ]
            
            for label, field in fields:
                if doc.get(field):
                    service_info += f"  {label}: {doc[field]}\n"
                    
            formatted.append(service_info)
            
        return "\n".join(formatted)