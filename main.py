import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.responses import StreamingResponse

from dotenv import load_dotenv

load_dotenv()  # Optional: only needed for local dev with a `.env` file

app = FastAPI()

API_KEY = os.getenv("API_KEY", "default-dev-key")  # fallback for local dev


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


# ========================= FUNCTIONS ========================= 

def verify_api_key(x_api_key: str = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
# Async generator that yields the tokens
async def stream_chat_response(message: str):
    # Stream the generation
    async for chunk in llm.astream(input=[HumanMessage(content=message)]):
        if chunk.content:
            yield chunk.content


# ========================= ENDPOINTS ========================= 

@app.get("/")
def read_root():
    return {"message": "Public endpoint - no auth needed"}

@app.post("/chat/stream", dependencies=[Depends(verify_api_key)])
async def chat_stream(prompt: str):
    generator = stream_chat_response(prompt)
    return StreamingResponse(generator, media_type="text/plain")
