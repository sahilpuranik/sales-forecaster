#!/usr/bin/env python
"""
Spin up both the Flask API (port 5000) and React-Vite dev server (port 3000)
with a single command:

    python app.py
"""
from __future__ import annotations

import subprocess
import sys
import os
import time
import requests

def start_backend():
    """Start the Flask backend server"""
    print("Starting Flask backend...")
    backend_process = subprocess.Popen([
        sys.executable, "FlaskBackend/run.py"
    ])
    return backend_process

def start_frontend():
    """Start the React frontend development server"""
    print("Starting React frontend...")
    os.chdir("ReactFrontEnd")
    frontend_process = subprocess.Popen([
        "npm", "run", "dev"
    ])
    os.chdir("..")
    return frontend_process

def wait_for_backend():
    """Wait for backend to be ready"""
    print("Waiting for backend to start...")
    for i in range(30):
        try:
            response = requests.get("http://localhost:5001/health", timeout=1)
            if response.status_code == 200:
                print("Backend is ready!")
                return True
        except:
            pass
        time.sleep(1)
    return False

def main():
    print("Starting Sales Forecasting Application...")
    
    # Start backend
    backend_process = start_backend()
    
    # Wait for backend to be ready
    if not wait_for_backend():
        print("Backend failed to start. Stopping...")
        backend_process.terminate()
        return
    
    # Start frontend
    frontend_process = start_frontend()
    
    print("\n" + "="*50)
    print("Sales Forecasting App is running!")
    print("Frontend: http://localhost:3000")
    print("Backend API: http://localhost:5001")
    print("API Docs: http://localhost:5001/docs")
    print("="*50)
    print("\nPress Ctrl+C to stop both servers")
    
    try:
        # Keep the main process running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Servers stopped.")

if __name__ == "__main__":
    main()