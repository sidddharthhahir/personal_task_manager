#!/usr/bin/env python
"""
Quick server runner script for Personal Task Manager
Run this file to start the development server quickly
"""

import os
import sys
import subprocess

def main():
    print("🚀 Starting Personal Task Manager...")
    print("=" * 50)

    # Check if virtual environment exists
    venv_path = "venv"
    if not os.path.exists(venv_path):
        print("❌ Virtual environment not found!")
        print("Please run the setup first:")
        print("1. python -m venv venv")
        print("2. Activate venv and install requirements")
        return

    # Check if Django is installed
    try:
        import django
        print(f"✅ Django {django.get_version()} found")
    except ImportError:
        print("❌ Django not installed!")
        print("Please install requirements: pip install -r requirements.txt")
        return

    # Check if migrations are applied
    if not os.path.exists("db.sqlite3"):
        print("⚠️  Database not found. Running migrations...")
        subprocess.run([sys.executable, "manage.py", "migrate"])

    print("🌐 Starting development server...")
    print("📱 Open your browser and go to: http://localhost:8000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)

    # Start the server
    subprocess.run([sys.executable, "manage.py", "runserver"])

if __name__ == "__main__":
    main()
