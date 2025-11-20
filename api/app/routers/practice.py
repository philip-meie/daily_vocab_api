from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Word, PracticeSession
from app.schemas import ValidateSentenceRequest, ValidateSentenceResponse
from app.utils import mock_ai_validation

router = APIRouter()


@router.post("/validate-sentence", response_model=ValidateSentenceResponse)
def validate_sentence(
    request: ValidateSentenceRequest,
    db: Session = Depends(get_db)
):
    """
    Receive user sentence and validate it (mock AI)
    Save results to database
    """
    
    # Get word data
    word = db.query(Word).filter(Word.id == request.word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    # Mock AI validation
    ai_result = mock_ai_validation(request.sentence,word.word,word.difficulty_level)

    # Save to database
    session_record = PracticeSession(
        user_id=1,
        word_id=request.word_id,
        submitted_sentence=request.sentence,
        score=ai_result["score"],
        feedback=ai_result["suggestion"],
        corrected_sentence=ai_result["corrected_sentence"],
    )

    db.add(session_record)
    db.commit()
    db.refresh(session_record)


    return ValidateSentenceResponse(
        score=ai_result["score"],
        level=ai_result["level"],
        suggestion=ai_result["suggestion"],
        corrected_sentence=ai_result["corrected_sentence"]
    )
