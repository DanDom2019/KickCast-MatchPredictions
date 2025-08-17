# test_api.py
from fetchData import load_team_data

try:
    team_data = load_team_data(57)
    print("✅ API call successful:", team_data.get('name', 'Unknown'))
except Exception as e:
    print(f"❌ API call failed: {e}")
