from fastapi import FastAPI, HTTPException, Form, Query
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
import random
import wordninja

app = FastAPI(title="Wordle API", description="API for playing Wordle", version="1.0.0")

class WordSegResponse(BaseModel):
    segmented: List[str]

class ResultKind(str, Enum):
    ABSCENT = "absent"
    PRESENT = "present"
    CORRECT = "correct"

class GuessResult(BaseModel):
    slot: int
    guess: str
    result: ResultKind

WORD_LIST = [
    "world", "plane", "crane", "brake", "stake",
    "snake", "grape", "shape", "shade", "blade"
]

def validate_word(word: str, size: int) -> bool:
    return len(word) == size and word.isalpha()

def check_guess(target: str, guess: str) -> List[GuessResult]:
    if len(guess) != len(target):
        raise HTTPException(status_code=400, detail="Guess length must match target word length")
    
    target_chars = list(target.lower())
    guess_chars = list(guess.lower())
    results = []
    
    for i, (guess_char, target_char) in enumerate(zip(guess_chars, target_chars)):
        if guess_char == target_char:
            results.append(GuessResult(slot=i, guess=guess_char, result=ResultKind.CORRECT))
            target_chars[i] = None
            guess_chars[i] = None
    
    for i, guess_char in enumerate(guess_chars):
        if guess_char is None:
            continue
        
        if guess_char in target_chars:
            results.append(GuessResult(slot=i, guess=guess_char, result=ResultKind.PRESENT))
            target_chars[target_chars.index(guess_char)] = None
        else:
            results.append(GuessResult(slot=i, guess=guess_char, result=ResultKind.ABSCENT))
    
    results.sort(key=lambda x: x.slot)
    return results

def segment_words(text: str) -> List[str]:
    try:
        text = str(text).strip()
        if not text:
            raise ValueError("Empty text provided")
        
        segmented = wordninja.split(text)
        return segmented
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in word segmentation: {str(e)}")

DAILY_WORD = random.choice(WORD_LIST)

@app.get("/daily")
async def guess_daily(guess: str = Query(..., description="Your guess"),
                      size: int = Query(default=5, description="Word size")) -> List[GuessResult]:
    if not validate_word(guess, size):
        raise HTTPException(status_code=400, detail="Invalid guess")
    return check_guess(DAILY_WORD, guess)

@app.get("/random")
async def guess_random(guess: str = Query(..., description="Your guess"),
                       size: int = Query(default=5, description="Word size"),
                       seed: Optional[int] = Query(default=None, description="Random seed")) -> List[GuessResult]:
    if seed is not None:
        random.seed(seed)
    target = random.choice(WORD_LIST)
    if not validate_word(guess, size):
        raise HTTPException(status_code=400, detail="Invalid guess")
    return check_guess(target, guess)

@app.get("/word/{word}")
async def guess_word(word: str,
                     guess: str = Query(..., description="Your guess for the word")) -> List[GuessResult]:
    if not validate_word(word, len(word)):
        raise HTTPException(status_code=400, detail="Invalid target word")
    if not validate_word(guess, len(word)):
        raise HTTPException(status_code=400, detail="Invalid guess")
    return check_guess(word, guess)

@app.post("/wordseg")
async def wordseg(text: str = Form(...)) -> WordSegResponse:
    words = segment_words(text)
    return WordSegResponse(segmented=words)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)