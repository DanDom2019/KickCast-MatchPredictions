// --- Global State Management ---
// These variables will store the user's choices.
let firstTeam = null;
let opponentTeam = null;
const API_BASE = 'http://127.0.0.1:5000'; // Your Flask server URL

// ==================================================================
//  Functions for Populating Dropdowns from Local JSON Files
// ==================================================================

/**
 * Fetches the list of leagues from your local JSON file.
 * @param {string} selectionType - 'firstTeam' or 'opponent'
 */
function fetchLeagues(selectionType) {
    console.log(`Fetching leagues for: ${selectionType}`);
    fetch('/foundationData/leagues.json')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(leagues => {
            const leagueListId = (selectionType === 'firstTeam') ? 'first-team-league-list' : 'opponent-league-list';
            const leagueList = document.getElementById(leagueListId);
            
            if (!leagueList) {
                console.error(`Error: Element with ID '${leagueListId}' not found.`);
                return;
            }
            leagueList.innerHTML = ''; // Clear previous items

            leagues.forEach(league => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.className = 'dropdown-item';
                a.href = '#';
                a.textContent = league.Name;
                a.onclick = (event) => {
                    event.preventDefault();
                    // Update the button text
                    const button = leagueList.previousElementSibling;
                    button.textContent = league.Name;
                    // Fetch the teams for the selected league
                    fetchTeamsByLeague(league.LeagueID, selectionType);
                };
                li.appendChild(a);
                leagueList.appendChild(li);
            });
        })
        .catch(error => console.error('Error fetching leagues:', error));
}

/**
 * Fetches teams for a specific league from your local JSON file.
 * @param {number} leagueId - The ID of the league to fetch teams for.
 * @param {string} selectionType - Determines which dropdown to populate ('firstTeam' or 'opponent').
 */
function fetchTeamsByLeague(leagueId, selectionType) {
    fetch('/foundationData/mainLeaguesTeams.json')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(allTeamsData => {
            const teams = allTeamsData[leagueId];
            if (!teams) {
                console.error(`No teams found for league ID: ${leagueId}`);
                return;
            }

            const teamListId = (selectionType === 'firstTeam') ? 'first-team-list' : 'opponent-team-list';
            const teamList = document.getElementById(teamListId);

            if (!teamList) {
                console.error(`Error: Element with ID '${teamListId}' not found.`);
                return;
            }
            teamList.innerHTML = ''; // Clear previous items

            teams.forEach(team => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.className = 'dropdown-item';
                a.href = '#';
                a.textContent = team.Name;
                a.onclick = (event) => {
                    event.preventDefault();
                    // Call the correct function based on the step
                    if (selectionType === 'firstTeam') {
                        selectFirstTeam(team.TeamID, team.Name);
                    } else {
                        selectOpponentTeam(team.TeamID, team.Name);
                    }
                };
                li.appendChild(a);
                teamList.appendChild(li);
            });
        })
        .catch(error => console.error('Error fetching teams:', error));
}


// ==================================================================
// STEP 2: Functions for Handling the User Workflow
// ==================================================================

/**
 * Called when the user selects their first team.
 */
function selectFirstTeam(teamId, teamName) {
    console.log(`First team selected: ${teamName} (ID: ${teamId})`);
    firstTeam = { id: teamId, name: teamName };

    // Update the button text
    document.getElementById('first-team-dropdown-btn').textContent = teamName;

    // Fetch and display the team's data in the info box 
    apiCall(`/api/team/${teamId}`, 'first-team-info');
    //fetch and display the last 10 matches for the selected team
    displayLast10Matches(teamId);
    // Show the next step
    document.getElementById('step2-choose-opponent').classList.remove('d-none');
    document.getElementById('step3-simulation-result').classList.add('d-none');
}

/**
 * Called when the user selects the opponent team.
 */
