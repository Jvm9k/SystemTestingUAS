#!/usr/bin/env python
"""
Flask application launcher
Run this file to start the development server
"""
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

from app.routes import app

if __name__ == '__main__':
    print("Starting Task Management System API...")
    print("Server running at http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    app.run(debug=True, host='localhost', port=5000)
