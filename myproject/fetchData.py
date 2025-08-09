import requests

API_TOKEN = "5d5cbeda806945ef9b31088d6bce37e3"
BASE_URL   = "https://api.football-data.org/v4"


def fetch(path, params=None):
    url     = BASE_URL + path
    headers = {
      "X-Auth-Token": API_TOKEN,
      "Accept":       "application/json"
    }
    resp = requests.get(url, headers=headers, params=params or {})
    resp.raise_for_status()
    return resp.json()

def fetch_leagues_teams():
    data = fetch("/competitions")
    return data

def fetch_teams():
    data = fetch("/teams")
    return data

def load_team_data(teamId : int):
    """
    Fetches teams for a specific league.
    :param leagueid: The ID of the league to fetch teams for.
    :return: A list of teams in the specified league.
    """
    data = fetch(f"/teams/{teamId}")
    return data

def load_team_match_upcoming_match(teamId : int):
    """
    Fetches match history for a specific team.
    :param teamId: The ID of the team to fetch matches for.
    :return: A list of matches played by the specified team.
    """
    data = fetch(f"/teams/{teamId}/matches")
    return data

def load_last_10_match(teamId : int):
    """
    Fetches the last 10 matches for a specific team.
    :param teamId: The ID of the team to fetch matches for.
    :return: A list of the last 10 matches played by the specified team.
    """
    data = fetch(f"/teams/{teamId}/matches?status=FINISHED&limit=10")
    return data


def load_previous_matches_history(season=None, team_id=None):
    """
    Fetches all Premier League matches for a given season.
    Optionally filters for a specific team.
    :param season: The year of the season (e.g., 2024 for 2024-25).
    :param team_id: Optional team ID to filter matches for a specific team.
    :return: A list of matches.
    """
    params = {
        "status": "FINISHED",
        "season": season
    }
    data = fetch("/competitions/2021/matches", params=params)
    if not data:
        print(f"Failed to fetch matches for season {season}")
        return []
    if data['resultSet']['count'] == 0:
        print(f"No matches found for season {season}")
        return []

    matches = data['matches']
    if team_id:
        # Filter matches involving the specified team
        matches = [match for match in matches if match['homeTeam']['id'] == team_id or match['awayTeam']['id'] == team_id]
        print(f"Found {len(matches)} matches for team ID {team_id} in season {season}")
    return matches


if __name__ == "__main__":

    data=load_previous_matches_history(65)  # Example team ID for Manchester City
    # Summarize leagues by printing id and name
    print(data)
