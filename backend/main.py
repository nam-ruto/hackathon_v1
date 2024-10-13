from typing import Union, Optional, Dict, List
from fastapi import FastAPI
from pydantic import BaseModel
from logic.chatbot import process_chat, gpa_advise
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# AskRequest class: contain parameters for the request
class AskRequest(BaseModel):
    question: str
    session_id: str

class Course(BaseModel):
    course_name: str
    credit: int
    grade: float  # Assuming the grade is represented as a number

# Define the request model containing a list of courses
class GPACalculationRequest(BaseModel):
    courses: List[Course]

def calculate_gpa(courses: List[Course]) -> float:
    total_points = sum(course.credit * course.grade for course in courses)
    total_credits = sum(course.credit for course in courses)
    return total_points / total_credits if total_credits > 0 else 0.0

def format_gpa_question(courses):
    course_details = "\n".join(
        [f"{course.course_name}: {course.credit} credits, grade {course.grade}" for course in courses]
    )
    question = f"Given the following courses, do you have any comments for me:\n{course_details}"
    return question


@app.post("/ask")
async def ask(request: AskRequest):
    question = request.question
    session_id = request.session_id

    answer = process_chat(user_input=question, session_id=session_id)
    logger.info(answer)

    return answer

# We don't need this endpoint anymore
@app.post("/calculate-gpa")
async def calculate_gpa_endpoint(request: GPACalculationRequest):
    gpa = calculate_gpa(request.courses)
    return {"gpa": gpa}

@app.post("/request-advise")
async def request_advise(request: GPACalculationRequest):
    question = format_gpa_question(courses=request.courses)
    
    answer = gpa_advise(user_input=question)
    logger.info(answer)

    return answer
    