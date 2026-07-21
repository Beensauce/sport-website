document.addEventListener('DOMContentLoaded', () => {
    const seasonSelect = document.getElementById('season-select');
    const text = document.getElementById('not-available');
    checkTeams();
    filterTeamBySeason(seasonSelect.value)

    seasonSelect.addEventListener('change', () => {
    checkTeams();
    filterTeamBySeason(seasonSelect.value)
});

    function filterTeamBySeason(selectedSeason){    
        const teamItems = document.querySelectorAll('.team-item');
        
        teamItems.forEach((teamItem) => {
            const teamSeason = teamItem.dataset.season;
            const selectedSeason = seasonSelect.value;
            if (selectedSeason === teamSeason) {
                teamItem.classList.remove('hidden');
            } else {
                teamItem.classList.add('hidden');
            }
        });
    }           

    function checkTeams(){
        const selectedSeason = seasonSelect.value;
        const teamsForSeason = document.querySelectorAll(`[data-season="${seasonSelect.value}"]`);
        const hasTeams = teamsForSeason.length > 0;
        if (hasTeams) {
            text.classList.add('hidden');
            filterTeamBySeason(selectedSeason);
        } else {
            text.classList.remove('hidden');
            filterTeamBySeason(selectedSeason);
        }
    }
});

