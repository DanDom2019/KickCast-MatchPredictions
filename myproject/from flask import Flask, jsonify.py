from flask import Flask, jsonify

app = Flask(__name__)

# This route simulates fetching player data for a team
@app.route('/mock-api/team/<team_name>')
def get_team_data(team_name):
    
    # --- This is your fake data ---
    # It should have the same structure as the real API's response.
    fake_player_data = {
        "team_name": team_name,
        "players": [
            {"player_id": 1, "name": "John Doe", "position": "ST", "fc25_rating": 88, "form_rating": 8.1},
            {"player_id": 2, "name": "Jane Smith", "position": "CAM", "fc25_rating": 91, "form_rating": 7.5},
            {"player_id": 3, "name": "Peter Jones", "position": "LW", "fc25_rating": 85, "form_rating": 8.8}
        ]
    }
    
    # The jsonify function correctly formats your dictionary as a JSON response.
    return jsonify(fake_player_data)

if __name__ == '__main__':
    app.run(debug=True)