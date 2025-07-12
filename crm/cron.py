from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    message = f"{timestamp} CRM is alive"

    # GraphQL transport setup
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Simple query to verify endpoint
    try:
        query = gql("{ hello }")
        result = client.execute(query)
        hello_response = result.get("hello", "No response")
        message += f" | GraphQL says: {hello_response}"
    except Exception as e:
        message += f" | GraphQL ERROR: {str(e)}"

    with open("/tmp/crm_heartbeat_log.txt", "a") as log:
        log.write(message + "\n")
