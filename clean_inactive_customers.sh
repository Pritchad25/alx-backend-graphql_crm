#!/bin/bash

# Define timestamp
timestamp=$(date '+%Y-%m-%d %H:%M:%S')

# Run Django shell command to delete inactive customers
deleted_count=$(python manage.py shell << END
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(order__isnull=True, created_at__lt=one_year_ago)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
END
)

# Log result to file
echo "$timestamp - Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt
