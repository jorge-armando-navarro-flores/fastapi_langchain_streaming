import os
from fastapi import FastAPI, Header, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse, JSONResponse
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

load_dotenv()

app = FastAPI()

# Set up rate limiter (5 reqs per minute per IP)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

API_KEY = os.getenv("API_KEY", "default-dev-key")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# ========================= FUNCTIONS ========================= 

async def verify_api_key(x_api_key: str = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

async def stream_chat_response(message: str):
    async for chunk in llm.astream(input=[HumanMessage(content=message)]):
        content = getattr(chunk, "content", None)
        if content:
            yield content

# ========================= ENDPOINTS ========================= 

@app.get("/")
def read_root():
    return {"message": "Public endpoint - no auth needed"}

@app.post("/chat/stream", dependencies=[Depends(verify_api_key)])
@limiter.limit("10/day")  # Limit to 10 requests per day per IP
async def chat_stream(prompt: str, request: Request):
    generator = stream_chat_response(prompt)
    return StreamingResponse(generator, media_type="text/event-stream")
