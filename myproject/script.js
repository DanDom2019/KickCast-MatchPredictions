const API_BASE = 'http://127.0.0.1:5000';

        // Utility function to make API calls
        async function apiCall(endpoint, resultId) {
            const resultDiv = document.getElementById(resultId);
            resultDiv.innerHTML = 'Loading...';
            
            try {
                const response = await fetch(API_BASE + endpoint);
                const data = await response.json();
                
                if (response.ok) {
                    resultDiv.innerHTML = '<h3>✅ Success</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } else {
                    resultDiv.innerHTML = '<h3>❌ Error</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                }
            } catch (error) {
                resultDiv.innerHTML = '<h3>❌ Network Error</h3><p>' + error.message + '</p>';
            }
        }

        // Match functions
        function fetchMatchData() {
            apiCall('/mock-api/match', 'match-result');
        }

        function fetchPredictions() {
            apiCall('/mock-api/prediction', 'match-result');
        }

        function fetchHeadToHead() {
            apiCall('/mock-api/head-to-head', 'match-result');
        }

        // Team functions
        function fetchTeamData() {
            const teamType = document.getElementById('team-select').value;
            apiCall('/mock-api/team/' + teamType, 'team-result');
        }

        function fetchTeamForm() {
            const teamType = document.getElementById('team-select').value;
            apiCall('/mock-api/form/' + teamType, 'team-result');
        }

        // Custom endpoint
        function testEndpoint() {
            const endpoint = document.getElementById('custom-endpoint').value;
            apiCall(endpoint, 'custom-result');
        }

        function clearAll() {
            document.getElementById('match-result').innerHTML = '';
            document.getElementById('team-result').innerHTML = '';
            document.getElementById('custom-result').innerHTML = '';
        }

        function fetchLeagues() {
            console.log('Fetching leagues...');
            fetch('foundationData/leagues.json')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(leagues => {
                    const leagueSelect = document.getElementById('league-select');
                    leagueSelect.innerHTML = ''; // Clear previous items
                    leagues.forEach(league => {
                        const li = document.createElement('li');
                        const a = document.createElement('a');
                        a.className = 'dropdown-item';
                        a.href = '#';
                        a.textContent = league.Name;
                        a.dataset.leagueId = league.LeagueID;
                        a.onclick = function() {
                            selectLeague(league.LeagueID, league.Name);
                            return false; // Prevent default action
                        };
                        li.appendChild(a);
                        leagueSelect.appendChild(li);
                    });
                })
                .catch(error => {
                    const leagueSelect = document.getElementById('league-select');
                    leagueSelect.innerHTML = `<option value="">Error loading leagues</option>`;
                    leagueSelect.classList.add('is-invalid'); // Bootstrap error style
                    console.error(error);
                });
        }
        
        function selectLeague(leagueId, leagueName) {
            console.log(`Selected league: ${leagueName} (ID: ${leagueId})`);
            
            // Update the dropdown button text to show the selected league
            const dropdownButton = document.querySelector('.dropdown-toggle');
            if (dropdownButton) {
                dropdownButton.textContent = leagueName;
            }
            
            // Store the selected league ID for later use
            document.querySelector('.teamSelectDropdown').dataset.selectedLeagueId = leagueId;
            
            // You can add more functionality here, like:
            // 1. Fetch teams for this league
            // 2. Update other parts of your UI
            // 3. Trigger other actions
            
            // Example: fetchTeamsForLeague(leagueId);
        }