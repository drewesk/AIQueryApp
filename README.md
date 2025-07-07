# AIQueryApp

## LangChain Flask SerpAPI MongoDB Ollama Integration

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
_____

SerpAPI setup

1. Go to [serpapi.com](https://serpapi.com/), sign up.
2. Copy your API key.
3. Add to `.env`

MongoDB setup

1. Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas) and sign up.
2. Create a **free shared cluster**.
3. In **Database Access**, create a user with a username and password.
4. In **Network Access**, add IP `0.0.0.0/0` to allow all connections.
5. Click **Connect** → **Connect your application**.
6. Choose:
   - **Driver**: Python
   - **Version**: Latest (e.g. 3.12 or later)
7. Copy the connection auto-genearated string, then add to your `.env` file

____

5. **Run Ollama model server:**

   ```bash
   ollama serve
   ```

6. **Pull model:**

   `ollama pull WhiteRabbitNeo/WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B`

   or use your <modelname> of choice and then modify `app.py` to reflect the new Model Name.

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

> 💡 To activate real-time web search (instead of using the local LLM), **prefix your prompt with the word `search`**.

This bypasses the local language model and uses your SerpAPI key to fetch live results directly from Google Search.

---

#### ✅ Example Using `search` Keyword:

```bash
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt":"search the weather in NYC"}'
  ```

---

## Notes

- The app sends the prompt to the Ollama server API (`http://localhost:11434/api/generate`) to get AI responses.
- MongoDB stores the conversation history for persistent memory.
- SerpAPI is used internally for live search queries.

---

# MIT License | Open Source |

Copyright (c) 2025 Andrew Eskenazi

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
