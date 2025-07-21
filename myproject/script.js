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