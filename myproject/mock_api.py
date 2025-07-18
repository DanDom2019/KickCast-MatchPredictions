from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Load JSON data from file
def load_mock_data():
    """Load data from the mockApi.json file"""
    try:
        json_file_path = os.path.join(os.path.dirname(__file__), 'mockApi.json')
        with open(json_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"error": "Mock data file not found"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}

# Route to get complete match data
@app.route('/mock-api/match')
def get_match_data():
    """Get complete match information"""
    data = load_mock_data()
    if "error" in data:
        return jsonify(data), 404
    return jsonify(data["match"])

# Route to get team player data
@app.route('/mock-api/team/<team_type>')
def get_team_data(team_type):
    """Get player data for home or away team"""
    data = load_mock_data()
    if "error" in data:
        return jsonify(data), 404
    
    if team_type.lower() not in ['home', 'away']:
        return jsonify({"error": "Team type must be 'home' or 'away'"}), 400
    
    # Get team info and players
    team_key = f"{team_type.lower()}_team"
    team_info = data["match"][f"{team_type.lower()}Team"]
    players = data["prediction_data"]["player_stats"][team_key]
    
    # Calculate average form rating for each player
    for player in players:
        if "last_five_ratings" in player:
            player["form_rating"] = round(sum(player["last_five_ratings"]) / len(player["last_five_ratings"]), 1)
    
    result = {
        "team_name": team_info["name"],
        "team_short_name": team_info["shortName"],
        "team_id": team_info["id"],
        "crest": team_info["crest"],
        "players": players
    }
    
    return jsonify(result)

# Route to get prediction data
@app.route('/mock-api/prediction')
def get_prediction_data():
    """Get all prediction data including head-to-head and form"""
    data = load_mock_data()
    if "error" in data:
        return jsonify(data), 404
    return jsonify(data["prediction_data"])

# Route to get head-to-head data
@app.route('/mock-api/head-to-head')
def get_head_to_head():
    """Get head-to-head match history"""
    data = load_mock_data()
    if "error" in data:
        return jsonify(data), 404
    return jsonify(data["prediction_data"]["head_to_head"])

# Route to get team form
@app.route('/mock-api/form/<team_type>')
def get_team_form(team_type):
    """Get form data for home or away team"""
    data = load_mock_data()
    if "error" in data:
        return jsonify(data), 404
    
    if team_type.lower() not in ['home', 'away']:
        return jsonify({"error": "Team type must be 'home' or 'away'"}), 400
    
    form_key = f"{team_type.lower()}_team_form"
    return jsonify(data["prediction_data"][form_key])

if __name__ == '__main__':
    app.run(debug=True)