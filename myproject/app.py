from flask import Flask, jsonify, send_from_directory, request
import json
import os
from prosessData import process_last_X_games
from fetchData import load_team_data, load_team_match_upcoming_match

app = Flask(__name__, static_folder='.')

# --- JSON Data Loading ---
def fetch_data():
    """Load data from the mockApi.json file"""
    try:
        json_file_path = os.path.join(os.path.dirname(__file__), 'mockApi.json')
        with open(json_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"error": "Mock data file not found"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}

# --- Frontend Routes ---

@app.route('/')
def serve_index():
    """Serves the main index.html page."""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """Serves any other file requested by the frontend."""
    return send_from_directory('.', path)

# --- API Routes ---

@app.route('/api/team/<int:teamId>')
def get_team_by_id(teamId):
    """Fetches detailed data for a specific team using its ID."""
    try:
        team_data = load_team_data(teamId) 
        if not team_data:
            return jsonify({"error": "Team not found"}), 404
        return jsonify(team_data)
    except Exception as e:
        print(f"Error in get_team_by_id: {e}")
        return jsonify({"error": "An error occurred on the server"}), 500

@app.route('/app/team/<int:teamId>/last10matches')
def get_last_10_matches(teamId):
    """Get the last 10 processed matches for a given team."""
    leagueId = request.args.get('leagueId', default=2021, type=int)  
    season = 2024
    try:
        matches = process_last_X_games(leagueId=leagueId, teamId=teamId, season=season)
        if not matches:
            return jsonify({"error": "No matches found for this team."}), 404
        return jsonify(matches)
    except Exception as e:
        print(f"Error in get_last_10_matches: {e}")
        return jsonify({"error": "An error occurred while fetching match data."}), 500

@app.route('/api/team/<int:teamId>/next_match')
def get_next_match(teamId):
    """Get the next upcoming match for a team."""
    try:
        upcoming_matches = load_team_match_upcoming_match(teamId)
        if not upcoming_matches or not upcoming_matches.get('matches'):
            return jsonify({"error": "No upcoming matches found for this team."}), 404
        
        next_match = upcoming_matches['matches'][0]
        return jsonify(next_match)
    except Exception as e:
        print(f"Error fetching next match: {e}")
        return jsonify({"error": "An error occurred while fetching the next match."}), 500

@app.route('/app/prediction')
def get_prediction_data():
    """Returns mock prediction data."""
    data = fetch_data()
    if "error" in data:
        return jsonify(data), 404
    return jsonify(data.get("prediction_data", {}))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
