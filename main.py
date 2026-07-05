import random
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from questions import QUESTION_BANK, CATEGORIES

app = FastAPI()


class Question(BaseModel):
    id: int
    category: str
    question: str
    choices: List[str]
    answer: str
    explanation: str = ""
    image: str = ""


@app.get("/questions", response_model=List[Question])
def get_questions(count: int = 5, category: Optional[str] = None):
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
        result.append(Question(
            id=item["id"],
            category=item["category"],
            question=item["question"],
            choices=choices,
            answer=item["answer"],
            explanation=item.get("explanation", ""),
            image=item.get("image", ""),
        ))
    return result


@app.get("/categories")
def get_categories():
    return {"categories": CATEGORIES}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
