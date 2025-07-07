import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from langchain_mongodb import MongoDBChatMessageHistory
from pymongo.errors import ConnectionFailure

load_dotenv()

app = Flask(__name__)

memory = None  # Default to None in case MongoDB fails
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
except ConnectionFailure as e:
    print("❌ Failed to connect to MongoDB:", str(e))
except Exception as e:
    print("❌ MongoDB setup error:", str(e))

# === Search Tool (SerpAPI) ===
search = SerpAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful for current events and online questions.",
    )
]

# === POST /chat — sends prompt to Ollama (localhost:11434) ===
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        prompt = data.get("prompt")
        print("📥 Received prompt:", prompt)

        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        # Send prompt to Ollama
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
            return jsonify({"response": answer})
        else:
            return jsonify({"error": "Failed to generate response", "details": response.text}), 500

    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
