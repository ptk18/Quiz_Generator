from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
from typing import List
import json
import re
from fastapi.middleware.cors import CORSMiddleware
from database import engine, database, SessionLocal
from models import Base, User, MyQuiz

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI instance
app = FastAPI()

origins = [
    "http://localhost:5173",   # Local SvelteKit development server
    "http://localhost:3000",    # SvelteKit preview/production in Docker
    "http://frontend:3000",  # Your SvelteKit frontend's origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows only specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Load environment variables from .env file
load_dotenv()

# Set your Gemini API key
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set")

genai.configure(api_key=API_KEY)

class QuizRequest(BaseModel):
    text: str
    num_questions: int
    difficulty: str

class QuizQuestion(BaseModel):
    question: str
    optionA: str
    optionB: str
    optionC: str
    optionD: str
    correctAns: str

class Quiz(BaseModel):
    questions: List[QuizQuestion]

@app.post("/api/generate-quiz", response_model=Quiz)
async def generate_quiz(request: QuizRequest) -> Quiz:
    logger.info(f"Received quiz generation request: {request}")

    prompt = (
        f"Generate a quiz about {request.text} with {request.num_questions} questions at {request.difficulty} difficulty level. "
        f"Format each question as follows:\n"
        f"**Question X:** [question text]\n"
        f"optionA: [option A text]\n"
        f"optionB: [option B text]\n"
        f"optionC: [option C text]\n"
        f"optionD: [option D text]\n"
        f"correctAns: [correct option letter]\n\n"
    )

    try:
        logger.info("Sending request to Gemini API")
        
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)

        # Log the raw response for debugging
        logger.info(f"Raw response from Gemini API: {response.text}")

        # Updated regex pattern to match the new format
        question_pattern = re.compile(r'\*\*Question \d+:\*\*\s*(.+?)\s*optionA:\s*(.+?)\s*optionB:\s*(.+?)\s*optionC:\s*(.+?)\s*optionD:\s*(.+?)\s*correctAns:\s*(.+?)\s*(?=\*\*Question|$)', re.DOTALL)
        matches = question_pattern.findall(response.text)

        if not matches:
            logger.error("No questions found in the response")
            raise ValueError("No questions could be extracted from the API response")

        # Process the parsed data
        quiz_questions = []
        for match in matches:
            quiz_questions.append(QuizQuestion(
                question=match[0].strip(),
                optionA=match[1].strip(),
                optionB=match[2].strip(),
                optionC=match[3].strip(),
                optionD=match[4].strip(),
                correctAns=match[5].strip()
            ))

        return Quiz(questions=quiz_questions)

    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except (genai.types.generation_types.BlockedPromptException, genai.types.generation_types.StopCandidateException) as e:
        logger.error(f"Content generation blocked: {str(e)}")
        raise HTTPException(status_code=400, detail="The quiz content was flagged as inappropriate or generation was stopped")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    
# Create the database tables on startup
@app.on_event("startup")
async def startup():
    await database.connect()
    Base.metadata.create_all(bind=engine)

# Disconnect the database on shutdown
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    
# Pydantic model for the request body
class UserCreate(BaseModel):
    name: str
    email: str
    password: str = Field(..., min_length=8)
    
class UserLogin(BaseModel):
    email: str
    password: str

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create-user/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the email is alredy registered
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(name=user.name, email=user.email, password=user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Check if the email exists
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # Check if the password matches
    if db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # If login is successful, return a success message or user info
    return {"message": "Login successful!", "id": db_user.id ,"name": db_user.name, "email": db_user.email}

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}

@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all() 
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

class QuestionAnswer(BaseModel):
    question: str
    optionA: str
    optionB: str
    optionC: str
    optionD: str
    correctAns: str
    userAnswer: str
    isCorrect: bool

class QuizCreate(BaseModel):
    user_id: int
    questions: List[QuestionAnswer]
    score: int
    total_questions: int
    
class QuizResponse(BaseModel):
    q_id: int
    user_id: int
    questions: List[QuestionAnswer]
    score: int
    total_questions: int
    
    class Config:
        orm_mode = True
    
@app.post("/save-quiz/")
def save_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):
    # If q_id is provided, check if the quiz exists (for updating)
    if hasattr(quiz, 'q_id') and quiz.q_id is not None:
        # Check if the quiz with the given ID already exists
        existing_quiz = db.query(MyQuiz).filter(MyQuiz.q_id == quiz.q_id).first()

        if existing_quiz:
            # Update the existing quiz fields
            existing_quiz.user_id = quiz.user_id
            existing_quiz.questions = [q.dict() for q in quiz.questions]  # Update questions
            existing_quiz.score = quiz.score
            existing_quiz.total_questions = quiz.total_questions

            # Commit the changes to the database
            db.commit()
            db.refresh(existing_quiz)

            return {"message": "Quiz updated successfully!", "quiz_id": existing_quiz.q_id}
        else:
            return {"error": "Quiz not found for update."}
    
    # If q_id is not provided or it's None, create a new quiz
    new_quiz = MyQuiz(
        user_id=quiz.user_id,
        questions=[q.dict() for q in quiz.questions],  # Use the list of dictionaries
        score=quiz.score,
        total_questions=quiz.total_questions
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)

    return {"message": "New quiz saved successfully!", "quiz_id": new_quiz.q_id}



@app.get("/users/{user_id}/quizzes", response_model=list[QuizResponse])
def get_user_quizzes(user_id: int, db: Session = Depends(get_db)):
    quizzes = db.query(MyQuiz).filter(MyQuiz.user_id == user_id).all()
    
    if not quizzes:
        raise HTTPException(status_code=404, detail="No quizzes found for this user")
    
    return quizzes

@app.delete("/quizzes/{quiz_id}/delete")
def delete_quiz(quiz_id: int, current_user_id: int, db: Session = Depends(get_db)):
    quiz = db.query(MyQuiz).filter(MyQuiz.q_id == quiz_id).first()
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    if quiz.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this quiz")
    
    db.delete(quiz)
    db.commit()
    
    return {"message": "Quiz deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)