// --- Global State Management ---
let firstTeam = null;
let opponentTeam = null;
let nextMatchDetails = null; 
let predictionChart = null; 
const API_BASE = 'http://127.0.0.1:5000';

// ==================================================================
//  Functions for Populating Dropdowns
// ==================================================================

function fetchLeagues(selectionType) {
    fetch('/static/foundationData/leagues.json')
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
    fetch('/static/foundationData/mainLeaguesTeams.json')
        .then(response => response.json())
        .then(allTeamsData => {
            const teams = allTeamsData[leagueId];
            if (!teams) return;

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
                        nextMatchDetails = null;
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
// User Workflow Functions
// ==================================================================

function selectFirstTeam(teamId, teamName, leagueId) {
    firstTeam = { id: teamId, name: teamName, leagueId: leagueId };
    document.getElementById('first-team-dropdown-btn').textContent = teamName;
    
    // **CORRECTED ANIMATION LOGIC**
    // 1. Animate the main container upwards
    document.getElementById('main-container').classList.add('content-moved-up');
    
    // 2. Show the details container that holds the team info
    document.getElementById('first-team-details-container').classList.remove('d-none');
    
    // 3. Populate the details
    apiCall(`/api/team/${teamId}`, 'first-team-info', displayTeamInfo);
    displayLast10Matches(teamId, leagueId, 'last10');

    // 4. Show the opponent selection step
    document.getElementById('step2-container').classList.remove('d-none');

    // 5. Hide other sections until needed
    document.getElementById('opponent-team-info-wrapper').classList.add('d-none');
    document.getElementById('step3-simulation-result').classList.add('d-none');
}

function selectOpponentTeam(teamId, teamName, leagueId) {
    opponentTeam = { id: teamId, name: teamName, leagueId: leagueId };
    
    document.getElementById('opponent-team-dropdown-btn').textContent = teamName;
    document.getElementById('opponent-team-info-wrapper').classList.remove('d-none');
    
    apiCall(`/api/team/${teamId}`, 'opponent-team-info', displayTeamInfo);
    displayLast10Matches(teamId, leagueId, 'opponent-last10');

    displayMatchDetails();

    document.getElementById('start-simulation-btn').classList.remove('d-none');
    document.getElementById('step3-simulation-result').classList.add('d-none');
}

async function simulateNextOfficialMatch() {
    if (!firstTeam) {
        alert("Please select a team first.");
        return;
    }
    const endpoint = `/api/team/${firstTeam.id}/next_match`;
    
    try {
        const response = await fetch(API_BASE + endpoint);
        const matchData = await response.json();

        if (response.ok) {
            nextMatchDetails = matchData;
            const opponent = matchData.awayTeam.id === firstTeam.id ? matchData.homeTeam : matchData.awayTeam;
            const opponentLeagueId = matchData.competition.id;
            selectOpponentTeam(opponent.id, opponent.name, opponentLeagueId);
        } else {
            alert(`Error finding next match: ${matchData.error}`);
        }
    } catch (error) {
        alert(`Network Error: ${error.message}`);
    }
}


// ==================================================================
// Display and Simulation Functions
// ==================================================================

function displayTeamInfo(teamData, elementId) {
    const container = document.getElementById(elementId);
    if (!teamData || !teamData.crest || !teamData.name || !teamData.venue || !teamData.area) {
        container.innerHTML = `<p class="text-danger">Could not display team info.</p>`;
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

function displayMatchDetails() {
    const detailsWrapper = document.getElementById('match-details-wrapper');
    const detailsContent = document.getElementById('match-details-content');

    if (nextMatchDetails) {
        const matchDate = new Date(nextMatchDetails.utcDate);
        const formattedDate = matchDate.toLocaleString();

        detailsContent.innerHTML = `
            <p class="mb-1"><strong>Date & Time:</strong> ${formattedDate}</p>
            <p class="mb-0"><strong>Venue:</strong> ${nextMatchDetails.venue}</p>
        `;
        detailsWrapper.classList.remove('d-none');
    } else {
        detailsWrapper.classList.add('d-none');
    }
}

function runSimulation() {
    if (!firstTeam || !opponentTeam) {
        alert("Error: Both teams must be selected.");
        return;
    }
    const endpoint = `/simulation/predict?home=${firstTeam.id}&away=${opponentTeam.id}&leagueId=${firstTeam.leagueId}`;
    document.getElementById('step3-simulation-result').classList.remove('d-none');
    apiCall(endpoint, 'match-result-display', displayPredictionResult);
}

function displayPredictionResult(data, elementId) {
    const container = document.getElementById(elementId);
    if (!data || data.error) {
        container.innerHTML = `<p class="text-danger">Failed to get a valid simulation result: ${data.error || 'Unknown error'}</p>`;
        return;
    }

    let topScoresHtml = '';
    data.top_five_scores.forEach(item => {
        topScoresHtml += `
            <li class="list-group-item d-flex justify-content-between align-items-center">
                Score: <strong>${item.score}</strong>
                <span class="badge bg-info rounded-pill">${item.probability}%</span>
            </li>
        `;
    });

    container.innerHTML = `
        <div class="row align-items-center">
            <div class="col-md-5 text-center">
                <h5>${firstTeam.name}</h5>
                <h1 class="display-4">${data.home_team_win_probability}%</h1>
                <p class="text-muted">Win Probability</p>
            </div>
            <div class="col-md-2 text-center">
                <h5 class="text-muted">Draw</h5>
                <h1 class="display-4">${data.draw_probability}%</h1>
            </div>
            <div class="col-md-5 text-center">
                <h5>${opponentTeam.name}</h5>
                <h1 class="display-4">${data.away_team_win_probability}%</h1>
                <p class="text-muted">Win Probability</p>
            </div>
        </div>
        <hr>
        <div class="row mt-3">
            <div class="col-md-7">
                <h5>Outcome Probabilities</h5>
                <canvas id="predictionChart"></canvas>
            </div>
            <div class="col-md-5">
                <h5>Top 5 Scorelines</h5>
                <ul class="list-group mb-3"> ${topScoresHtml} </ul>
                <h5>Predicted Goals</h5>
                <ul class="list-group">
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        ${firstTeam.name}:
                        <span class="badge bg-primary rounded-pill">${data.predicted_goals_home}</span>
                    </li>
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        ${opponentTeam.name}:
                        <span class="badge bg-primary rounded-pill">${data.predicted_goals_away}</span>
                    </li>
                </ul>
            </div>
        </div>
    `;
    
    const ctx = document.getElementById('predictionChart').getContext('2d');
    if (predictionChart) {
        predictionChart.destroy();
    }
    predictionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: [`${firstTeam.name} Win`, 'Draw', `${opponentTeam.name} Win`],
            datasets: [{
                label: 'Match Outcome Probability',
                data: [data.home_team_win_probability, data.draw_probability, data.away_team_win_probability],
                backgroundColor: ['rgba(75, 192, 192, 0.7)', 'rgba(255, 206, 86, 0.7)', 'rgba(255, 99, 132, 0.7)'],
                borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 206, 86, 1)', 'rgba(255, 99, 132, 1)'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: { color: '#e0e0e0' }
                },
                title: {
                    display: true,
                    text: 'Match Outcome Prediction',
                    color: '#e0e0e0'
                }
            }
        }
    });
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
            tableBody.innerHTML = `<tr><td colspan="5" class="text-center text-danger">${matches.error || 'Could not load match data.'}</td></tr>`;
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
        tableBody.innerHTML = `<tr><td colspan="5" class="text-center text-danger">Network Error: ${error.message}</td></tr>`;
    }
}


// ==================================================================
//  Utility Function for API Calls
// ==================================================================

async function apiCall(endpoint, resultId, displayFunction) {
    const resultDiv = document.getElementById(resultId);
    resultDiv.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';
    try {
        const response = await fetch(API_BASE + endpoint);
        const data = await response.json();

        if (response.ok) {
            if (displayFunction) {
                displayFunction(data, resultId);
            } else {
                 resultDiv.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            }
        } else {
            resultDiv.innerHTML = '<h3>Error:</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
        }
    } catch (error) {
        resultDiv.innerHTML = `<p class="text-danger">Network or Server Error: ${error.message}</p>`;
    }
}