from .vectorstore import load_vectorstore

def get_retriever(persist_dir="chroma_db", k=10):
    vectorstore = load_vectorstore(persist_dir)
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever
