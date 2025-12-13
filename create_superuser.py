#!/usr/bin/env python
"""
Script to create a superuser in the production database.
Set environment variables before running:
  export DB_NAME=postgres
  export DB_USER=postgres
  export DB_PASSWORD=rocklee123
  export DB_HOST=35.236.10.79
  export DB_PORT=5432
"""
import os
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings.prod')

# Setup Django
django.setup()

from django.contrib.auth.models import User

def create_superuser(username, email, password):
    """Create a superuser account"""
    if User.objects.filter(username=username).exists():
        print(f"Superuser '{username}' already exists.")
        return False
    
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created successfully!")
    return True

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python create_superuser.py <username> <email> <password>")
        print("Example: python create_superuser.py admin admin@example.com mypassword")
        sys.exit(1)
    
    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    
    create_superuser(username, email, password)
