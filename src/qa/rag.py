"""
Model
-----
This module defines AI-dependent functions.
"""
import os

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_cohere import ChatCohere
from database.build_qdrant import get_qdrant





template = """You are a helpful assistant named "Neuroscholar". You answer questions about papers based on the context.
If you receive a question that is not related to the papers or context, you should answer "Please ask another question".
Make sure to attach the title of the article that you relied on in the answer and attach a link to it
#################
Context: {context}
#################
Question:
{question}
#################
Answer: """

prompt = PromptTemplate(template=template, input_variables=[
                        "context", "question"])


def format_document(doc, index):
    text = doc["page_content"]
    title = doc["metadata"]["title"]
    link = doc["metadata"]["link"]
    authors = doc["metadata"]["authors"]

    return f"Document {index}:\nText: {text}\nTitle: {title}\nLink: {link}\nAuthors: {authors}\n"


def document_to_dict(document):
    return {"page_content": document.page_content, "metadata": document.metadata}


def retrieve(question: str):
    qdrant = get_qdrant()
    retriever = qdrant.as_retriever(
        search_kwargs={"k": 5}, score_threshold=0.8, verbose=True
    )
    retrieved_docs = retriever.get_relevant_documents(question)

    return [document_to_dict(doc) for doc in retrieved_docs]


def generate(context: str, question: str):
    prompt = PromptTemplate(template=template, input_variables=[
                            "context", "question"])
    llm_chain = LLMChain(
        prompt=prompt, llm=ChatCohere(
            cohere_api_key=os.environ["COHERE_API_KEY"])
    )  # TO DO singltone

    return llm_chain.run(question=question, context=context)
