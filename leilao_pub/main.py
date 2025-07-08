from fastapi import FastAPI
from pydantic import BaseModel
from .publisher import publisher

app = FastAPI()

class Message(BaseModel):
    body: str



@app.post('/pub')
def send_message(message: Message):
    publisher.send_message(message.body)


    return {"message_status":"enviada"}
