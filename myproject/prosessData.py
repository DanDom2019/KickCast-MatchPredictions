from fetchData import *
import json
from datetime import datetime



def process_preious_matches(leagueId, teamId,season=None):
    matches= retrieve_matches_for_team(leagueId,season, teamId, 10)
    last_match= matches[0]
    last_match_result= matches[0]['full_time_score']


#showcase the last 10 games info.
def process_last_10_games(leagueId, teamId, season=None,matches=None):
    """
    Processes the last 10 games for a specific team in a league.
    :param leagueId: The ID of the league.
    :param teamId: The ID of the team.
    :param season: Optional season to filter matches.
    :return: A dictionary with processed match data.
    """
    if matches is None:
        matches = retrieve_matches_for_team(leagueId, season, teamId, 10)
    team_matches=[]
    
    for match in matches:
        #check hoeme or away
        is_home=match['homeTeam']['id'] == teamId
        is_away=match['awayTeam']['id'] == teamId
        if not (is_home or is_away):
            continue
        #extract the opponents
        opps=match['awayTeam']['name'] if is_home else match['homeTeam']['name']
        #extract the scores
        score=f"{match['score']['fullTime']['home']} - {match['score']['fullTime']['away']}"

        winner = match['score']['winner']
        if winner == "DRAW":
            result = "Draw"
        elif (winner == "HOME_TEAM" and is_home) or (winner == "AWAY_TEAM" and is_away):
            result = "Win"
        else:
            result = "Loss"

        date = datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')

        #grab the matches day,date, opponent, score, and result from the team
        match_day = match['matchday'] 
        
        processed_data = {
            "matchDay": match_day,
            "date": date,
            "opponent": opps,
            "score": score,
            "result": result
        }
        team_matches.append(processed_data)
    return team_matches



if __name__ == "__main__":
    leagueId = 2021  # Example league ID for Premier League
    teamId = 66  # Example team ID for Manchester City
    season = "2024"  # Example season

    last_10_games = process_last_10_games(leagueId, teamId, season)

    print(last_10_games)
