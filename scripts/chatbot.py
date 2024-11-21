import argparse
import os
import logging
import json
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Configuration
CHROMA_PATH = os.getenv("CHROMA_PATH", "chroma")
PROMPT_TEMPLATE = """
You are a Northwestern football coaching assistant. Your job is to provide clear, actionable, and expert advice based on the provided context. 
Always keep your answers relevant to football coaching, tactics, player development, and game strategies.

Context:
{context}

---

Coach's Question:
{question}

---

Your Expert Advice:
"""
RELEVANCE_THRESHOLD = 0.7

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FootballCoachAssistant")

def initialize_db(path, embedding_function):
    """Initialize the Chroma database."""
    try:
        return Chroma(persist_directory=path, embedding_function=embedding_function)
    except Exception as e:
        logger.error(f"Failed to initialize Chroma DB: {e}")
        raise

def search_db(db, query, k=3):
    """Search the Chroma database for the most relevant results."""
    try:
        return db.similarity_search_with_relevance_scores(query, k=k)
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise

def generate_prompt(context, question):
    """Generate a prompt for the football coaching assistant."""
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    return prompt_template.format(context=context, question=question)

def chatbot(query_text, relevance_threshold=0.7, results_count=3):

    # Initialize embeddings and database
    embedding_function = OpenAIEmbeddings()
    db = initialize_db(CHROMA_PATH, embedding_function)
    
    # Perform similarity search in the database
    results = search_db(db, query_text, k=results_count)
    if len(results) == 0 or results[0][1] < relevance_threshold:
        print("Unable to find matching results. Please refine your query.")
        return

    # Extract and format the context
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
    if not context_text.strip():
        print("No valid context retrieved.")
        return

    # Generate the prompt and make a prediction
    prompt = generate_prompt(context=context_text, question=query_text)
    model = ChatOpenAI(model="gpt-4o")
    response_text = model.predict(prompt)

    # Format and display the response
    sources = [doc.metadata.get("source") for doc, _ in results if doc.metadata.get("source")]
    formatted_response = {
        "response": response_text,
        "sources": sources
    }
    return formatted_response
