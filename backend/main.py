# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import HTTPException

app = FastAPI()

class Workload(BaseModel):
    type: str  # "compute" | "storage" | "mixed"
    size: float  # GB or vCPU hours

@app.post("/recommend")
def recommend(workload: Workload):
    """
    Recommends the most cost-effective cloud provider (Apex, AWS, or Azure)
    based on workload size and type.

    Args:
        workload (Workload): A Pydantic model with 'type' (compute/storage/mixed)
                             and 'size' (in GB or compute units).

    Returns:
        dict: A dictionary containing detailed cost estimates and the recommended provider.
    """

    # Define detailed pricing per provider by workload type ($/unit)
    pricing = {
        "compute": {
            "apex": 0.10,   # APEX estimated compute cost
            "aws": 0.12,    # AWS EC2 on-demand (approx. t3.medium equivalent)
            "azure": 0.11   # Azure VM A2 v2 (approximate)
        },
        "storage": {
            "apex": 0.07,   # APEX file/block storage estimate
            "aws": 0.023,   # AWS S3 standard
            "azure": 0.0184 # Azure Blob hot tier
        },
        "mixed": {
            "apex": 0.085,  # Hybrid estimate
            "aws": 0.10,    # Estimated blend of EC2 + S3
            "azure": 0.095  # Estimated blend of Azure VM + Blob
        }
    }

    # Validate type
    if workload.type not in pricing:
        raise HTTPException(status_code=400, detail="Invalid workload type. Must be 'compute', 'storage', or 'mixed'.")

    # Compute costs
    cost_details = {}
    for provider, unit_price in pricing[workload.type].items():
        total = unit_price * workload.size
        cost_details[provider] = {
            "unit_price": unit_price,
            "workload_size": workload.size,
            "total_cost": round(total, 4),
            "description": f"{workload.type.capitalize()} at ${unit_price}/unit for {workload.size} units"
        }

    # Determine the recommended provider
    best_provider = min(cost_details, key=lambda k: cost_details[k]["total_cost"])

    return {
        "costs": cost_details,
        "recommended": best_provider,
        "note": f"{best_provider.capitalize()} offers the lowest total cost for this workload type."
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

