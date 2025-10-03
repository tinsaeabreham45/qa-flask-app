from qa.chain import build_qa_chain
from flask import Flask, request, jsonify


app = Flask(__name__)

qa = build_qa_chain()

@app.route("/ask", methods=["POST"])
def ask():
    query = request.json.get("query")
    answer = qa.run(query)
    return jsonify({"answer": answer})
