from flask import Flask, jsonify, send_from_directory, request
import json
import os
from prosessData import process_last_X_games
from fetchData import load_team_data, load_team_match_upcoming_match
# Import your new prediction function
from simulationModel import predict_match
from flask_cors import CORS

app = Flask(__name__)

# Enhanced CORS configuration
CORS(app, 
     origins=['*'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'],
     supports_credentials=True)

# Add manual CORS headers as backup
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

# --- Test Routes for Debugging ---
@app.route('/test')
def test():
    return jsonify({
        "status": "running",
        "message": "Backend is working!",
        "cors": "enabled"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

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
    leagueId = request.args.get('leagueId', type=int)
    season = 2024
    if not leagueId:
        return jsonify({"error": "leagueId is required"}), 400
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
    """
    Gets the next upcoming match for a team, sorted by date.
    This version now correctly checks for both 'SCHEDULED' and 'TIMED' statuses.
    """
    try:
        upcoming_matches = load_team_match_upcoming_match(teamId)
        if not upcoming_matches or 'matches' not in upcoming_matches or not upcoming_matches['matches']:
            return jsonify({"error": "No upcoming matches found for this team."}), 404
        
        # 1. Filter for all matches that haven't been played yet
        scheduled_matches = [
            match for match in upcoming_matches['matches'] if match['status'] in ['SCHEDULED', 'TIMED']
        ]

        if not scheduled_matches:
            return jsonify({"error": "No scheduled matches found."}), 404
            
        # 2. Sort the matches by their date to find the earliest one
        scheduled_matches.sort(key=lambda x: x['utcDate'])
        
        # 3. The first match in the sorted list is the true next match
        next_match = scheduled_matches[0]
        
        return jsonify(next_match)
    except Exception as e:
        print(f"Error fetching next match: {e}")
        return jsonify({"error": "An error occurred while fetching the next match."}), 500
        

# --- NEW SIMULATION ROUTE ---
@app.route('/simulation/predict')
def run_prediction():
    """
    Runs the simulation based on home and away team IDs from the request.
    """
    home_id = request.args.get('home', type=int)
    away_id = request.args.get('away', type=int)
    league_id = request.args.get('leagueId', type=int)

    if not all([home_id, away_id, league_id]):
        return jsonify({"error": "Missing home, away, or leagueId parameters"}), 400

    try:
        prediction_result = predict_match(home_team_id=home_id, away_team_id=away_id, league_id=league_id)
        if "error" in prediction_result:
            return jsonify(prediction_result), 500
        return jsonify(prediction_result)
    except Exception as e:
        print(f"Error during simulation: {e}")
        return jsonify({"error": "An internal error occurred during the simulation."}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)