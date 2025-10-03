from langchain.chains import RetrievalQA
from .retriever import get_retriever
import os
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import init_chat_model

load_dotenv(find_dotenv())
api_key = os.getenv("GOOGLE_API_KEY")
llm_model = "gemini-2.0-flash"


def build_qa_chain(persist_dir="chroma_db"):
    retriever = get_retriever(persist_dir)
    
    llm = init_chat_model(llm_model, model_provider="google_genai")
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        verbose = True
    )
    return qa_chain


# if __name__ == "__main__":
#     query = "Who is allowed for taking Re-examinations?"
#     chain = build_qa_chain()
#     result = chain.invoke(query)
#     print("Type of result:", type(result))
#     print(result)