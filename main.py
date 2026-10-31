import os
import logging
from datetime import datetime, timezone
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("sentinova")

app = FastAPI(
    title="Sentinova Threat Lens",
    description="Cybersecurity Threat Detection and Analysis Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

input_text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Text, URL or log entry to analyze"
    )


class ThreatResponse(BaseModel):
    status: str
    risk_level: str
    threat_score: int
    detected_indicators: List[str]
    timestamp: str

THREAT_INDICATORS = {
    "script_injection": [
        "<script",
        "javascript:",
        "onerror="
    ],
    "command_injection": [
        "&&",
        "||",
        "; rm ",
        "powershell -enc"
    ],
    "suspicious_url": [
        "bit.ly/",
        "tinyurl.com/",
        "ngrok.io"
    ],
    "phishing_indicators": [
        "verify your account",
        "urgent password reset",
        "confirm your credentials"
    ],
    "suspicious_file": [
        ".exe",
        ".bat",
        ".ps1",
        ".vbs"
    ]
}


def analyze_threat(text: str):
    detected = []
    normalized_text = text.lower()

    for category, indicators in THREAT_INDICATORS.items():
        for indicator in indicators:
            if indicator in normalized_text:
                detected.append(category)
                break

    # Simple heuristic score, not a probability
    score = min(len(detected) * 25, 100)

    if score >= 75:
        risk = "High"
    elif score >= 25:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "risk_level": risk,
        "threat_score": score,
        "detected_indicators": detected
    }


# --------------------------------------------------
# HOME ROUTE
# --------------------------------------------------

@app.get("/")
async def home():
    return {
        "project": "Sentinova Threat Lens",
        "message": "Welcome to Sentinova Threat Lens",
        "description": "Cybersecurity Threat Detection Platform",
        "status": "Running Successfully",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/health"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "application": "Sentinova Threat Lens",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# --------------------------------------------------
# API STATUS
# --------------------------------------------------

@app.get("/api/status")
async def api_status():
    return {
        "api": "Sentinova Threat Lens API",
        "status": "online",
        "version": "1.0.0"
    }


# --------------------------------------------------
# THREAT ANALYSIS API
# --------------------------------------------------

@app.post("/api/analyze", response_model=ThreatResponse)
async def threat_analysis(request: ThreatRequest):

    try:
        logger.info("Threat analysis request received")

        result = analyze_threat(request.input_text)

        return ThreatResponse(
            status="analysis_completed",
            risk_level=result["risk_level"],
            threat_score=result["threat_score"],
            detected_indicators=result["detected_indicators"],
            timestamp=datetime.now(timezone.utc).isoformat()
        )

    except Exception:
        logger.exception("Threat analysis failed")
        raise HTTPException(
            status_code=500,
            detail="Internal threat analysis error"
        )

@app.get("/api/info")
async def application_info():
    return {
        "name": "Sentinova Threat Lens",
        "framework": "FastAPI",
        "deployment": "Render",
        "status": "Active"
    }

import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