function selectOpponentTeam(teamId, teamName) {
    console.log(`Opponent team selected: ${teamName} (ID: ${teamId})`);
    opponentTeam = { id: teamId, name: teamName };

    // Update the button text
    document.getElementById('opponent-team-dropdown-btn').textContent = teamName;

    // Run the simulation now that both teams are selected
    runSimulation();
}

/**
 * Placeholder for the "Next Official Match" feature.
 */
function simulateNextOfficialMatch() {
    if (!firstTeam) {
        alert("Please select a team first.");
        return;
    }
    // For now, we'll use a hardcoded opponent for demonstration
    opponentTeam = { id: 66, name: "Manchester United FC" };
    console.log(`Simulating next official match against: ${opponentTeam.name}`);
    runSimulation();
}

/**
 * Calls the Python backend to get the final prediction.
 */
function runSimulation() {
    if (!firstTeam || !opponentTeam) {
        alert("Error: Both teams must be selected for simulation.");
        return;
    }

    const endpoint = `/simulation/predict?home=${firstTeam.id}&away=${opponentTeam.id}`;

    // Show the final result section and trigger the API call
    document.getElementById('step3-simulation-result').classList.remove('d-none');
    apiCall(endpoint, 'match-result-display');
}


// ==================================================================
// STEP 3: Utility Function for Making API Calls
// ==================================================================

/**
 * A helper function to fetch data from the backend and display it.
 * @param {string} endpoint - The API endpoint to call 
 * @param {string} resultId - The ID of the HTML element to display the result in.
 */
async function apiCall(endpoint, resultId) {
    const resultDiv = document.getElementById(resultId);
    resultDiv.innerHTML = 'Loading...';
    try {
        const response = await fetch(API_BASE + endpoint);
        const data = await response.json();

        if (response.ok) {
            resultDiv.innerHTML = '<h3>Simulation Result:</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
        } else {
            resultDiv.innerHTML = '<h3>Error:</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
        }
    } catch (error) {
        resultDiv.innerHTML = `<p class="text-danger">Network or Server Error: ${error.message}</p>`;
    }
}


// ==================================================================
//dynamic table section
/**
 * Fetches and displays the last 10 matches in a table.
 * @param {number} teamId - The ID of the team.
 */
async function displayLast10Matches(teamId) {
    const tableBody = document.getElementById('last10-table-body');
    const loadingState = document.getElementById('last10-loading-state');
    const endpoint = `/app/team/${teamId}/last10matches`;

    // Show loading indicator and clear previous results
    tableBody.innerHTML = '';
    loadingState.classList.remove('d-none');

    try {
        const response = await fetch(API_BASE + endpoint);
        const matches = await response.json();

        loadingState.classList.add('d-none'); // Hide loading indicator

        if (!response.ok || matches.error) {
            const errorHtml = `<tr><td colspan="5" class="text-center text-danger">Error: ${matches.error || 'Could not load match data.'}</td></tr>`;
            tableBody.innerHTML = errorHtml;
            return;
        }

        // Dynamically create a badge for the match result
        const getResultBadge = (result) => {
            if (result === 'Win') {
                return `<span class="badge bg-success">${result}</span>`;
            } else if (result === 'Loss') {
                return `<span class="badge bg-danger">${result}</span>`;
            } else {
                return `<span class="badge bg-warning text-dark">${result}</span>`;
            }
        };

        // Populate the table with match data
        matches.forEach(match => {
            const row = `
                <tr>
                    <td>${match.matchDay}</td>
                    <td>${match.date}</td>
                    <td>${match.opponent}</td>
                    <td>${match.score}</td>
                    <td>${getResultBadge(match.result)}</td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });

    } catch (error) {
        loadingState.classList.add('d-none');
        const errorHtml = `<tr><td colspan="5" class="text-center text-danger">Network or Server Error: ${error.message}</td></tr>`;
        tableBody.innerHTML = errorHtml;
    }
}

// ==================================================================
