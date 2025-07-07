import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from langchain.memory import ConversationBufferMemory
from langchain_mongodb import MongoDBChatMessageHistory
from serpapi import GoogleSearch
from pymongo.errors import ConnectionFailure

load_dotenv()
app = Flask(__name__)

# — Setup MongoDB-backed memory —
try:
    history = MongoDBChatMessageHistory(
        connection_string=os.getenv("MONGODB_URI"),
        session_id="user1"
    )
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=history
    )
    print("✅ MongoDB memory initialized.")
except ConnectionFailure:
    memory = None
    print("⚠️ MongoDB memory not initialized.")


def search_with_serpapi(q):
    params = {"engine":"google","q":q,"api_key":os.getenv("SERPAPI_API_KEY")}
    r = GoogleSearch(params).get_dict()
    if "answer_box" in r:
        return r["answer_box"].get("answer") or r["answer_box"].get("snippet", "")
    if r.get("organic_results"):
        return r["organic_results"][0].get("snippet", "")
    return "No results."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "").strip()
    print("📥 Received prompt:", prompt)

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # route to SerpAPI or Ollama
    if prompt.lower().startswith("search"):
        resp_text = search_with_serpapi(prompt[len("search"):].strip(" :"))
    else:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "WhiteRabbitNeo/WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B",
                "prompt": prompt,
                "stream": False
            }
        )
        if r.status_code != 200:
            print("❌ Ollama error:", r.text)
            return jsonify({"error": "LLM error"}), 500
        resp_text = r.json().get("response", "").strip()

    # save both user and assistant messages
    if memory:
        try:
            print(">> Saving to MongoDB memory...")
            memory.save_context({"input": prompt}, {"output": resp_text})
            print("✅ Save successful.")
        except Exception as e:
            print("⚠️ Memory save failed:", str(e))
    else:
        print("⚠️ No memory instance available; skipping save.")

    return jsonify({"response": resp_text})

if __name__ == "__main__":
    app.run(debug=False)
