from fetchData import *
import json
from datetime import datetime
import os



def process_preious_matches(leagueId, teamId,season=None):
    matches= retrieve_matches_for_team(leagueId,season, teamId, 10)
    last_match= matches[0]
    last_match_result= matches[0]['full_time_score']


#showcase the last 10 games info.
def process_last_X_games(leagueId, teamId, season=None,matches=None, X=10):
    """
    Processes the last 10 games for a specific team in a league.
    :param leagueId: The ID of the league.
    :param teamId: The ID of the team.
    :param season: Optional season to filter matches.
    :return: A dictionary with processed match data.
    """
    if matches is None:
        matches = retrieve_matches_for_team(leagueId, season, teamId, X)
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





def fetch_data(filename="foundationData/2024Season/epl_2024_stats.json"):
    """Load data from the mockApi.json file"""
    try:
        # Correctly locate mockApi.json in the same directory as this script
        json_file_path = os.path.join(os.path.dirname(__file__), f'{filename}')
        with open(json_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filename} not found")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file {filename}")
    

def get_season_weights(matches_played, transition_period=8):
    """
    Calculates the weights for the previous and current seasons.
    """
    if matches_played >= transition_period:
        return 0.0, 1.0  # 0% for previous, 100% for current

    weight_prev = (transition_period - matches_played) / transition_period
    weight_curr = matches_played / transition_period
    
    return weight_prev, weight_curr
        

def calculate_current_season_averages(team_id, current_matches):
    """Calculates goal averages for a team based on a list of current matches."""
    home_goals_scored, home_conceded, home_matches = 0, 0, 0
    away_goals_scored, away_conceded, away_matches = 0, 0, 0

    for match in current_matches:
        if match['homeTeam']['id'] == team_id:
            home_matches += 1
            home_goals_scored += match['score']['fullTime']['home']
            home_conceded += match['score']['fullTime']['away']
        elif match['awayTeam']['id'] == team_id:
            away_matches += 1
            away_goals_scored += match['score']['fullTime']['away']
            away_conceded += match['score']['fullTime']['home']
    
    return {
        "avg_home_scored": home_goals_scored / home_matches if home_matches > 0 else 0,
        "avg_home_conceded": home_conceded / home_matches if home_matches > 0 else 0,
        "avg_away_scored": away_goals_scored / away_matches if away_matches > 0 else 0,
        "avg_away_conceded": away_conceded / away_matches if away_matches > 0 else 0,
    }



#main function to simulate the match
def calculate_final_team_stats(current_season,leagueId,team_id,league_averages):
    team_matches= retrieve_matches_for_team(leagueId, current_season, team_id,numsMatches=None,noMatch=True) or []
    #determine if we need last season data since the current season is not sufficient
    enough_matches=8
    
    if len(team_matches)==0:
            prev_averages=fetch_data(filename="foundationData/2024Season/epl_2024_stats.json")
            team_stats= prev_averages['teams'][str(team_id)]
            return {
            "attack_strength_home": team_stats['attack_strength_home'],
            "defense_strength_home": team_stats['defense_strength_home'],
            "attack_strength_away": team_stats['attack_strength_away'],
            "defense_strength_away": team_stats['defense_strength_away']
        }
    #process the simulation data
    if 0<len(team_matches) <enough_matches:
        weight_prev, weight_curr = get_season_weights(len(team_matches), transition_period=enough_matches)
        previous__season_data=fetch_data(filename="foundationData/2024Season/epl_2024_stats.json")
        prev_averages=previous__season_data['teams'][str(team_id)]
        curr_averages= calculate_current_season_averages(team_id, team_matches)
        
        avg_home_scored = (weight_prev * prev_averages['avg_home_scored']) + (weight_curr * curr_averages['avg_home_scored'])
        avg_home_conceded = (weight_prev * prev_averages['avg_home_conceded']) + (weight_curr * curr_averages['avg_home_conceded'])
        avg_away_scored = (weight_prev * prev_averages['avg_away_scored']) + (weight_curr * curr_averages['avg_away_scored'])
        avg_away_conceded = (weight_prev * prev_averages['avg_away_conceded']) + (weight_curr * curr_averages['avg_away_conceded'])

    else: # 8 or more matches
            stats_source = calculate_current_season_averages(team_id, team_matches)
            avg_home_scored = stats_source['avg_home_scored']
            avg_home_conceded = stats_source['avg_home_conceded']
            avg_away_scored = stats_source['avg_away_scored']
            avg_away_conceded = stats_source['avg_away_conceded']

    #final calculation of the team stats
    
    attack_strength_home = avg_home_scored / league_averages['avg_home_goals'] if league_averages['avg_home_goals'] > 0 else 0
    defense_strength_home = avg_home_conceded / league_averages['avg_away_goals'] if league_averages['avg_away_goals'] > 0 else 0
    attack_strength_away = avg_away_scored / league_averages['avg_away_goals'] if league_averages['avg_away_goals'] > 0 else 0
    defense_strength_away = avg_away_conceded / league_averages['avg_home_goals'] if league_averages['avg_home_goals'] > 0 else 0
    
    return {
        "attack_strength_home": round(attack_strength_home, 3),
        "defense_strength_home": round(defense_strength_home, 3),
        "attack_strength_away": round(attack_strength_away, 3),
        "defense_strength_away": round(defense_strength_away, 3),
    }

if __name__ == "__main__":
    leagueId = 2021  # Example league ID for Premier League
    team_id = 65 # Example team ID for Manchester City
    season = 2025 # Example season

    league_average=calculate_league_averages(retrieve_matches_for_team(leagueId, season, team_id=None))
    team_stats= calculate_final_team_stats(season, leagueId, team_id, league_average)
    print(team_stats)
