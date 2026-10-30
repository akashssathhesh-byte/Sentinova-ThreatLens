import hashlib
import ipaddress
import json
import re
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "indicators.json"
app = FastAPI(title="Sentinova Threat Lens", version="1.0.0", description="Safe demo indicator reputation lookup")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")


def load_indicators() -> list[dict[str, Any]]:
    try:
        with DATA_FILE.open(encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, list):
            raise ValueError("Indicator data must be a list")
        return data
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise RuntimeError("Local indicator data is unavailable or invalid") from exc


def classify(value: str) -> str:
    value = value.strip()
    try:
        ipaddress.ip_address(value)
        return "ip"
    except ValueError:
        pass
    if re.fullmatch(r"(?i)[a-f0-9]{32}|[a-f0-9]{40}|[a-f0-9]{64}", value):
        return "hash"
    domain = value[:-1] if value.endswith(".") else value
    if len(domain) <= 253 and all(
        re.fullmatch(r"(?i)[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", part)
        for part in domain.split(".")
    ) and "." in domain:
        return "domain"
    raise HTTPException(status_code=422, detail="Enter a valid IPv4/IPv6 address, domain, or MD5/SHA-1/SHA-256 hash.")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(ROOT / "static" / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/summary")
def summary() -> dict[str, Any]:
    try:
        items = load_indicators()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {
        "total": len(items),
        "high_risk": sum(item.get("risk") == "High" for item in items),
        "medium_risk": sum(item.get("risk") == "Medium" for item in items),
        "low_risk": sum(item.get("risk") == "Low" for item in items),
        "source": "Local demo dataset",
    }


@app.get("/api/indicators")
def indicators(kind: str = Query("all", pattern="^(all|ip|domain|hash)$")) -> dict[str, Any]:
    try:
        items = load_indicators()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    if kind != "all":
        items = [item for item in items if item["type"] == kind]
    return {"items": items, "count": len(items)}


@app.get("/api/lookup")
def lookup(value: str = Query(..., min_length=1, max_length=253)) -> dict[str, Any]:
    clean = value.strip()
    kind = classify(clean)
    normalized = clean.lower()
    try:
        records = load_indicators()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    match = next((row for row in records if row["type"] == kind and row["value"].lower() == normalized), None)
    if match:
        return {**match, "matched": True, "source": "Local demo dataset"}
    return {
        "value": clean,
        "type": kind,
        "risk": "Unknown",
        "confidence": 0,
        "category": "No local match",
        "first_seen": None,
        "last_seen": None,
        "summary": "This indicator was not found in the bundled demo data. Unknown does not mean safe.",
        "matched": False,
        "source": "Local demo dataset",
        "reference": hashlib.sha256(normalized.encode()).hexdigest()[:12],
    }
