import psycopg2
import numpy as np
from pgvector.psycopg2 import register_vector
from langchain_openai import OpenAIEmbeddings
import openai
import os
from dotenv import load_dotenv

load_dotenv() 
openai_client = openai.OpenAI()

conn = psycopg2.connect(
    host = os.getenv('POSTGRES_HOST', 'postgres'),       
    database = os.getenv('POSTGRES_DB', 'mental_health_db'),
    user = os.getenv('POSTGRES_USER', 'mental_health_user'),
    password = os.getenv('POSTGRES_PASSWORD', 'password'),
    port = os.getenv('POSTGRES_PORT', '5432'), 
)

def get_top3_similar_docs(query_embedding, conn):
    embedding_array = np.array(query_embedding)
    register_vector(conn)
    cur = conn.cursor()
    cur.execute("SELECT record_index FROM MentalHealthEmbeddings ORDER BY embedding <=> %s LIMIT 3", (embedding_array,))
    top3_indexes = cur.fetchall()
    top3_indexes_flat = tuple(idx[0] for idx in top3_indexes)
    cur.execute("SELECT * FROM MentalHealthRawData WHERE id in %s", (top3_indexes_flat, ))
    top_3_docs = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    record = [dict(zip(colnames, doc)) for doc in top_3_docs]
    return record

def get_completion_from_messages(messages, model="gpt-4o", temperature=0, max_tokens=1000):
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )
    return response.choices[0].message.content

def get_embeddings_vector(text): 
  embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
  response = embedding_model.embed_query(text)
  return response

def process_input_with_retrieval_continuous(user_input, conversation_history=[]):
    delimiter = "```"

    related_docs = get_top3_similar_docs(get_embeddings_vector(user_input), conn)

    system_message = f"""
    You are a friendly chatbot. \
    You can answer questions about mental health services. \
    You respond in a concise, technically credible tone. \
    Use the conversation history to maintain context and provide personalized responses. \
    Reference previous conversations when relevant.
    """
    
    # Build message history for context
    messages = [{"role": "system", "content": system_message}]
    
    # Add conversation history (limit to last 10 messages to manage token usage)
    recent_history = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
    messages.extend(recent_history)
    
    # Add current user input and retrieved documents
    messages.extend([
        {"role": "user", "content": f"{delimiter}{user_input}{delimiter}"},
        {"role": "assistant", "content": f"Relevant mental health services information: \n {related_docs[0]} \n {related_docs[1]} {related_docs[2]}"}   
    ])

    final_response = get_completion_from_messages(messages)
    return final_response