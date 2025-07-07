# AI Query App

## LangChain Flask SerpAPI MongoDB Ollama Integration

This is a simple Flask app that connects to:

- An Ollama AI model server
- SerpAPI for web search
- MongoDB for persistent chat memory

## Setup Instructions

1. **Clone the repo:**

   ```bash
   git clone https://github.com/drewesk/AIQueryApp.git
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

   `ollama run WhiteRabbitNeo/WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B`

   or

   `ollama pull <modelname>`

   and then update app.py to reflect this new model.

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

# MIT License | Open Source USE!

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy  
of this software and associated documentation files (the "Software"), to deal  
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all  
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  
SOFTWARE.
