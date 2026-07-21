// Inputs
const teamInput = document.getElementById('id_team');
const firstNameInput = document.getElementById('id_first_name');
const lastNameInput = document.getElementById('id_last_name');
const positionInput = document.getElementById('id_position');
const yearInput = document.getElementById('id_year');
const imageInput = document.getElementById('id_image');
const shirtNumberInput = document.getElementById('id_shirt_number');
const captainInput = document.getElementById('id_is_captain');
const quoteInput = document.getElementById('id_quote');

// Display values
const teamDisplay = document.getElementById('team-position');
const nameDisplay = document.getElementById('captain-name')
const yearDisplay = document.getElementById('year');
const quoteDisplay = document.querySelector('.quote');
const imageDisplay = document.getElementById('image-core');
const captainDisplay = document.querySelector('.captain-badge');
const numberDisplay = document.querySelector('.player-number')

firstNameInput.addEventListener('input', updateName);
lastNameInput.addEventListener('input', updateName);
teamInput.addEventListener('change', updateTeam);
positionInput.addEventListener('input', updateTeam);
quoteInput.addEventListener('input', updateQuote);
imageInput.addEventListener('change', updateImage);
captainInput.addEventListener('change', updateCaptain);
shirtNumberInput.addEventListener('input', updateShirtNumber);
yearInput.addEventListener('change', updateYear);


function updateShirtNumber(){
    numberDisplay.textContent = shirtNumberInput.value;
}


function updateCaptain(){
    captainDisplay.classList.toggle('hidden');
}


function updateName(){
    nameDisplay.textContent = firstNameInput.value + " " + lastNameInput.value;
}

function updateYear(){
    yearDisplay.textContent = 'Year: ' + yearInput.value;
}


function updateTeam(){
    if (teamInput.value){
        const selectedOption = teamInput.options[teamInput.selectedIndex];
        teamDisplay.textContent = selectedOption.textContent + " - " + positionInput.value;
    }
    else{
        teamDisplay.textContent = positionInput.value;
    }
}

function updateQuote(){
    quoteDisplay.innerText = '“' + quoteInput.value + '”';
}

function updateImage(){
    const reader = new FileReader();

    reader.onload = (e) => {
        const imageDataUrl = e.target.result;
        imageDisplay.src = imageDataUrl;
    }

    reader.readAsDataURL(imageInput.files[0]);
}