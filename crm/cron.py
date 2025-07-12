from datetime import datetime
import requests

def log_crm_heartbeat():
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    message = f"{timestamp} CRM is alive"

    # Optional: Check GraphQL hello field
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code == 200:
            message += " | GraphQL OK"
        else:
            message += f" | GraphQL ERROR {response.status_code}"
    except Exception as e:
        message += f" | GraphQL EXCEPTION: {str(e)}"

    with open("/tmp/crm_heartbeat_log.txt", "a") as log:
        log.write(message + "\n")
