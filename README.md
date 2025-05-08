# Hybrid Cloud Cost Optimization Tool

This tool helps users compare the cost of running workloads on Dell APEX vs AWS vs Azure, and recommends the optimal deployment strategy.

## Features
- Simple workload type selection
- Cost comparison (mock pricing)
- Deployment recommendation

## Stack
- Backend: FastAPI (Python)
- Frontend: React + Axios

## Run Locally
1. `cd backend && uvicorn main:app --reload`
2. `cd frontend/hybrid-cost-ui && npm start`
