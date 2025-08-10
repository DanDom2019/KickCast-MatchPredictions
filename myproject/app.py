from flask import Flask, jsonify, send_from_directory
import json
import os
from prosessData import process_preious_matches, process_last_10_games
from fetchData import load_team_data

app = Flask(__name__, static_folder='.')

# --- JSON Data Loading ---
def fetch_data():
    """Load data from the mockApi.json file"""
    try:
        # Correctly locate mockApi.json in the same directory as this script
        json_file_path = os.path.join(os.path.dirname(__file__), 'mockApi.json')
        with open(json_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"error": "Mock data file not found"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}

# --- Frontend Routes (Serving HTML, JS, JSON) ---

@app.route('/')
def serve_index():
    """Serves the main index.html page."""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """
    Serves any other file requested by the frontend.
    This single route handles requests for:
    - script.js
    - team-selector.js
    - foundationData/leagues.json
    - and any other file in that directory or its subdirectories.
    """
    return send_from_directory('.', path)

# --- API Routes ---

@app.route('/app/match')
def get_match_data():
    """Get complete match information"""
    data = fetch_data()
    if "error" in data:
        return jsonify(data), 404
    return jsonify(data.get("match", {}))

@app.route('/api/team/<int:teamId>')
def get_team_by_id(teamId):
    """
    Fetches detailed data for a specific team using its ID.
    """
    try:
       
        team_data = load_team_data(teamId) 
        if not team_data:
            return jsonify({"error": "Team not found"}), 404
        return jsonify(team_data)
    except Exception as e:
        return jsonify({"error": "An error occurred on the server"}), 500


@app.route('/app/prediction')
def get_prediction_data():
    """Get all prediction data including head-to-head and form"""
    data = fetch_data()
    if "error" in data:
        return jsonify(data), 404
    return jsonify(data.get("prediction_data", {}))

@app.route('/app/head-to-head')
def get_head_to_head():
    """Get head-to-head match history"""
    data = fetch_data()
    if "error" in data:
        return jsonify(data), 404
    return jsonify(data.get("prediction_data", {}).get("head_to_head", []))

@app.route('/app/form/<team_type>')
def get_team_form(team_type):
    """Get form data for home or away team"""
    data = fetch_data()
    if "error" in data:
        return jsonify(data), 404

    if team_type.lower() not in ['home', 'away']:
        return jsonify({"error": "Team type must be 'home' or 'away'"}), 400

    form_key = f"{team_type.lower()}_team_form"
    return jsonify(data.get("prediction_data", {}).get(form_key, {}))


@app.route('/app/team/<int:teamId>/last10matches')
def get_last_10_matches(teamId, leagueId=2021, season=2024):
    """
    Get the last 10 processed matches for a given team.
    Note: You will need to determine the correct leagueId and season,
    or modify process_last_10_games to not require them if they are not needed.
    For this example, we'll use a placeholder for leagueId and season.
    """
    # Placeholder leagueId and season, as they are required by your function.
    # You might want to make these dynamic in a real application.
    leagueId = 2021 # Example: Premier League
    season = 2024   # Example: 2024 season

    try:
        matches = process_last_10_games(leagueId=leagueId, teamId=teamId, season=season)
        if not matches:
            return jsonify({"error": "No matches found for this team."}), 404
        return jsonify(matches)
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching match data."}), 500

if __name__ == '__main__':
    # Update the app.run() call if necessary
    app.run(debug=True, port=5000)