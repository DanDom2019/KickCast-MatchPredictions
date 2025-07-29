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

if __name__ == "__main__":

    data = fetch(f"/competitions/{2015}/teams")
    # Summarize leagues by printing id and name
    teams = data.get('teams', [])
    print("League ID - Name:")
    for team in teams:
        print(f"{team['id']} - {team['name']}")