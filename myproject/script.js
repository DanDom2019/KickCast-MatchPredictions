// --- Global State Management ---
let firstTeam = null;
let opponentTeam = null;
const API_BASE = 'http://127.0.0.1:5000'; // Flask server URL

// ==================================================================
//  Functions for Populating Dropdowns
// ==================================================================

function fetchLeagues(selectionType) {
    fetch('/foundationData/leagues.json')
        .then(response => response.json())
        .then(leagues => {
            const leagueListId = (selectionType === 'firstTeam') ? 'first-team-league-list' : 'opponent-league-list';
            const leagueList = document.getElementById(leagueListId);
            leagueList.innerHTML = '';

            leagues.forEach(league => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.className = 'dropdown-item';
                a.href = '#';
                a.textContent = league.Name;
                a.onclick = (event) => {
                    event.preventDefault();
                    leagueList.previousElementSibling.textContent = league.Name;
                    fetchTeamsByLeague(league.LeagueID, selectionType);
                };
                li.appendChild(a);
                leagueList.appendChild(li);
            });
        })
        .catch(error => console.error('Error fetching leagues:', error));
}

function fetchTeamsByLeague(leagueId, selectionType) {
    fetch('/foundationData/mainLeaguesTeams.json')
        .then(response => response.json())
        .then(allTeamsData => {
            const teams = allTeamsData[leagueId];
            if (!teams) {
                console.error(`No teams found for league ID: ${leagueId}`);
                return;
            }

            const teamListId = (selectionType === 'firstTeam') ? 'first-team-list' : 'opponent-team-list';
            const teamList = document.getElementById(teamListId);
            teamList.innerHTML = '';

            teams.forEach(team => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.className = 'dropdown-item';
                a.href = '#';
                a.textContent = team.Name;
                a.onclick = (event) => {
                    event.preventDefault();
                    if (selectionType === 'firstTeam') {
                        selectFirstTeam(team.TeamID, team.Name, leagueId);
                    } else {
                        selectOpponentTeam(team.TeamID, team.Name, leagueId);
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

function selectFirstTeam(teamId, teamName, leagueId) {
    console.log(`First team selected: ${teamName} (ID: ${teamId}, League: ${leagueId})`);
    firstTeam = { id: teamId, name: teamName, leagueId: leagueId };

    document.getElementById('first-team-dropdown-btn').textContent = teamName;
    apiCall(`/api/team/${teamId}`, 'first-team-info');
    displayLast10Matches(teamId, leagueId, 'last10');

    document.getElementById('step2-choose-opponent').classList.remove('d-none');
    document.getElementById('step3-simulation-result').classList.add('d-none');
    document.getElementById('opponent-team-info-wrapper').classList.add('d-none');
    document.getElementById('start-simulation-btn').classList.add('d-none');
}

function selectOpponentTeam(teamId, teamName, leagueId) {
    console.log(`Opponent team selected: ${teamName} (ID: ${teamId})`);
    opponentTeam = { id: teamId, name: teamName, leagueId: leagueId };
    
    document.getElementById('opponent-team-dropdown-btn').textContent = teamName;
    document.getElementById('opponent-team-info-wrapper').classList.remove('d-none');
    
    apiCall(`/api/team/${teamId}`, 'opponent-team-info');
    displayLast10Matches(teamId, leagueId, 'opponent-last10');

    // Show the simulation button
    document.getElementById('start-simulation-btn').classList.remove('d-none');
    document.getElementById('step3-simulation-result').classList.add('d-none');
}

async function simulateNextOfficialMatch() {
    if (!firstTeam) {
        alert("Please select a team first.");
        return;
    }
    const endpoint = `/api/team/${firstTeam.id}/next_match`;
    const resultDiv = document.getElementById('match-result-display');
    resultDiv.innerHTML = 'Finding next official match...';
    document.getElementById('step3-simulation-result').classList.remove('d-none');


    try {
        const response = await fetch(API_BASE + endpoint);
        const nextMatch = await response.json();

        if (response.ok) {
            document.getElementById('step3-simulation-result').classList.add('d-none');
            const opponent = nextMatch.awayTeam.id === firstTeam.id ? nextMatch.homeTeam : nextMatch.awayTeam;
            const opponentLeagueId = nextMatch.competition.id;
            selectOpponentTeam(opponent.id, opponent.name, opponentLeagueId);
        } else {
            resultDiv.innerHTML = '<h3>Error:</h3><pre>' + JSON.stringify(nextMatch, null, 2) + '</pre>';
        }
    } catch (error) {
        resultDiv.innerHTML = `<p class="text-danger">Network or Server Error: ${error.message}</p>`;
    }
}


// ==================================================================
// STEP 3: Display and Simulation Functions
// ==================================================================

function displayTeamInfo(teamData, elementId) {
    const container = document.getElementById(elementId);
    if (!teamData || !teamData.crest || !teamData.name || !teamData.venue || !teamData.area) {
        container.innerHTML = `<p class="text-danger">Could not display team info due to missing data.</p>`;
        return;
    }
    const teamCardHtml = `
        <div class="d-flex align-items-center">
            <img src="${teamData.crest}" alt="${teamData.name} logo" style="width: 75px; height: 75px; margin-right: 15px;">
            <div>
                <h4 class="mb-1">${teamData.name}
                <img src="${teamData.area.flag}" alt="${teamData.area.name} flag" style="width: 40px; height: auto; margin-left: 10px;">
                </h4>  
                <p class="mb-0 text-muted"><strong>Venue:</strong> ${teamData.venue}</p>
                <p class="mb-0 text-muted"><strong>Founded:</strong> ${teamData.founded || 'N/A'}</p>
            </div>
        </div>
    `;
    container.innerHTML = teamCardHtml;
}

function runSimulation() {
    if (!firstTeam || !opponentTeam) {
        alert("Error: Both teams must be selected for simulation.");
        return;
    }
    // Using the mock API endpoint for now
    const endpoint = `/app/prediction`; 
    document.getElementById('step3-simulation-result').classList.remove('d-none');
    apiCall(endpoint, 'match-result-display');
}

async function displayLast10Matches(teamId, leagueId, tableType) {
    const tableBody = document.getElementById(`${tableType}-table-body`);
    const loadingState = document.getElementById(`${tableType}-loading-state`);
    const endpoint = `/app/team/${teamId}/last10matches?leagueId=${leagueId}`;

    tableBody.innerHTML = '';
    loadingState.classList.remove('d-none');

    try {
        const response = await fetch(API_BASE + endpoint);
        const matches = await response.json();
        loadingState.classList.add('d-none');

        if (!response.ok || matches.error) {
            tableBody.innerHTML = `<tr><td colspan="5" class="text-center text-danger">Error: ${matches.error || 'Could not load match data.'}</td></tr>`;
            return;
        }

        const getResultBadge = (result) => {
            if (result === 'Win') return `<span class="badge bg-success">${result}</span>`;
            if (result === 'Loss') return `<span class="badge bg-danger">${result}</span>`;
            return `<span class="badge bg-warning text-dark">${result}</span>`;
        };

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
        tableBody.innerHTML = `<tr><td colspan="5" class="text-center text-danger">Network or Server Error: ${error.message}</td></tr>`;
    }
}


// ==================================================================
//  Utility Function for API Calls
// ==================================================================

async function apiCall(endpoint, resultId) {
    const resultDiv = document.getElementById(resultId);
    resultDiv.innerHTML = 'Loading...';
    try {
        const response = await fetch(API_BASE + endpoint);
        const data = await response.json();

        if (response.ok) {
            if (resultId.includes('-team-info')) {
                displayTeamInfo(data, resultId);
            } else {
                resultDiv.innerHTML = '<h3>Simulation Result:</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
            }
        } else {
            resultDiv.innerHTML = '<h3>Error:</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
        }
    } catch (error) {
        resultDiv.innerHTML = `<p class="text-danger">Network or Server Error: ${error.message}</p>`;
    }
}
