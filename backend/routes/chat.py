from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Import your RAG function
from rag.rag_pipeline import answer_question

router = APIRouter()


# -----------------------------
# Request Model
# -----------------------------
class ChatRequest(BaseModel):
    question: str
    report_text: str


# -----------------------------
# Response Model (Optional)
# -----------------------------
class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


# -----------------------------
# Chat Endpoint
# -----------------------------
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    # Validate question
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # Validate report
    if not request.report_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Please upload a blood report first."
        )

    try:

        result = answer_question(
            question=request.question,
            report_text=request.report_text
        )

        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"]
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Error generating response: {str(e)}"
        )