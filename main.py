from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="Cloud API", version="1.0.0")

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "cloud-api",
        "version": "2.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/info")
def get_info():
    return {
        "name": "Cloud API Microservice",
        "version": "1.0.0",
        "endpoints": ["/", "/info", "/docs"]
    }
