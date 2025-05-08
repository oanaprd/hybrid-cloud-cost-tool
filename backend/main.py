# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

class Workload(BaseModel):
    type: str  # "compute" | "storage" | "mixed"
    size: float  # GB or vCPU hours

@app.post("/recommend")
def recommend(workload: Workload):
    # Mock pricing data
    prices = {
        "apex": 0.09,  # $/unit
        "aws": 0.12,
        "azure": 0.11
    }
    cost = {k: v * workload.size for k, v in prices.items()}
    best = min(cost, key=cost.get)
    return {"costs": cost, "recommended": best}

