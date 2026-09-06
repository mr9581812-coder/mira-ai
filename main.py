import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI()

# Enable CORS for Flutter Web App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = """
Tum Mira ho, ek fictional female AI companion. Tum friendly, funny,
playful aur caring ho. User se natural Hinglish mein baat karo.
Formal/corporate language avoid karo. Situation ke according halka teasing aur humour use karo.
"""

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "MIRA Backend is running live!"}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        full_prompt = f"{SYSTEM_PROMPT}\nUser: {request.message}\nMira:"
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
        )
        return {"reply": response.text}
    except Exception as e:
        return {"error": str(e)}
        
