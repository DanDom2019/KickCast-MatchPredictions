# KickCast - Soccer Match Prediction

KickCast is a web-based application that predicts the outcomes of soccer matches using a Poisson distribution model. It provides probabilities for a home win, away win, or draw, along with the top five most likely scores. The application can be deployed locally and currently supports major European leagues, with plans for expansion.

## Features 

  * **Match Prediction:** Get predictions for upcoming matches, including win/loss/draw probabilities and the most likely scores.
  * **Team Statistics:** View detailed information for each team, including their last 10 matches.
  * **Dynamic Model:** The prediction model dynamically adjusts to team performance as the season progresses, using the previous season's data for early-season accuracy.
  * **Web Interface:** An intuitive web interface for selecting teams and viewing predictions.
  * **REST API:** A Flask-based REST API for fetching data and running simulations.

## How It Works 

The prediction model is based on the **Poisson distribution**, a statistical model that is well-suited for modeling the number of goals scored in a soccer match. The model calculates the expected number of goals for each team (lambda) based on their historical performance.

Here's a breakdown of the process:

1.  **Data Collection:** Match data, including scores, teams, and leagues, is fetched from the [football-data.org](https://www.football-data.org/) API.
2.  **Statistical Modeling:** The application calculates team-specific and league-wide statistics. For the early part of a new season, the model uses a weighted average of the previous season's and the current season's data. As more matches are played in the current season, the weight shifts towards the current season's data.
3.  **Poisson Distribution:** The Poisson distribution is used to calculate the probability of each team scoring a certain number of goals.
4.  **Outcome Probabilities:** By combining the probabilities of each possible scoreline, the model determines the overall probability of a home win, away win, or draw.

## Supported Leagues ⚽

The application currently supports the following leagues:

  * Premier League (England)
  * Ligue 1 (France)
  * Bundesliga (Germany)
  * Serie A (Italy)
  * Primera Division (La Liga) (Spain)

## Getting Started 🚀

To run the application locally, you'll need Python and the dependencies listed in `requirements.txt`.

### Prerequisites

  * Python 3.x
  * pip

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/dandom2019/footballmatchessimulation.git
    cd footballmatchessimulation
    ```
2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Run the Flask application:**
    ```bash
    python app.py
    ```
2.  **Open your browser** and navigate to `http://127.0.0.1:5000`.

## Technologies Used 

  * **Backend:** Python, Flask, Flask-Cors
  * **Frontend:** HTML, CSS, JavaScript, Bootstrap
  * **Data Processing:** pandas, scipy
  * **Data Fetching:** requests, beautifulsoup4, lxml

## Future Work 

  * Expand support to other major leagues around the world.
  * Incorporate more advanced prediction models.
  * Add more detailed team and player statistics.
  * Deploy the application to a cloud platform to make it publicly accessible to users worldwide.

