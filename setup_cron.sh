#!/bin/bash
# Setup cron job for daily news digest

# Get current crontab
crontab -l > /tmp/current_cron 2>/dev/null

# Define the cron job (8 AM daily)
PROJECT_PATH="/Users/a90362/Documents/D/AI_Project/claude-code/00-News-Aggregator-Oct2025"
CRON_JOB="0 8 * * * cd ${PROJECT_PATH} && ${PROJECT_PATH}/venv/bin/python3 ${PROJECT_PATH}/daily_digest.py >> ${PROJECT_PATH}/logs/digest.log 2>&1"

# Check if job already exists
if grep -q "daily_digest.py" /tmp/current_cron 2>/dev/null; then
    echo "Cron job already exists. Updating..."
    grep -v "daily_digest.py" /tmp/current_cron > /tmp/new_cron
    echo "${CRON_JOB}" >> /tmp/new_cron
else
    echo "Adding new cron job..."
    cp /tmp/current_cron /tmp/new_cron 2>/dev/null || touch /tmp/new_cron
    echo "${CRON_JOB}" >> /tmp/new_cron
fi

# Install new crontab
crontab /tmp/new_cron

# Clean up
rm /tmp/current_cron /tmp/new_cron 2>/dev/null

echo "✓ Cron job installed successfully!"
echo ""
echo "Your daily news digest will run at 8:00 AM every day"
echo ""
echo "To verify, run: crontab -l"
echo "To change the time, run: crontab -e"
