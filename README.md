# Sentinova-ThreatLens

A beginner-friendly, defensive cybersecurity dashboard for reviewing sample IP address, domain, and file hash reputation records. It includes a FastAPI backend and responsive browser UI, and is ready to deploy as a Python web service on Render.

# Features

- Responsive dashboard with risk summary, risk distribution, and searchable indicator list.
- Input validation and lookups for IPv4/IPv6, DNS-style domains, and MD5/SHA-1/SHA-256 hex hashes.
- Local-only mock reputation data with category, confidence, timestamps, and explanatory notes.
- JSON endpoints and interactive API documentation at `/docs`.
- Health endpoint at `/health` for Render.
- Friendly error messages for invalid inputs and unavailable sample data.
  # Run locally

You need Python 3.10 or newer.

1. Download or clone this repository and open a terminal in its folder.

3. Create and activate a virtual environment:

   **Windows PowerShell**

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS / Linux**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install packages and start the app:

   ```bash
   pip install -r requirements.txt
   uvicorn main:app --reload
