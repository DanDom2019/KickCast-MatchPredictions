// Example data for demonstration
const leaguesByCountry = {
    england: [
        { id: 'epl', name: 'Premier League' },
        { id: 'championship', name: 'Championship' }
    ],
    spain: [
        { id: 'laliga', name: 'La Liga' },
        { id: 'segunda', name: 'Segunda División' }
    ],
    germany: [
        { id: 'bundesliga', name: 'Bundesliga' },
        { id: 'bundesliga2', name: '2. Bundesliga' }
    ]
};

const teamsByLeague = {
    epl: [
        { id: 'manutd', name: 'Manchester United' },
        { id: 'liverpool', name: 'Liverpool' }
    ],
    championship: [
        { id: 'leeds', name: 'Leeds United' }
    ],
    laliga: [
        { id: 'realmadrid', name: 'Real Madrid' },
        { id: 'barcelona', name: 'Barcelona' }
    ],
    bundesliga: [
        { id: 'bayern', name: 'Bayern Munich' }
    ]
};

function onCountryChange() {
    const country = document.getElementById('country-select').value;
    const leagueSelect = document.getElementById('league-select');
    const teamSelect = document.getElementById('team-select');
    leagueSelect.innerHTML = '<option value="">Select League</option>';
    teamSelect.innerHTML = '<option value="">Select Team</option>';
    teamSelect.disabled = true;

    if (country && leaguesByCountry[country]) {
        leaguesByCountry[country].forEach(league => {
            const opt = document.createElement('option');
            opt.value = league.id;
            opt.textContent = league.name;
            leagueSelect.appendChild(opt);
        });
        leagueSelect.disabled = false;
    } else {
        leagueSelect.disabled = true;
    }
}

function onLeagueChange() {
    const league = document.getElementById('league-select').value;
    const teamSelect = document.getElementById('team-select');
    teamSelect.innerHTML = '<option value="">Select Team</option>';

    if (league && teamsByLeague[league]) {
        teamsByLeague[league].forEach(team => {
            const opt = document.createElement('option');
            opt.value = team.id;
            opt.textContent = team.name;
            teamSelect.appendChild(opt);
        });
        teamSelect.disabled = false;
    } else {
        teamSelect.disabled = true;
    }
}
