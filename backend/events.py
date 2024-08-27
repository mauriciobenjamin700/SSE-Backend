from collections import deque
from typing import ClassVar
from pydantic import BaseModel

class EventModel(BaseModel):
    type: str
    message: str
    
class SSE(BaseModel):
    EVENTS: ClassVar[deque] = deque([])
    
    @staticmethod  
    def add_event(event: EventModel):
        SSE.EVENTS.append(event)

    @staticmethod        
    def get_event() -> EventModel:
        if len(SSE.EVENTS) > 0:
            return SSE.EVENTS.popleft()
        
        return None
    
    @staticmethod
    def count():
        return len(SSE.EVENTS)