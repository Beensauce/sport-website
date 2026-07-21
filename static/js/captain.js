const editTeamModel = document.querySelector('.edit-team-model'); 
const editGameModel = document.querySelector('.edit-game-model');
const addGameModel = document.querySelector('.add-game-model');
const addCoachModel = document.querySelector('.add-coach-model');

const backdrop = document.getElementById('modal-backdrop'); // Select the overlay
const closeBtns = document.querySelectorAll('.close-btn');
const editBtns = document.querySelectorAll('.edit-game-btn')
const editTeamBtn = document.getElementById('edit-team');
const addGameBtn = document.getElementById('add-game');
const addCoachBtn = document.getElementById('add-coach');

// Inputs
const inputOpposition = document.getElementById('editOpposition');
const inputDcbScore = document.getElementById('editDcbScore');
const inputOppScore = document.getElementById('editOppScore');
const inputDate = document.getElementById('editDate');
const inputTime = document.getElementById('editTime');
const inputLocation = document.getElementById('editLocation');
const inputIsFinished = document.getElementById('editIsFinished');

editTeamBtn.addEventListener('click', () => toggleHidden(editTeamModel));
addGameBtn.addEventListener('click', () => toggleHidden(addGameModel));
addCoachBtn.addEventListener('click', () => toggleHidden(addCoachModel));

// For results section
const resultsContainer = document.querySelector('.results-container');
resultsContainer.addEventListener('click', (e) => {
    const editBtn = e.target.closest('.edit-game-btn');
    if (editBtn) {
        e.stopPropagation();
        toggleHidden(editGameModel);
        instanceData(editBtn);
    }
});

// Edit coach sections
const coachesContainer = document.querySelector('.coach-table');
coachesContainer.addEventListener('click', (e) => {
    const editBtn = e.target.cloest('.edit-coach');
    if (editBtn){
        e.stopPropagation();
        toggleHidden()
    }
})


// For upcoming games section
const upcomingContainer = document.querySelector('.upcoming-container');
upcomingContainer.addEventListener('click', (e) => {
    const editBtn = e.target.closest('.edit-game-btn');
    if (editBtn) {
        e.stopPropagation();
        toggleHidden(editGameModel);
        instanceData(editBtn);
    }
});

closeBtns.forEach((btn) => btn.addEventListener('click', closeAllModals));
backdrop.addEventListener('click', closeAllModals);


function closeAllModals() {
    const allModals = document.querySelectorAll('.model, .edit-game');
    
    allModals.forEach(modal => {
        modal.classList.add('hidden');
    });
    
    backdrop.classList.add('hidden')
}

function toggleHidden(element){
    backdrop.classList.toggle('hidden');
    element.classList.toggle('hidden');
}

function instanceData(editBtn){
    const id = editBtn.dataset.id;
    const game = document.querySelector(`[data-id="${id}"]`)

    document.getElementById('editGameId').value = id;
    inputOpposition.value = game.dataset.opposition;
    inputDcbScore.value = game.dataset.dcbScore;
    inputOppScore.value = game.dataset.oppScore;
    inputDate.value = game.dataset.date;
    inputTime.value = game.dataset.time;
    inputLocation.value = game.dataset.location;
    inputIsFinished.checked = JSON.parse(game.dataset.isFinished.toLowerCase());

    editGameModel.dataset.id = id;
}

// Getting more games and deleting stuff
function submitDelete(gameId, year) {
    if (confirm(`Are you sure you want to delete this game?`)) {
        const form = document.getElementById('globalDeleteForm');
        form.action = `/game/${gameId}/delete/${year}`; 
        
        form.submit(); 
    }
}


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

                                // Add data attributes using dataset                      
                                gameDiv.dataset.id = game.id;
                                gameDiv.dataset.opposition = game.opposition;
                                gameDiv.dataset.dcbScore = game.dcb_score; 
                                gameDiv.dataset.oppScore = game.opp_score;
                                gameDiv.dataset.date = game.raw_date;
                                gameDiv.dataset.time = game.raw_time;
                                gameDiv.dataset.location = game.location;
                                gameDiv.dataset.isFinished = game.is_finished;
                                gameDiv.innerHTML = `
                                    <div>
                                        <div class="sport-tag">${game.dcb_team}</div>
                                    </div>
                                    <button class="edit-game-btn" data-id="${game.id}">Edit</button>
                                    <button type="button" class="delete-game-btn" 
                                            onclick="submitDelete('${game.id}')">
                                        Delete
                                    </button>
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
                                upcomingDiv.dataset.id = upcoming.id;
                                upcomingDiv.dataset.opposition = upcoming.opposition;
                                upcomingDiv.dataset.dcbScore = upcoming.dcb_score; 
                                upcomingDiv.dataset.oppScore = upcoming.opp_score;
                                upcomingDiv.dataset.date = upcoming.raw_date;
                                upcomingDiv.dataset.time = upcoming.raw_time;
                                upcomingDiv.dataset.location = upcoming.location;
                                upcomingDiv.dataset.isFinished = upcoming.is_finished;

                                upcomingDiv.innerHTML =    `
                                        <div class="sport-tag">${upcoming.dcb_team}</div>
                                            <button class="edit-game-btn" data-id="${upcoming.id}">Edit</button>
                                            <button type="button" class="delete-game-btn" 
                                                    onclick="submitDelete('${upcoming.id}')">
                                                Delete
                                            </button>
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
resultButton.addEventListener('click', () => loadMoreGames('results'));
upcomingButton.addEventListener('click', () => loadMoreGames('upcoming'))

// Validation for games, DCB score etc
const editGameForm = document.getElementById('edit-game-form');
editGameForm.addEventListener('submit', (e) => {
    const isFinished = document.getElementById('editIsFinished').checked;
    const dcbScore = document.getElementById('editDcbScore').value;
    const oppScore = document.getElementById('editOppScore').value;
    
    if (isFinished) {
        if (!dcbScore || !oppScore) {
            e.preventDefault();
            alert('Both scores are required for finished games!');
        }
    }
})

const addGameForm = document.getElementById('add-game-form');
addGameForm.addEventListener('submit', (e) => {
    const isFinished = document.getElementById('id_is_finished').checked;
    const dcbScore = document.getElementById('id_opp_score').value;
    const oppScore = document.getElementById('id_dcb_score').value;

    if (isFinished) {
        if (!dcbScore || !oppScore) {
            e.preventDefault();
            alert('Both scores are required for finished games!');
        }
    }
})