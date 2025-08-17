# test_imports.py
try:
    from flask import Flask
    print("✅ Flask imported successfully")
except Exception as e:
    print(f"❌ Flask import failed: {e}")

try:
    from prosessData import process_last_X_games
    print("✅ prosessData imported successfully")
except Exception as e:
    print(f"❌ prosessData import failed: {e}")

try:
    from fetchData import load_team_data, load_team_match_upcoming_match
    print("✅ fetchData imported successfully")
except Exception as e:
    print(f"❌ fetchData import failed: {e}")

try:
    from simulationModel import predict_match
    print("✅ simulationModel imported successfully")
except Exception as e:
    print(f"❌ simulationModel import failed: {e}")