from typing import Union, Optional, Dict, List
from fastapi import FastAPI
from pydantic import BaseModel
from logic.chatbot import process_chat
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# AskRequest class: contain parameters for the request
class AskRequest(BaseModel):
    question: str
    session_id: str

# --------------------------------------- #
# ----------MAIN ROUTE------------------- #
# --------------------------------------- #


# @app.get("/")
# async def home():
#     return "Hello"


@app.post("/ask")
async def ask(request: AskRequest):
    question = request.question
    session_id = request.session_id

    answer = process_chat(user_input=question, session_id=session_id)
    logger.info(answer)

    return answer
    