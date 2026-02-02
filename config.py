# config.py

SERVICES = [
    {
        "name": "GitHub",
        "url": "https://www.githubstatus.com/api/v2/status.json",
        "key_path": ["status", "description"]
    },
    {
        "name": "Slack",
        "url": "https://status.slack.com/api/v2.0.0/current",
        "key_path": ["status"]
    },
    {
        "name": "Atlassian", # Better than Google/Azure for testing logic
        "url": "https://status.atlassian.com/api/v2/status.json",
        "key_path": ["status", "description"]
    },
    {
        "name": "Cloudflare", # Extremely stable API
        "url": "https://www.cloudflarestatus.com/api/v2/status.json",
        "key_path": ["status", "description"]
    },
    {
        "name": "HashiCorp",
        "url": "https://status.hashicorp.com/api/v2/status.json",
        "key_path": ["status", "description"]
    },
    {
        "name": "Reddit", # Great for testing outages
        "url": "https://www.redditstatus.com/api/v2/status.json",
        "key_path": ["status", "description"]
    }
]

DATA_FILE = "data/status_history.json"