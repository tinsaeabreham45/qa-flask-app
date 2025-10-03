from flask import Flask, render_template, request, redirect, session
from qa.chain import build_qa_chain
import os
app = Flask(__name__)
app.secret_key = "supersecretkey"  # For session management

qa_chain = None  # Will be initialized after getting API key

@app.route("/", methods=["GET", "POST"])
def home():
    global qa_chain

    # Step 1: Get API Key
    if "api_key" not in session:
        if request.method == "POST" and "api_key" in request.form:
            session["api_key"] = request.form["api_key"]
            qa_chain = build_qa_chain(persist_dir="chroma_db", gemini_api_key=session["api_key"])
            return redirect("/")
        return render_template("get_api.html")

    # Ensure qa_chain exists
    if qa_chain is None and "api_key" in session:
        qa_chain = build_qa_chain(persist_dir="chroma_db", gemini_api_key=session["api_key"])

    # Step 2: Query QA
    if request.method == "POST" and "query" in request.form:
        query = request.form.get("query")
        result = qa_chain.invoke(query)
        answer = result['result']
        return render_template("index.html", query=query, answer=answer)

    return render_template("index.html")
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # use Render's assigned port
    app.run(host="0.0.0.0", port=port)