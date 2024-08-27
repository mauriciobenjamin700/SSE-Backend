from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import asyncio

from events import (
    EventModel,
    SSE
)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"msg": "Hello World"}

@app.post("/emit")
async def new_event(event: EventModel):
    SSE.add_event(event)
    return {
        "message": "Event added", 
        "count": SSE.EVENTS.count()}
    
@app.get("/stream")
async def stream_events(req: Request):
    
    async def stream_generator():
    
        while True:
            if req.is_disconnected():
                print("SEE Disconnected")
                break
            
            event = SSE.get_event()
            if event:
                yield f"data: {event.model_dump_json()}"
                
            await asyncio.sleep(1)
            
    return EventSourceResponse(stream_generator())