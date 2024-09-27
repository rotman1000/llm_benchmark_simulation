import time
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from tenacity import retry, stop_after_attempt, wait_fixed
from prometheus_client import start_http_server, Counter, Summary
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from .security import get_api_key
from .database import get_db
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


# Create Prometheus metrics
REQUEST_COUNT = Counter("api_requests_total", "Total number of requests")
REQUEST_LATENCY = Summary("request_latency_seconds", "Request latency in seconds")

@app.middleware("http")
async def prometheus_middleware(request, call_next):
    # Increment request count
    REQUEST_COUNT.inc()

    # Measure request latency
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    REQUEST_LATENCY.observe(process_time)

    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
@app.get("/rankings/{metric_name}")
def rankings(metric_name: str, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    result = get_rankings(db, metric_name)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result
