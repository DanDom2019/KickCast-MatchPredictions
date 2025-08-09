from flask import Flask, jsonify, send_from_directory
import json
import os

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

@app.route('/app/team/<team_type>')
def get_team_data(team_type):
    """Get player data for home or away team"""
    data = fetch_data()
    if "error" in data:
        return jsonify(data), 404

    if team_type.lower() not in ['home', 'away']:
        return jsonify({"error": "Team type must be 'home' or 'away'"}), 400

    team_key = f"{team_type.lower()}_team"
    team_info = data.get("match", {}).get(f"{team_type.lower()}Team", {})
    players = data.get("prediction_data", {}).get("player_stats", {}).get(team_key, [])

    for player in players:
        if "last_five_ratings" in player and player["last_five_ratings"]:
            player["form_rating"] = round(sum(player["last_five_ratings"]) / len(player["last_five_ratings"]), 1)

    result = {
        "team_name": team_info.get("name"),
        "team_short_name": team_info.get("shortName"),
        "team_id": team_info.get("id"),
        "crest": team_info.get("crest"),
        "players": players
    }
    return jsonify(result)

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

if __name__ == '__main__':
    # Update the app.run() call if necessary
    app.run(debug=True, port=5000)