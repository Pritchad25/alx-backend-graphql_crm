#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the root of the Django project
cd "$SCRIPT_DIR/../.." || exit 1  # Assuming script is in crm/cron_jobs/

# Get current working directory
cwd=$(pwd)

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

# Check if deletion succeeded
if [ $? -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted $deleted_count inactive customers from $cwd" >> /tmp/customer_cleanup_log.txt
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ERROR: Failed to delete customers" >> /tmp/customer_cleanup_log.txt
fi


# Log result to file
echo "$timestamp - Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt
