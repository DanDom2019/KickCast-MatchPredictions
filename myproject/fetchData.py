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


def load_seasons_matches_history(leagueId, season=None):
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
    data = fetch(f"/competitions/{leagueId}/matches", params=params)
    if not data:
        print(f"Failed to fetch matches for season {season}")
        return 
    if data['resultSet']['count'] == 0:
        print(f"No matches found for season {season}")
        return 

    matches = data['matches']
    return matches
    
#fetch the matches based on the team id and season and numbers of matches as requested
def retrieve_matches_for_team(leagueId,season, team_id, numsMatches):
    start_season=season
    matches = load_seasons_matches_history(leagueId=leagueId, season=season)
    # check if we need to include the previous seasons as well
    #if there is no matches for the current season, we can fetch the previous seasons
    combo = False
    noShow = False
    if matches is None:
        noShow=True
        season = season - 1
        # Fetch matches for the previous season
        matches = load_seasons_matches_history(leagueId=leagueId, season=season)
        if matches is None:
            matches = []
      #if current season matches dont have enough matches, we can fetch the previous seasons
    if team_id:
        # Filter matches involving the specified team
        matches = filter_matches_by_team_id(team_id, matches)
        current_matches_count = len(matches)
        if current_matches_count < numsMatches:
            # Fetch matches from previous seasons until we have enough matches
            while current_matches_count < numsMatches:
                combo=True
                season -= 1
                previous_matches = load_seasons_matches_history(leagueId=leagueId, season=season)
                if not previous_matches:
                    print(f"No more matches found for season {season}")
                    break
                previous_matches = filter_matches_by_team_id(team_id, previous_matches)
                matches.extend(previous_matches)
                current_matches_count = len(matches)

    if not numsMatches:
      print(f"Found {len(matches)} matches for team ID {team_id} in season {start_season}")
    else:
      # Fix the lambda variable from 'numsMatches' to 'match'
      matches.sort(key=lambda match: match['utcDate'], reverse=True)
      final_matches = matches[:numsMatches] # Get the final list

      # print an accurate message based on the flags and stored season
      if combo is False and noShow is False:
        print(f" Found {len(final_matches)} matches for team ID {team_id} in season {start_season}")
      elif noShow is True:
        print(f"Found {len(final_matches)} matches for team ID {team_id} from season {start_season - 1} and earlier.")
      else: # This means 'combo' is True
        print(f"Found {len(final_matches)} matches for team ID {team_id} by combining season {start_season} with previous seasons.")
      
      return final_matches
    return matches


def filter_matches_by_team_id(team_id, matches):
    matches = [match for match in matches if match['homeTeam']['id'] == team_id or match['awayTeam']['id'] == team_id]
    return matches

#test and example usage
if __name__ == "__main__":

    data=retrieve_matches_for_team(leagueId=2021, season=2025 , team_id=563, numsMatches=40)
    # Summarize leagues by printing id and name
    print(data)
