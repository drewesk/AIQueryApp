import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from langchain.memory import ConversationBufferMemory
from langchain_mongodb import MongoDBChatMessageHistory
from pymongo.errors import ConnectionFailure

from serpapi import GoogleSearch  # Official SerpAPI SDK

load_dotenv()

app = Flask(__name__)

memory = None
chat_history = None

# === MongoDB Memory Setup ===
try:
    mongo_url = os.getenv("MONGODB_URI")
    chat_history = MongoDBChatMessageHistory(
        connection_string=mongo_url,
        session_id="user1"
    )
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=chat_history
    )
    print("✅ MongoDB connection established.")
except ConnectionFailure:
    # Just ignore ConnectionFailure silently (like SSL handshake errors)
    pass
except Exception as e:
    # For other exceptions, still print (optional)
    print("❌ MongoDB setup error:", str(e))

# === SerpAPI Search Function ===
def search_with_serpapi(query: str) -> str:
    print(f"🔍 Running SerpAPI search for: {query}")

    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return "❌ SerpAPI API key not configured."

    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    # Debug: print full raw JSON from SerpAPI to console
    print("🔎 Full SerpAPI results JSON:")
    import json
    print(json.dumps(results, indent=2))

    answer = ""
    source_url = ""

    if "answer_box" in results:
        answer = results["answer_box"].get("answer") or results["answer_box"].get("snippet", "")
        source_url = results["answer_box"].get("link", "")
    elif "organic_results" in results and len(results["organic_results"]) > 0:
        answer = results["organic_results"][0].get("snippet", "")
        source_url = results["organic_results"][0].get("link", "")
    else:
        answer = "No good search results found."

    # Append the source URL to the answer for reference
    if source_url:
        answer += f"\n\n(Source: {source_url})"

    print(f"✅ SerpAPI returned: {answer}")
    return answer

# === Flask route ===
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        prompt = data.get("prompt")
        print("📥 Received prompt:", prompt)

        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        # If prompt starts with 'search', use SerpAPI
        if prompt.lower().startswith("search"):
            query = prompt[len("search"):].strip(" :")
            result = search_with_serpapi(query)
            return jsonify({"response": result})

        # Otherwise, send to Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "WhiteRabbitNeo/WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B",
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code == 200:
            result = response.json()
            answer = result.get("response", "").strip()

            # ✅ Only save if memory is initialized
            if memory:
                try:
                    memory.save_context({"input": prompt}, {"output": answer})
                except Exception as e:
                    print("⚠️ Failed to save context to MongoDB:", str(e))

            return jsonify({"response": answer})
        else:
            return jsonify({"error": "Failed to generate response", "details": response.text}), 500

    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=False)
