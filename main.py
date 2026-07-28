import random
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
from typing import List, Optional
from questions import QUESTION_BANK, CATEGORIES

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# 問題IDからインデックスへの高速引き当て用マップ
_QUESTION_MAP = {q["id"]: q for q in QUESTION_BANK}


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

app.add_middleware(SecurityHeadersMiddleware)


# クライアントに返す問題（answer・explanation は含まない）
class QuestionPublic(BaseModel):
    id: int
    category: str
    question: str
    choices: List[str]
    image: str = ""


# 回答後に返すデータ
class AnswerResponse(BaseModel):
    id: int
    answer: str
    explanation: str


MAX_COUNT = 50


@app.get("/questions", response_model=List[QuestionPublic])
def get_questions(
    count: int = Query(default=5, ge=1, le=MAX_COUNT),
    category: Optional[str] = None,
):

    pool = QUESTION_BANK
    if category and category != "all":
        pool = [q for q in pool if q["category"] == category]
    if not pool:
        pool = QUESTION_BANK

    sampled = random.sample(pool, min(count, len(pool)))
    result = []
    for item in sampled:
        choices = item["choices"][:]
        random.shuffle(choices)
        result.append(QuestionPublic(
            id=item["id"],
            category=item["category"],
            question=item["question"],
            choices=choices,
            image=item.get("image", ""),
        ))
    return result


@app.get("/answer/{question_id}", response_model=AnswerResponse)
def get_answer(question_id: int):
    q = _QUESTION_MAP.get(question_id)
    if q is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return AnswerResponse(
        id=q["id"],
        answer=q["answer"],
        explanation=q.get("explanation", ""),
    )


@app.get("/categories")
def get_categories():
    return {"categories": CATEGORIES}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
