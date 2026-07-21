const selectedYear = document.getElementById('season-select');
const teamsContainer = document.getElementById('teams-container')

selectedYear.addEventListener('change', () => getTeams(selectedYear.value));

// Fetching API function
function getTeams(year){
    fetch(`/api/teams/${year}`)
    .then(response => response.json())
    .then(data => {
        let teamsAppend = '';
        if (data.teams_data.length === 0){
            console.log('No teams available');
        }        
        else{
            data.teams_data.forEach(team => {
                const coachesList = team.coaches && team.coaches.length > 0 ? team.coaches.join(', ') : 'No coaches yet';
                const studentCoachHTML = team.student_coaches.length > 0 
                    ? `<h6>Student coach: ${team.student_coaches.join(', ')}</h6>` 
                    : '';
                const captainsList = team.captain && team.captain.length > 0 ? team.captain.join(', '): "No captains yet";
                    teamsAppend += `
                        <div class="card team-item">
                            <img src="${team.image}" class="card-img-top team-photo" alt="${team.name} picture">
                            <div class="card-body">
                                <h5 class="card-title" style="font-weight: bold;">${team.name}</h5>
                                <h6 style="font-weight: 600;">Coach: ${coachesList}</h6>
                                ${studentCoachHTML}
                                <h6>Captain: ${captainsList}</h6>
                                <a href="/teams/${team.level}/${team.sport}/${selectedYear.value}" class="btn btn-primary btn-visit">View team</a>
                            </div>
                        </div>
                        `               
            })
        }
        teamsContainer.innerHTML = teamsAppend;
    }).catch(error => {
            console.log(error);
            console.log("Error loading team")
        })
}