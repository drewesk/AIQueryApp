<!-- Generated Using ChatGPT -->

# LangChain Flask SerpAPI MongoDB Ollama Integration

This is a simple Flask app that connects to:

- An Ollama AI model server
- SerpAPI for web search
- MongoDB for persistent chat memory

## Setup Instructions

1. **Clone the repo:**

   ```bash
   git clone <repo-url>
   cd langchain_flask_serpapi_mongo
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file with:

   ```
   SERPAPI_API_KEY=your_serpapi_api_key
   MONGODB_URI=your_mongodb_connection_string
   ```

5. **Run Ollama model server:**

   ```bash
   ollama serve
   ```

6. **Run your model:**

   ```bash
   ollama run WhiteRabbitNeo/WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B
   ```

   (If you don’t have the model locally, Ollama will download it automatically.)

7. **Run the Flask app:**

   ```bash
   python app.py
   ```

8. **Send POST requests to the Flask app `/chat` endpoint with JSON body:**

   ```json
   {
     "prompt": "Your question here"
   }
   ```

   Example using `curl`:

   ```bash
   curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"prompt":"What is the weather in NYC?"}'
   ```

---

## Notes

- The app sends the prompt to the Ollama server API (`http://localhost:11434/api/generate`) to get AI responses.
- MongoDB stores the conversation history for persistent memory.
- SerpAPI is used internally for live search queries.

---
