import pandas as pd
import qdrant_client

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document


def load_data(filepath):
    """Load and preprocess the data."""
    data = pd.read_csv(filepath)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1024)
    documents = [
        Document(
            page_content=row["Abstract"],
            metadata={
                "link": row["Link"],
                "title": row["Title"],
                "authors": row["Authors"],
            }
        )
        for _, row in data.iterrows()
    ]
    return splitter.split_documents(documents)


def initialize_embeddings(model_name, device='cpu', normalize_embeddings=True):
    """Initialize the embeddings model."""
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': device},
        encode_kwargs={'normalize_embeddings': normalize_embeddings},
    )


def init_qdrant(documents, embeddings, url, collection_name):
    """Set up the Qdrant vector store with documents."""
    qdrant = Qdrant.from_documents(
        documents,
        embeddings,
        url=url,
        collection_name=collection_name,
    )
    return qdrant


def get_qdrant(model_name="intfloat/multilingual-e5-large", host="http://qdrant:6333", collection_name="papers"):
    embeddings = initialize_embeddings(model_name)

    client = qdrant_client.QdrantClient(
        host
    )
    qdrant = Qdrant(
        client=client, collection_name=collection_name,
        embeddings=embeddings,
    )
    return qdrant


def setup_qdrant(data_path="./database/papers.csv", model_name="intfloat/multilingual-e5-large", qdrant_url="http://qdrant:6333", collection_name="papers"):
    # Load and preprocess data
    documents = load_data(data_path)

    # Initialize embeddings
    embeddings = initialize_embeddings(model_name)

    # Set up Qdrant
    init_qdrant(documents, embeddings, qdrant_url, collection_name)

    print("Qdrant setup complete with the following collection:", collection_name)
