#!/usr/bin/env python3
"""
Test runner for SalesForecaster application.
Runs all tests with coverage reporting and generates HTML report.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return None

def main():
    """Run all tests with coverage."""
    print("🧪 SalesForecaster Test Suite")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("tests").exists():
        print("❌ Error: tests directory not found. Run from project root.")
        sys.exit(1)
    
    # Run unit tests with coverage
    coverage_cmd = [
        "python", "-m", "pytest", 
        "tests/", 
        "--cov=App", 
        "--cov=FlaskBackend",
        "--cov-report=html:htmlcov",
        "--cov-report=term-missing",
        "-v"
    ]
    
    result = run_command(" ".join(coverage_cmd), "Running unit tests with coverage")
    
    if result is None:
        print("\n❌ Tests failed. Fix issues before continuing.")
        sys.exit(1)
    
    # Run integration tests
    integration_result = run_command(
        "python -m pytest tests/test_integration.py -v",
        "Running integration tests"
    )
    
    if integration_result is None:
        print("\n⚠️  Integration tests failed. Check application setup.")
    
    # Generate coverage summary
    print("\n📊 Coverage Summary:")
    print("-" * 30)
    
    coverage_summary = run_command(
        "python -m coverage report --show-missing",
        "Generating coverage summary"
    )
    
    if coverage_summary:
        print(coverage_summary)
    
    # Open coverage report in browser (if available)
    html_report = Path("htmlcov/index.html")
    if html_report.exists():
        print(f"\n📈 Coverage report generated: {html_report.absolute()}")
        print("Open htmlcov/index.html in your browser to view detailed coverage.")
    
    print("\n✅ Test suite completed!")
    print("\nNext steps:")
    print("1. Review any failed tests")
    print("2. Check coverage report")
    print("3. Fix any issues before deployment")

if __name__ == "__main__":
    main()
