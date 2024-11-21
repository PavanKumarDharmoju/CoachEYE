import os
import logging
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Configuration
CHROMA_PATH = os.getenv("CHROMA_PATH", "chroma")
PROMPT_TEMPLATE = """
You are an expert Northwestern football coaching assistant with deep knowledge of:
- Modern offensive and defensive strategies
- Player development and training techniques
- Game analysis and tactical planning
- Northwestern's specific football program, culture, and historical strengths

Coaching Principles:
- Provide evidence-based, strategic recommendations
- Focus on player development and team performance
- Offer actionable, specific insights
- Consider both short-term tactics and long-term program growth

Context Provided:
{context}
---
Specific Coaching Challenge or Question:
{question}
---
Comprehensive Coaching Response Guidelines:
1. Analyze the situation thoroughly
2. Provide clear, strategic recommendations
3. Explain the rationale behind each suggestion
4. Include potential implementation steps
5. Highlight potential challenges and mitigation strategies

Expert Coaching Advice:
"""
RELEVANCE_THRESHOLD = 0.7

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("soccerCoachAssistant")


def initialize_db():
    """Initialize the Chroma database."""
    try:
        embedding_function = OpenAIEmbeddings()
        return Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    except Exception as e:
        logger.error(f"Failed to initialize Chroma DB: {e}")
        raise


def search_db(db, query, k=3, relevance_threshold=RELEVANCE_THRESHOLD):
    """Search the Chroma database for the most relevant results."""
    try:
        results = db.similarity_search_with_relevance_scores(query, k=k)
        return [
            (doc.page_content, doc.metadata.get("source"), score)
            for doc, score in results if score >= relevance_threshold
        ]
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise


def generate_response(context, question):
    """Generate an expert coaching response."""
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context, question=question)
    model = ChatOpenAI(model="gpt-4o")
    return model.predict(prompt)


def create_chatbot():
    """Factory function to create the chatbot object."""
    db = initialize_db()
    model = ChatOpenAI(model="gpt-4o", temperature=0)

    def chatbot(inputs):
        query_text = inputs.get("question", "")

        # First, search the database for relevant documents
        try:
            results = search_db(db, query_text)
            logger.info(f"Found {len(results)} relevant documents.")
        except Exception as e:
            logger.error(f"Error during search: {e}")
            results = []

        if results:
            # Use the retrieved context to generate a response
            context_text = "\n\n---\n\n".join([r[0] for r in results])
            response = generate_response(context=context_text, question=query_text)
            sources = [r[1] for r in results if r[1]]

            return {"answer": response, "sources": sources}

        else:
            # Generate a conversational response if no relevant documents are found
            logger.info("No relevant documents found. Generating a conversational response.")
            fallback_prompt = (
                f"You are a friendly Northwestern soccer coaching assistant. You found No relevant documents during retrieval"
                f"Someone just said: '{query_text}'. Please respond helpfully."
            )
            response = model.predict(fallback_prompt)
            return {"answer": response, "sources": []}

    return chatbot
