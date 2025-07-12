from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def update_low_stock():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_file = "/tmp/low_stock_updates_log.txt"

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    mutation = gql("""
    mutation {
      updateLowStockProducts {
        updatedProducts {
          name
          stock
        }
        message
      }
    }
    """)

    try:
        result = client.execute(mutation)
        updates = result["updateLowStockProducts"]["updatedProducts"]
        message = result["updateLowStockProducts"]["message"]

        with open(log_file, "a") as log:
            log.write(f"{timestamp} - {message}\n")
            for product in updates:
                log.write(f"{timestamp} - {product['name']}: {product['stock']}\n")

    except Exception as e:
        with open(log_file, "a") as log:
            log.write(f"{timestamp} - ERROR: {str(e)}\n")
