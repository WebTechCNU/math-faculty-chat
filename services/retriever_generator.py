from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import pickle


class RetrieverGenerator:
    def __init__(self):
        load_dotenv()
        os.environ['LANGCHAIN_TRACING_V2'] = 'true'
        os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'

        langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
        os.environ['LANGCHAIN_API_KEY'] = langchain_api_key

        open_api_key = os.getenv("OPEN_API_KEY")

        os.environ['OPENAI_API_KEY'] = open_api_key
        os.environ['USER_AGENT'] = os.getenv("USER_AGENT")
        USER_AGENT = os.getenv("USER_AGENT")

        self.embd = OpenAIEmbeddings()

        self.vectorstore = FAISS.load_local(folder_path="models/", embeddings=self.embd, allow_dangerous_deserialization=True)

        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5}) # number of documents retrieved


