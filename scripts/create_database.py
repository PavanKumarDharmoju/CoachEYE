import logging
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai
from dotenv import load_dotenv
import os
import shutil
import nltk

# Download NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()

#---- Set OpenAI API key 
# Change environment variable name from "OPENAI_API_KEY" to the name given in 
# your .env file.
openai.api_key = os.environ['OPENAI_API_KEY']

CHROMA_PATH = "../chroma"
DATA_PATH = "../data_processed/"


def main():
    logging.info("Starting the process...")
    try:
        generate_data_store()
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)


def generate_data_store():
    logging.info("Generating data store...")
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    logging.info(f"Loading documents from {DATA_PATH}...")
    loader = DirectoryLoader(DATA_PATH, glob="*.txt")
    documents = loader.load()
    logging.info(f"Loaded {len(documents)} documents.")
    return documents


def split_text(documents: list[Document]):
    logging.info("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    logging.info(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10]
    logging.debug(f"Example chunk content: {document.page_content}")
    logging.debug(f"Example chunk metadata: {document.metadata}")

    return chunks


def save_to_chroma(chunks: list[Document]):
    logging.info("Saving chunks to Chroma...")
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        logging.info(f"Clearing existing Chroma database at {CHROMA_PATH}...")
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()
    logging.info(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()
