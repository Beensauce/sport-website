document.addEventListener('DOMContentLoaded', holyFunction)

function holyFunction(){
    function showFewerGames(type){
        const games = document.querySelectorAll(type);
        games.forEach(game => game.classList.toggle('hidden'))
    }

    const resultButton = document.querySelector('button[data-action="results"]');
    const upcomingButton = document.querySelector('button[data-action="upcoming"]');
    let resultsLoaded = false;
    let upcomingLoaded = false;

    function loadMoreGames(type){
        if (type === 'results'){
            if (resultButton.textContent === 'Show more games' ){
                resultButton.textContent = 'Show fewer games';
                if (!resultsLoaded) {
                    const total = document.querySelectorAll('.result').length;
                    const result = document.querySelector('.results-container');
                    const headingElement = document.getElementById('head-text');
                    const teamLevel = headingElement.dataset.teamLevel;
                    const teamSport = headingElement.dataset.teamSport;
                    const teamYear = headingElement.dataset.teamYear;

                    fetch(`/api/more-games/${teamLevel}/${teamSport}/${teamYear}/${total}`).then(response => response.json()).then(data => {
                        if (data.games.length === 0){
                                console.log("No more games available")
                            }
                            else{
                                data.games.forEach(game => {
                                    const gameDiv = document.createElement('div');
                                    let winner = '';
                                    if (game.dcb_score > game.opp_score){
                                        winner = '<div class="winner-indicator" style="background-color: green !important;">W</div>';
                                    }
                                    else if (game.dcb_score == game.opp_score){
                                        winner = '<div class="winner-indicator" style="background-color: grey !important;">D</div>';
                                    }
                                    else{
                                        winner = '<div class="winner-indicator">L</div>';
                                    }
                                    gameDiv.classList.add('result-card', 'result', 'new-result');

                                    gameDiv.innerHTML = `
                                        <div>
                                            <div class="sport-tag">${game.dcb_team}</div>
                                        </div>
                                        ${winner}
                                        <div class="team-name">vs ${game.opposition}</div>
                                        <div class="date-location">
                                            <div>${game.date}</div>
                                            <div>${game.time}</div>
                                            <div>${game.location}</div>
                                        </div>
                                        <div class="score-container">
                                            <div class="score-team">
                                                <h4>DCB</h4>
                                                <span>${game.dcb_score}</span>
                                            </div>
                                            <div class="vs-separator">-</div>
                                            <div class="score-team">
                                                <h4>${game.opposition}</h4>
                                                <span>${game.opp_score}</span>
                                            </div>
                                        </div>
                                    `;
                                    result.appendChild(gameDiv);
                                })
                                resultsLoaded = true;
                            }
                                
                    }).catch(error => {
                            console.log(error);
                            console.log("Error loading game")
                        })
                }
                else{
                    resultButton.textContent = 'Show fewer games';
                    showFewerGames('.new-result');
                }
            }
            else{
                resultButton.textContent = 'Show more games';
                showFewerGames('.new-result');
            }
        }


        else{
            if (upcomingButton.textContent === 'Show more games' ){
                upcomingButton.textContent = 'Show fewer games';
                if (!upcomingLoaded){
                    const total = document.querySelectorAll('.upcoming-count').length;
                    const upcomingContainer = document.querySelector('.upcoming-container');
                    const headingElement = document.getElementById('head-text');
                    const teamLevel = headingElement.dataset.teamLevel;
                    const teamSport = headingElement.dataset.teamSport;
                    const teamYear = headingElement.dataset.teamYear;
                    fetch(`/api/more-upcomings/${teamLevel}/${teamSport}/${teamYear}/${total}`).then(response => response.json()).then(data =>{
                            if (data.games.length === 0){
                                console.log("No more games available")
                            }
                            else{
                                data.games.forEach(upcoming => {
                                    const upcomingDiv = document.createElement('div');
                                    upcomingDiv.classList.add('result-card', 'upcoming', 'upcoming-count', 'new-upcoming');

                                    upcomingDiv.innerHTML =    `
                                            <div class="sport-tag">${upcoming.dcb_team}</div>
                                                <div class="team-name">vs ${upcoming.opposition}</div>
                                                <div class="date-location">
                                                    <div>${upcoming.date}</div>
                                                    <div>${upcoming.time}</div>
                                                    <div>${upcoming.location}</div>
                                                </div>
                                            `;
                                    upcomingContainer.appendChild(upcomingDiv);
                            })
                            upcomingLoaded = true;
                        } 
                        }).catch(error => {
                            console.log(error);
                            console.log("Error loading game")
                        })
                }
                else{
                    upcomingButton.textContent = 'Show fewer games';
                    showFewerGames('.new-upcoming');
                }
            }
            else{            
                upcomingButton.textContent = 'Show more games';
                showFewerGames('.new-upcoming');
            }

        }
    }

    // Check if results button exists before adding event listener
    if (resultButton) {
        resultButton.addEventListener('click', () => loadMoreGames('results'));
    }

    // Check if upcoming button exists before adding event listener
    if (upcomingButton) {
        upcomingButton.addEventListener('click', () => loadMoreGames('upcoming'));
    }
}
