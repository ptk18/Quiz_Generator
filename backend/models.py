from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(300))
    email = Column(String(300), unique=True, index=True)
    password = Column(String(300))  # Make sure this is defined
    
class MyQuiz(Base):
    __tablename__ = 'quizzes'

    q_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    questions = Column(JSON)  # This will store the entire questions list with answers
    score = Column(Integer)
    total_questions = Column(Integer)

    user = relationship("User")