# 🛡️ Cloud Drift Engine (DevSecOps)

A lightweight Continuous Compliance Engine built with Python and Docker. 
This project simulates enterprise-grade cloud security guardrails by parsing infrastructure-as-code or live cloud configurations, detecting unauthorized security group drift, and instantly dispatching alert payloads to a Discord Webhook channel.

---

# 📈 DevSecOps Impact

- **Zero-Dependency Architecture:** Built purely using Python standard libraries (`urllib`, `json`, `os`) to keep the runtime footprint minimal and highly secure.
- **Secured Runtime Secrets:** Implements absolute separation of config and code by leveraging Docker environment variables (`-e`) and GitHub Actions Secrets to prevent credential leaks.
- **Automated Ephemeral Scans:** Containerized using an ultra-lightweight Alpine Linux layer, enabling the engine to boot, scan, alert, and terminate within seconds without system bloat.

---

# 🛠️ How It Works

1. **Ingestion:** 
   The engine reads `baseline.json`, representing the approved secure cloud network configuration.

2. **Inspection:** 
   It ingests `live-state.json`, representing the real-time active state of cloud network assets.

3. **Analysis:** 
   The engine maps assets using unique IDs and compares active rules against the baseline configuration.

4. **Alerting:** 
   If an unauthorized change is detected (for example, a database port exposed to public `0.0.0.0/0`), the engine dispatches an active incident alert to Discord.

---

# 📂 Project Structure

```text
cloud-drift-engine/
│
├── baseline.json
├── live-state.json
├── engine.py
├── Dockerfile
└── .github/
    └── workflows/
        └── scan.yml
```

### File Descriptions

| File | Purpose |
|---|---|
| `baseline.json` | Approved security posture baseline |
| `live-state.json` | Simulated active cloud state containing drift |
| `engine.py` | Core compliance checking logic and webhook driver |
| `Dockerfile` | Alpine-based container configuration |
| `scan.yml` | Hourly GitHub Actions CRON workflow |

---

# 🚨 Sample Alert Payload

When the engine detects drift, it formats and ships the following payload directly to ChatOps channels:

```yaml
🚨 CLOUD SECURITY DRIFT DETECTED 🚨

Resource: production-db (sg-prod-db-01)
Expected Network: 10.0.0.5/32
Actual Live Network: 0.0.0.0/0
Risk: EXPOSED TO INTERNET (Potential Exfiltration)
```

---

# 💻 Quick Start

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/cloud-drift-engine.git
cd cloud-drift-engine
```

---

## 2️⃣ Build the Portable Docker Image

```bash
docker build -t cloud-drift-engine:v3 .
```

---

## 3️⃣ Execute the Scan Locally

Inject your runtime variables securely without modifying source code:

```bash
docker run -e DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_RAW_URL" cloud-drift-engine:v3
```

---

# 🔒 Automated CI/CD Core

The background automation engine uses GitHub Actions to spin up ephemeral Linux runners on an hourly CRON schedule:

```text
0 * * * *
```

## Setup Instructions

1. Open your GitHub repository.
2. Navigate to:

```text
Settings → Secrets and variables → Actions
```

3. Create a new repository secret.

## Secret Name

```text
DISCORD_WEBHOOK_URL
```

4. Paste your Discord webhook URL as the secret value.

---

# 🧠 Concepts Demonstrated

- DevSecOps
- Infrastructure Drift Detection
- Docker Containerization
- Secure Secret Injection
- REST API Integration
- GitHub Actions Automation
- Compliance Monitoring
- ChatOps Alerting

---

# 📌 Future Enhancements

- AWS Security Group API integration using boto3
- GCP Firewall rule analysis
- PostgreSQL audit logging
- Automated remediation engine
- Multi-cloud compliance support
- Slack / Microsoft Teams integration

---

# 📜 License

This project is intended for educational and portfolio purposes.
