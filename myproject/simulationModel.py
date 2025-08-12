from scipy.stats import poisson
import json
import os
from prosessData import calculate_final_team_stats 
from fetchData import retrieve_matches_for_team, calculate_league_averages

def predict_match(home_team_id, away_team_id, league_id):
    """
    Simulates a match by dynamically calculating team stats based on current season performance,
    using the previous season's data as a baseline during transitional periods.

    :param home_team_id: The ID for the home team.
    :param away_team_id: The ID for the away team.
    :param league_id: The ID for the league the match is in.
    :return: A dictionary containing the prediction probabilities and details.
    """
    print("running")
    current_season = 2025 # This can be updated as new seasons begin

    # 1. Calculate current league-wide goal averages
    all_matches_current_season = retrieve_matches_for_team(league_id, current_season, team_id=None) or []
    if not all_matches_current_season:
        return {"error": f"No match data found for the league in season {current_season} to calculate averages."}
    
    league_averages = calculate_league_averages(all_matches_current_season)
    print("got league averages")
    # 2. Calculate dynamic stats for both teams
    home_team_stats = calculate_final_team_stats(current_season, league_id, home_team_id, league_averages)
    away_team_stats = calculate_final_team_stats(current_season, league_id, away_team_id, league_averages)
    print("successfully calculated team stats")
    # 3. Calculate expected goals (lambda) using dynamic strengths
    lambda_home = (home_team_stats['attack_strength_home'] * away_team_stats['defense_strength_away'] * league_averages['avg_home_goals'])
                   
    lambda_away = (away_team_stats['attack_strength_away'] * home_team_stats['defense_strength_home'] * league_averages['avg_away_goals'])
    print("calculated expected goals")
    # 4. Simulate outcomes using the Poisson distribution
    max_goals = 7
    home_win_prob, away_win_prob, draw_prob = 0, 0, 0
    score_probabilities = {}

    for home_goals in range(max_goals + 1):
        for away_goals in range(max_goals + 1):
            prob = poisson.pmf(home_goals, lambda_home) * poisson.pmf(away_goals, lambda_away)
            scoreline = f"{home_goals}-{away_goals}"
            score_probabilities[scoreline] = round(prob * 100, 2)
            
            if home_goals > away_goals:
                home_win_prob += prob
            elif away_goals > home_goals:
                away_win_prob += prob
            else:
                draw_prob += prob
    # Normalize probabilities
    print("normalizing probabilities")
    most_likely_score = max(score_probabilities, key=score_probabilities.get)

    return {
        "home_team_win_probability": round(home_win_prob * 100, 2),
        "away_team_win_probability": round(away_win_prob * 100, 2),
        "draw_probability": round(draw_prob * 100, 2),
        "predicted_goals_home": round(lambda_home, 2),
        "predicted_goals_away": round(lambda_away, 2),
        "most_likely_score": f"{most_likely_score} ({score_probabilities[most_likely_score]}%)",
        "score_probabilities": score_probabilities
    }

# Example of how to run it directly
if __name__ == '__main__':

  
    prediction = predict_match(home_team_id=64, away_team_id=66, league_id=2021)
    print("--- Dynamic Match Simulation Result ---")
    print(json.dumps(prediction, indent=4))