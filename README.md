# Sentinova-ThreatLens;

A beginner-friendly, defensive cybersecurity dashboard for reviewing sample IP address, domain, and file hash reputation records. It includes a FastAPI backend and responsive browser UI, and is ready to deploy as a Python web service on Render.

# Features:

• Responsive dashboard with risk summary, risk distribution, and searchable indicator list.
• Input validation and lookups for IPv4/IPv6, DNS-style domains, and MD5/SHA-1/SHA-256 hex hashes.
• Local-only mock reputation data with category, confidence, timestamps, and explanatory notes.
• JSON endpoints and interactive API documentation at `/docs`.
• Health endpoint at `/health` for Render.
• Friendly error messages for invalid inputs and unavailable sample data.
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

# Scope and Limitations:

• Dashboard UI with a search form and summary cards.
• Local sample IOC dataset for predictable demonstrations.
• FastAPI backend with input validation and JSON responses.
• Health-check endpoint and clear error responses.
• Deployment configuration and beginner-friendly documentation.
• Guaranteed detection of real-world threats or malware.
• Automatic containment, file deletion, network blocking, or endpoint remediation.
• A verified live feed from VirusTotal, OTX, or another threat-intelligence provider.
• Authentication, multi-user permissions, persistent case management, or production-grade audit logging.

# Core Features:

IOC lookup Search an IP address, domain, or file hash.
Input validation Reject malformed indicators and return useful error messages.
Risk classification Display Low, Medium, High, or Unknown based on documented sample rules.
Threat details Show indicator type, sample description, source label, and last-updated field when present.
API endpoints Provide health and analysis endpoints for the dashboard and external testing.
Configuration Load safe defaults from config.yaml; allow environment variables for deployment settings.
Responsive interface Use a clean, accessible layout that works on desktop and mobile.

# Architecture:
A simple deployment has three layers:
• Frontend: HTML, CSS, and JavaScript render the dashboard and send requests to the API.
• Application API: FastAPI validates inputs, loads configuration, checks the local sample dataset, and returns
structured JSON.
• Data/configuration: config.yaml and a sample JSON file provide demo rules and indicators. Secrets, if any are
later required, belong in Render environment variables—not in Git.
Browser
   |
   | HTTPS request
   v
FastAPI application (main.py)
   |-- input validation
   |-- risk scoring / sample lookup
   |-- health endpoint
   |
   +--> config.yaml
   +--> data/sample_threats.json
   |
   v
JSON response -> dashboard

# Technology Stack:
Technology Purpose
Python Backend language and validation logic
FastAPI Web API framework
Uvicorn ASGI server
HTML / CSS / JavaScript Frontend dashboard
YAML + JSON Application settings and sample data
Git + GitHub Version control and public portfolio repository
Render Cloud web-service hosting

# Testing Checklist:

• n Application starts locally without errors.
• n Dashboard loads on desktop and mobile widths.
• n /health returns a successful response.
• n Valid IPv4, domain, and hash inputs are handled as expected.
• n Malformed or missing input returns a clear 4xx response.
• n Known sample indicators return the expected demo classification.
• n Unknown indicators are not incorrectly described as confirmed safe.
• n No API keys or secrets are committed to GitHub.
• n Render build and startup logs show no errors.
• n Public Render URL and README instructions match the deployed version.

# Security and Responsible Use:
    
• Treat all external indicator values as untrusted input and validate length and format.
• Do not automatically download, execute, or open suspicious files or URLs.
• Do not perform scanning, exploitation, or blocking actions as part of this lookup dashboard.
• If external intelligence APIs are added, store credentials in environment variables and handle provider errors and
rate limits.
• Use HTTPS in production and consider authentication, request throttling, logging, and dependency updates
before handling sensitive data.

# Conclusion:

Sentinova Threat Lens is a practical portfolio project for demonstrating Python API development, input validation,
threat-indicator handling, dashboard design, GitHub workflow, and cloud deployment. Start with predictable local
demo data, test each endpoint, document limitations honestly, and add live intelligence integrations only when they
are explicitly configured and secured.
