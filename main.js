var map = L.map('map').setView([48.2071889, 16.4205083], 5);
var data;  // Declare data variable

L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

var markers = [];  // Array to store markers

 // Add a single click event listener to the body using event delegation
 document.body.addEventListener('click', (event) => {
    const clickedElement = event.target;

    // Check if the clicked element is an opponent name
    if (clickedElement.classList.contains('opponent-name')) {
        const opponentId = clickedElement.dataset.clubid;
        // Update selectedClub and fetch data for the new club
        onClubSelect(opponentId);
    }
});

// Fetch clubs from the API
fetch('http://localhost:5000/clubs')
    .then(response => response.json())
    .then(apiData => {
        data = apiData;  // Assign apiData to the data variable
        const clubSelect = document.getElementById('club-select');
        data.clubs.forEach(club => {
            const option = document.createElement('option');
            option.value = club.id;
            option.textContent = club.name;
            clubSelect.appendChild(option);
        });
    })
    .catch(error => console.error('Error fetching clubs:', error));

function onClubSelect(clubId) {
    // Remove existing markers
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];
    console.log('Selected club:', clubId);
    // Get geolocation for the selected club
    const selectedClub = data.clubs.find(club => club.id === clubId);

    if (selectedClub) {
        const { lat, long } = selectedClub.geolocation;

        // Create a red marker for the selected club
        const selectedMarker = L.marker([parseFloat(lat), parseFloat(long)], { icon: L.divIcon({ className: 'custom-marker', html: '&#x1F534;' }) }).addTo(map);
        markers.push(selectedMarker);

        // Update the club information section
        const clubInfoSection = document.getElementById('club-info');
        clubInfoSection.innerHTML = `
            <div style="display: flex; flex-direction: column; align-items: center; padding: 10px; padding-top: 30px; width: 300px;">
                <img src="${selectedClub.logo}" style="max-width: 150px; max-height: 150px;">
                <br>
                <h2 style="text-align: center;">${selectedClub.name}</h2>
                <p style="text-align: center">
                    <b>Country:</b> ${selectedClub.country} <br>
                    <b>City:</b> ${selectedClub.city}<br>
                    <b>Stadium:</b> ${selectedClub.stadium}<br>
                    <b>Capacity:</b> ${selectedClub.capacity}
                </p>
                <p style="text-align: center">
                    <b>Champions League:</b> (${selectedClub.competitions["UEFA Champions League"].length}) ${selectedClub.competitions["UEFA Champions League"].join(', ')}<br>
                    <b>Europa League:</b> (${selectedClub.competitions["UEFA Europa League"].length}) ${selectedClub.competitions["UEFA Europa League"].join(', ')}<br>
                    <b>Europa Conference League:</b> (${selectedClub.competitions["UEFA Europa Conference League"].length}) ${selectedClub.competitions["UEFA Europa Conference League"].join(', ')}
                </p>
            </div>
        `;

        // Make a request to /matches/<string:name>
        fetch(`http://localhost:5000/matches/${clubId}`)
            .then(response => response.json())
            .then(matchesData => {
                // Create a map to store matches by opponent team
                const matchesByOpponent = new Map();

                // Group matches by opponent team
                matchesData.matches.forEach(match => {
                    const { date, away_team_name, away_team_id, away_team_score, home_team_name, home_team_id, home_team_score, winner, results } = match;
                    // Determine the opponent team
                    const opponentTeam = (home_team_id === clubId) ? away_team_id : home_team_id;

                    // Initialize the matches array for the opponent
                    matchesByOpponent.set(opponentTeam, matchesByOpponent.get(opponentTeam) || []);

                    // Add the match details to the opponent's matches array
                    matchesByOpponent.get(opponentTeam).push({
                        date,
                        home_team_name,
                        away_team_name,
                        home_team_id,
                        away_team_id,
                        home_team_score,
                        away_team_score,
                        winner,
                        results
                    });
                });

                // Display popups for each opponent with sorted matches
                for (const [opponent, matches] of matchesByOpponent.entries()) {
                    const opponentData = data.clubs.find(club => club.id === opponent);
                
                    if (opponentData) {  // Check if opponentData is defined
                        const { lat, long } = opponentData.geolocation;
                        if (lat == null || long == null) {
                            console.error(`Geolocation not found for ${opponentData.name} skip`);
                            continue;
                        }
                        // Sort matches by date in ascending order
                        matches.sort((a, b) => new Date(a.date) - new Date(b.date));

                        // Create a popup with all matches against the opponent
                        const popupContent = `<div style="display: flex; flex-direction: column;">
                                                <div style="display: flex; align-items: center;">
                                                    <img src="${opponentData.logo}" alt="${opponent}" style="max-width: 50px; max-height: 50px; margin-right: 10px;">
                                                    <h2 class="opponent-name" data-clubid="${opponent}">${opponentData.name}</h2>
                                                </div>
                                                <div style="display: flex; justify-content: center; font-size: 12px; margin-bottom: 10px; font-weight: bold;">
                                                    <span style="color: green; margin-right: 8px;">W${matches[0].results.win}</span>-
                                                    <span style="color: orange; margin-right: 8px; margin-left: 8px;"> D${matches[0].results.draw}</span>-
                                                    <span style="color: red; margin-left: 8px;">L${matches[0].results.loss}</span>
                                                </div>
                                            </div>${matches.map(match => {
                            const formattedDate = new Date(match.date).toLocaleDateString();
                            if (match.winner.toLowerCase() === 'draw') {
                                return `${formattedDate} - ${match.home_team_name} ${match.home_team_score}-${match.away_team_score} ${match.away_team_name}`;
                            }
                            const result = (match.winner === match.home_team_id) ?
                                `<b>${match.home_team_name}</b> ${match.home_team_score}-${match.away_team_score} ${match.away_team_name}` :
                                `${match.home_team_name} ${match.home_team_score}-${match.away_team_score} <b>${match.away_team_name}</b>`;
                            return `${formattedDate} - ${result}`;
                        }).join('<br>')}`;
                
                        const opponentMarker = L.marker([parseFloat(lat), parseFloat(long)]).addTo(map).bindPopup(popupContent);
                        markers.push(opponentMarker);
                    } else {
                        console.error(`Opponent data not found for ${opponent}`);
                    }
                }
            })
            .catch(error => console.error(`Error fetching matches for ${selectedClub}:`, error));
    } else {
        console.error(`Geolocation not found for ${JSON.stringify(selectedClub)}`);
    }
}
