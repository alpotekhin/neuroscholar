"""
Model
-----
This module defines AI-dependent functions.
"""
import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

import qdrant_client
from langchain_community.vectorstores import Qdrant
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_cohere import ChatCohere

from database.build_qdrant import get_qdrant

import getpass
import os



template = """Analyze the context of the question and identify key themes, concepts, and information requests.
Utilize natural language processing algorithms to comprehend the meaning of the question and associated data.
Formulate a response to the question based on the analysis of the context and the extracted data.
Verify the formulated response for relevance to the query and its comprehensibility for the user.
Provide the response to the user, taking into account the wording of the question and preferences in conveying information.
Make sure to indicate the title of the article that you relied on in the answer and attach a link to it
==================
Context: {context}
==================
Question:
{question}
==================
Answer: """

prompt = PromptTemplate(template=template, input_variables=["context","question"])

def format_document(doc, index):
    text = doc.page_content
    title = doc.metadata["title"]
    link = doc.metadata["link"]
    authors = doc.metadata["authors"]
    
    return f"Document {index}:\nText: {text}\nTitle: {title}\nLink: {link}\nAuthors: {authors}\n"

def retrieve(question: str):
    qdrant = get_qdrant()
    # print("\n\nqdrant activated", qdrant, "\n\n")
    retriever = qdrant.as_retriever(search_kwargs={"k": 5}, score_threshold=0.8,verbose=True)
    retrieved_doc = retriever.get_relevant_documents(question)
    # print("\n\nretrieved_doc", retrieved_doc, "\n\n")
    
    return retrieved_doc

def generate(context: str, question: str):
    prompt = PromptTemplate(template=template, input_variables=["context","question"])
    llm_chain = LLMChain(prompt=prompt, llm=ChatCohere(cohere_api_key=os.environ["COHERE_API_KEY"]))
    
    return llm_chain.run(question=question, context=context)

