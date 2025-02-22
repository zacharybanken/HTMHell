from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import os

# FastAPI app initialization
app = FastAPI()

# Enable CORS
origins = [
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Route to serve index.html
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

USE_LOCAL_LLM = True
OLLAMA_URL = "http://localhost:11434/api/generate"
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_API_KEY = "your_api_key_here"

@app.post("/generate_html/")
async def generate_html(request: Request):
    data = await request.json()
    current_html = data.get("html", "")
    clicked_id = data.get("clicked_id", "")
    
    prompt = f"""
    You are an AI that dynamically generates web pages. 
    The current page is the following HTML:
    {current_html}
    
    The user clicked on the element with ID: {clicked_id}.
    Generate the next short page in valid HTML format.
    Include a few links and some creative content.
    Only include the HTML page in your response.
    No preface. No explanation. No sign-off.
    """
    
    if USE_LOCAL_LLM:
        print("sending to local LLM...")
        response = requests.post(OLLAMA_URL, json={"model": "llama2", "prompt": prompt})
        
        # Handle streaming response from Ollama
        generated_html = ""
        try:
            # Split response into lines and process each JSON object
            for line in response.text.strip().split('\n'):
                if line:
                    try:
                        json_response = json.loads(line)
                        # Accumulate the response text
                        if 'response' in json_response:
                            generated_html += json_response['response']
                    except json.JSONDecodeError:
                        print(f"Failed to parse JSON line: {line}")
                        continue
        except Exception as e:
            print(f"Error processing response: {e}")
            return {"error": str(e)}
    else:
        response = requests.post(
            TOGETHER_API_URL,
            json={
                "model": "togethercomputer/llama-2-7b-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "Generate a full HTML page based on user interactions and the previous page. Keep the page short and include a few links. The page should be creative and unique."
                    },
                    {"role": "user", "content": prompt}
                ]
            },
            headers={"Authorization": f"Bearer {TOGETHER_API_KEY}"}
        )
        generated_html = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

    print("generated_html:", generated_html)
    return {"html": generated_html}