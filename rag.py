from langchain_openai import OpenAIEmbeddings
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

def generate_rag_chain(model):
    # questions_db.append(question)
    with open(f"models/index.pkl", "rb") as f:
        stored_data = pickle.load(f)

    vectorstore = FAISS.load_local(folder_path="models/", embeddings=embd, allow_dangerous_deserialization=True)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5}) # number of documents retrieved

    # Prompt
    template = """Я є студентом або викладачем Чернівецького Національного 
    Університету, дай відповідь на наступне запитання, використовуючи 
    даний контекст:
    {context}

    Будь-ласка, дай якомога більше інформації!
    Не кажи слово 'контекст'
    Запитання: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    # LLM
    llm = ChatOpenAI(model_name=model, temperature=0)

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain