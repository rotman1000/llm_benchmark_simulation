from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from tenacity import retry, stop_after_attempt, wait_fixed
from .security import get_api_key, create_api_key
from .database import create_tables, get_db
from .ranking import get_rankings

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         
    allow_credentials=True,    
    allow_methods=["*"],            
    allow_headers=["*"],  
)

@app.on_event("startup")
def on_startup():
    create_tables()

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
@app.get("/rankings/{metric_name}")
def rankings(metric_name: str, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    result = get_rankings(db, metric_name)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result

@app.get('/get_api_key')
def get_api_key(db: Session = Depends(get_db)):
    return create_api_key(db)

