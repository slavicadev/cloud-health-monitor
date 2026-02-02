# Cloud-Pulse: Infrastructure Intelligence Platform

I built this tool to move away from manually checking individual status pages. It is a containerized monitoring system that tracks global cloud service health and uses a heuristic logic engine to spot patterns in concurrent outages. Instead of just showing a list of "up" or "down" statuses, it analyzes whether multiple failures point to a larger backbone or DNS issue.

---

* **Asynchronous Polling:** Hits multiple service APIs (GitHub, Slack, Cloudflare, etc.) without blocking the main thread.
* **Stability Predictor:** A logic layer that calculates a Global Health Score and provides context on whether an outage is isolated or systemic.
* **Architecture:** Decoupled into two microservices (Monitor and Dashboard) handled via Docker Compose.
* **Persistent History:** Uses a local volume to store state, ensuring trend data survives container restarts.
* **Real-time Visualization:** A Streamlit-based UI for temporal analysis and reliability tracking.

---

## Tech Stack

* **Language:** Python 3.12
* **Data Science:** Pandas for time-series processing.
* **Frontend:** Streamlit for the analytics dashboard.
* **Infrastructure:** Docker & Docker Compose for container orchestration.
* **Automation:** GitHub Actions (CI) for automated build verification.

---

## Getting Started

### Prerequisites
* Docker and Docker Compose installed on your machine.

### Setup and Execution
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/slavicadev/cloud-health-monitor.git](https://github.com/slavicadev/cloud-health-monitor.git)
    cd cloud-health-monitor
    ```

2.  **Spin up the stack:**
    ```bash
    docker compose up --build -d
    ```

3.  **Access the dashboard:**
    The UI is served at [http://localhost:8501]

---

## Logic and Data Flow
The monitor service polls external status APIs every 10 minutes and appends the results to a shared JSON store. The dashboard service reads this history to generate reliability charts. The "AI" component is a heuristic engine that weights service failures; for example, a Cloudflare outage is weighted more heavily in the stability score than a single service outage due to its impact on the wider internet backbone.

---

## Project Structure

```text
.
├── .github/workflows/    # CI/CD pipeline configurations
├── app/                  # Frontend logic (Streamlit UI)
│   └── app.py            
├── monitor/              # Backend engine (Health polling & AI)
│   ├── monitor.py        # Main execution loop
│   └── config.py         # API endpoints and service settings
├── data/                 # Shared volume for JSON persistence
├── docker-compose.yml    # Container orchestration
├── Dockerfile            # Shared build logic for both services
└── requirements.txt      # Project-wide dependencies
