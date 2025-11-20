from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.models import Word, PracticeSession
from app.schemas import SummaryResponse, HistoryItem

router = APIRouter()


@router.get("/summary", response_model=SummaryResponse)
def get_summary(db: Session = Depends(get_db)):
    """Get overall practice statistics"""
    
    # Total practice sessions
    total_practices = db.query(func.count(PracticeSession.id)).scalar() or 0
    
    # Average score
    average_score = db.query(func.avg(PracticeSession.score)).scalar() or 0.0
    
    # Total unique words practiced
    total_words_practiced = (
        db.query(func.count(func.distinct(PracticeSession.word_id))).scalar() or 0
    )
    
    # Distribution by level
    level_rows = (
        db.query(Word.difficulty_level, func.count(PracticeSession.id))
        .join(PracticeSession, PracticeSession.word_id == Word.id)
        .group_by(Word.difficulty_level)
        .all()
    )
    level_distribution = {level: count for level, count in level_rows}

    return SummaryResponse(
        total_practices=total_practices,
        average_score=round(average_score, 2),
        total_words_practiced=total_words_practiced,
        level_distribution=level_distribution,
    )

@router.get("/history", response_model=List[HistoryItem])
def get_history(limit: int = 10, db: Session = Depends(get_db)):
    """Get last 10 practice sessions"""

    rows = (
        db.query(PracticeSession, Word.word)
        .join(Word, PracticeSession.word_id == Word.id)
        .order_by(PracticeSession.timestamp.desc())
        .limit(limit)
        .all()
    )

    history: List[HistoryItem] = []
    for session, word in rows:
        history.append(
            HistoryItem(
                id=session.id,
                word=word,
                user_sentence=session.submitted_sentence,
                score=session.score,
                feedback=session.feedback,
                practiced_at=session.timestamp,
            )
        )

    return history
