#!/usr/bin/env python3

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta
import logging

# Setup logging
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log_file = "/tmp/order_reminders_log.txt"

# GraphQL transport
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate date range
seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

# GraphQL query
query = gql("""
query GetRecentOrders($date: Date!) {
  orders(orderDate_Gte: $date) {
    id
    customer {
      email
    }
  }
}
""")

# Execute query
try:
    result = client.execute(query, variable_values={"date": seven_days_ago})
    orders = result.get("orders", [])

    with open(log_file, "a") as log:
        for order in orders:
            order_id = order["id"]
            email = order["customer"]["email"]
            log.write(f"{timestamp} - Order ID: {order_id}, Email: {email}\n")

    print("Order reminders processed!")

except Exception as e:
    with open(log_file, "a") as log:
        log.write(f"{timestamp} - ERROR: {str(e)}\n")
    print("Failed to process order reminders.")
