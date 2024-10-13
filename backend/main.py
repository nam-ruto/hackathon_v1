from typing import Union, Optional, Dict, List
from fastapi import FastAPI
from pydantic import BaseModel
from logic.chatbot import process_chat, gpa_advise
from logic.campus import campus
from fastapi.middleware.cors import CORSMiddleware
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Allow CORS for specific origins (your frontend URL in this case)
origins = [
    "http://127.0.0.1:5500",  # Frontend origin
    "http://localhost:5500"   # Localhost alternative
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,       # List of origins allowed to communicate with this API
    allow_origins=["*"],
    allow_credentials=True,      # If you need to send cookies or authorization headers
    allow_methods=["*"],         # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],         # Allow all headers
)

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
    

def load_campus_guide_data():
    try:
        with open('campus_guide.json', 'r') as file:
            data = json.load(file)
        return data['questions']
    except FileNotFoundError:
        logger.error("campus_guide.json file not found")
        return []
    except json.JSONDecodeError:
        logger.error("Error decoding campus_guide.json file")
        return []

# Function to process the question and return the appropriate answer
def get_campus_guide_answer(question: str):
    # Load data from the JSON file
    guide_data = load_campus_guide_data()
    
    # Find the matching answer
    for item in guide_data:
        if question.lower() in item['question'].lower():
            return item['answer']
    
    # If no match is found, return a default message
    return "Sorry, I don't have an answer to that question."

@app.post("/campus")
async def campus(request: AskRequest):
    question = request.question
    session_id = request.session_id

    # Process the question and fetch the appropriate answer
    answer = get_campus_guide_answer(question)
    
    # Log the answer (optional)
    logger.info(f"Question: {question}, Answer: {answer}")
    
    # Return the answer to the user
    return {"answer": answer}

# @app.post("/campus")
# async def campus_tour(request: AskRequest):
#     question = request.question
#     session_id = request.session_id

#     answer = campus(user_input=question, session_id=session_id)
#     logger.info(answer)

#     return answer
