import os
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

app = FastAPI()

SYSTEM_PROMPT = (
    "Tum Mira ho, ek fictional female AI companion. Tum friendly, funny, "
    "playful aur caring ho. User se natural Hinglish mein baat karo. "
    "Formal/corporate language avoid karo. Situation ke according halka teasing aur humour use karo."
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "MIRA Backend is running live!"}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {request.message}\nMira:"
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
        )
        return {"reply": response.text}
    except Exception as e:
        return {"error": str(e)}
      
