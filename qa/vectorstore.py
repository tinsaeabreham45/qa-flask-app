from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def load_vectorstore(persist_dir="chroma_db"):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory=persist_dir
    )
    return vectorstore

