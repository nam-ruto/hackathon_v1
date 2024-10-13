from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

async def campus(user_input: str, session_id: str):
    question = user_input
    session_id = session_id

    # Process the question and fetch the appropriate answer
    answer = get_campus_guide_answer(question)
    
    # Log the answer (optional)
    logger.info(f"Question: {question}, Answer: {answer}")
    
    # Return the answer to the user
    return {"answer": answer}
