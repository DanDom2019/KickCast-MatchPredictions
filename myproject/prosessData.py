from fetchData import *

def process_preious_matches(leagueId, teamId,season=None):
    matches= retrieve_matches_for_team(leagueId,season, teamId, 10)
    last_match= matches[0]
    last_match_result= matches[0]['full_time_score']
