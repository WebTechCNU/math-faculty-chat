from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag import generate_rag_chain

app = FastAPI()

# ✅ CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or use full URL like "https://example.com"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models = {'3': 'gpt-3.5-turbo', '4': 'gpt-4o'}

class Question(BaseModel):
    text: str

@app.post("/4o/question")
def add_question(question: Question):
    rag_chain = generate_rag_chain(models['4'])
    result = rag_chain.invoke(question.text)
    return {"message": result}



@app.post("/3-5/question")
def add_question(question: Question):
    rag_chain = generate_rag_chain(models['3'])
    result = rag_chain.invoke(question.text)
    return {"message": result}