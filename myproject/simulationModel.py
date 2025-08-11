from scipy.stats import poisson
import requests
import json
import os
from prosessData import *
from fetchData import *




def fetch_data(filename="epl_2024_stats.json"):
    """Load data from the mockApi.json file"""
    try:
        # Correctly locate mockApi.json in the same directory as this script
        json_file_path = os.path.join(os.path.dirname(__file__), '{filename}')
        with open(json_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"error": "Mock data file not found"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}
    

def process_previous_data(enough_data : bool, teamId):
    if not enough_data:
        previous__season_data=fetch_data(filename="epl_2024_stats.json")
        #get home and away team data: Attack Strength and Defense Strength, and league average home goals and away goals.
        avg_home_goals = previous__season_data['league_averages']['avg_home_goals']
        avg_away_goals = previous__season_data['league_averages']['avg_away_goals']
        avg_hometeam_attack_strength = previous__season_data['teams'][teamId]['attack_strength']

        


#main function to simulate the match
def simulate_match(current_season,leagueId,home_team_id, away_team_id):
    home_team_data= retrieve_matches_for_team(leagueId, current_season, teamId=home_team_id)
    away_team_data= retrieve_matches_for_team(leagueId, current_season, teamId=away_team_id)
    #determine if we need last season data since the current season is not sufficient
    enough_data=True
    if home_team_data[0]['season']['currentMatchday'] <8:
        enough_data=False
        process_previous_data(enough_data, home_team_id)
        