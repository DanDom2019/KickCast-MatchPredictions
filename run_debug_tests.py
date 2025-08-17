#!/usr/bin/env python3
"""
Comprehensive debug test runner for KickCast application
"""

import sys
import os

def test_imports():
    print("🔍 Testing imports...")
    print("=" * 50)
    
    try:
        from flask import Flask
        print("✅ Flask imported successfully")
    except Exception as e:
        print(f"❌ Flask import failed: {e}")
        return False

    try:
        from prosessData import process_last_X_games
        print("✅ prosessData imported successfully")
    except Exception as e:
        print(f"❌ prosessData import failed: {e}")
        return False

    try:
        from fetchData import load_team_data, load_team_match_upcoming_match
        print("✅ fetchData imported successfully")
    except Exception as e:
        print(f"❌ fetchData import failed: {e}")
        return False

    try:
        from simulationModel import predict_match
        print("✅ simulationModel imported successfully")
    except Exception as e:
        print(f"❌ simulationModel import failed: {e}")
        return False

    try:
        import requests
        print("✅ Requests imported successfully")
    except Exception as e:
        print(f"❌ Requests import failed: {e}")
        return False

    try:
        import pandas
        print("✅ Pandas imported successfully")
    except Exception as e:
        print(f"❌ Pandas import failed: {e}")
        return False

    try:
        import scipy
        print("✅ Scipy imported successfully")
    except Exception as e:
        print(f"❌ Scipy import failed: {e}")
        return False

    return True

def test_api_calls():
    print("\n🌐 Testing API calls...")
    print("=" * 50)
    
    try:
        from fetchData import load_team_data
        team_data = load_team_data(57)
        print("✅ API call successful:", team_data.get('name', 'Unknown'))
        return True
    except Exception as e:
        print(f"❌ API call failed: {e}")
        return False

def test_flask_app():
    print("\n🚀 Testing Flask app...")
    print("=" * 50)
    
    try:
        from app import app
        print("✅ Flask app imported successfully")
        
        # Test creating a test client
        with app.test_client() as client:
            response = client.get('/test')
            if response.status_code == 200:
                print("✅ Test endpoint working")
                return True
            else:
                print(f"❌ Test endpoint failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def main():
    print("🧪 KickCast Debug Test Suite")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test API calls
    api_ok = test_api_calls()
    
    # Test Flask app
    flask_ok = test_flask_app()
    
    print("\n📊 Test Results Summary")
    print("=" * 50)
    print(f"Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"API Calls: {'✅ PASS' if api_ok else '❌ FAIL'}")
    print(f"Flask App: {'✅ PASS' if flask_ok else '❌ FAIL'}")
    
    if all([imports_ok, api_ok, flask_ok]):
        print("\n🎉 All tests passed! Your app should work.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
    
    return all([imports_ok, api_ok, flask_ok])

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
