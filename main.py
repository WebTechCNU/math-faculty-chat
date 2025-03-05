from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

import tiktoken
from langchain_openai import OpenAIEmbeddings
import numpy as np
import bs4
from langchain_community.document_loaders import WebBaseLoader

import os
from dotenv import load_dotenv

load_dotenv()

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'

langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_API_KEY'] = langchain_api_key

open_api_key = os.getenv("OPEN_API_KEY")

os.environ['OPENAI_API_KEY'] = open_api_key
os.environ['USER_AGENT'] = os.getenv("USER_AGENT")
USER_AGENT = os.getenv("USER_AGENT")

from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import pickle

embd = OpenAIEmbeddings()


app = FastAPI()

class Question(BaseModel):
    text: str

@app.post("/question")
def add_question(question: Question):
    # questions_db.append(question)
    with open(f"models/index.pkl", "rb") as f:
        stored_data = pickle.load(f)

    vectorstore = FAISS.load_local(folder_path="models/", embeddings=embd, allow_dangerous_deserialization=True)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5}) # number of documents retrieved

    # Prompt
    template = """Answer the question based only on the following context:
    {context}

    Please, provide as much information as possible!
    Do not say words like 'context'
    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    # LLM
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    result = rag_chain.invoke(question.text)
    return {"message": result}