from sqlalchemy import Column, Integer, String, Text, DECIMAL, TIMESTAMP, Float, ForeignKey, Enum as SQLEnum
from datetime import datetime

from app.database import Base


class Word(Base):
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), unique=True, nullable=False)
    definition = Column(Text)
    difficulty_level = Column(
        SQLEnum('Beginner', 'Intermediate', 'Advanced', name='difficulty'),
        default='Beginner'
    )
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class PracticeSession(Base):
    __tablename__ = "practice_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)

    submitted_sentence = Column(String(255), nullable=False)
    score = Column(DECIMAL(3, 1), nullable=False)
    feedback = Column(Text, nullable=False)
    corrected_sentence = Column(String(255), nullable=False)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)
