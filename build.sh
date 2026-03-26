#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# NEW: The Safety Switch
if [ "$SEED_MOCK_DATA" = "True" ]; then
    echo "Safety switch is ON. Seeding mock data..."
    python manage.py setup_mock_data
else
    echo "Skipping mock data generation."
fi