from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Music Agents")
app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatMessage(BaseModel):
    message: str


@app.get("/")
async def root():
    return  FileResponse("static/index.html")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat(body: ChatMessage):
    # Here you would implement the logic to process the chat message and generate a response
    response = f"Received your message: {body.message}"
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)