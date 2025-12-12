#!/bin/bash
# Activate the virtual environment and update requirements.txt with all installed packages
source venv/bin/activate
pip freeze > requirements.txt
echo "requirements.txt updated with current environment packages."
