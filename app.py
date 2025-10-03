from flask import Flask, request, jsonify, render_template
from qa.chain import build_qa_chain

app = Flask(__name__)
qa = build_qa_chain(persist_dir="chroma_db")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        query = request.form.get("query")
        result = qa.invoke(query)   # ✅ instead of qa.run(query)
        answer = result['result']  # invoke returns a dict
        return render_template("index.html", query=query, answer=answer)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

