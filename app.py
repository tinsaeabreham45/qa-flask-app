from flask import Flask, render_template, request, redirect, session
from qa.chain import build_qa_chain
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # for session management, change in production

qa_chain = None  # Will be initialized after getting API key

@app.route("/", methods=["GET", "POST"])
def home():
    global qa_chain

    # Step 1: Get API Key
    if "api_key" not in session:
        if request.method == "POST" and "api_key" in request.form:
            session["api_key"] = request.form["api_key"]
            # Build QA chain immediately
            qa_chain = build_qa_chain(persist_dir="chroma_db", gemini_api_key=session["api_key"])
            return redirect("/")
        return render_template("get_api.html")

    # Ensure qa_chain is built if not already
    if qa_chain is None and "api_key" in session:
        qa_chain = build_qa_chain(persist_dir="chroma_db", gemini_api_key=session["api_key"])

    # Step 2: Query QA
    if request.method == "POST":
        query = request.form.get("query")
        result = qa_chain.invoke(query)
        answer = result['result']
        return render_template("index.html", query=query, answer=answer)

    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
