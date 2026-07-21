// Inputs
const nameInput = document.getElementById('id_name');
const teamsInput = document.getElementById('id_teams');
const yearInput = document.getElementById('id_class_of');
const imageInput = document.getElementById('id_image');
const descriptionInput = document.getElementById('id_description');

// Display values
const nameDisplay = document.querySelector('.legend-name')
const teamsDisplay = document.querySelector('.legend-team');
const descriptionDisplay = document.querySelector('.legend-honors');
const imageDisplay = document.querySelector('.legend-pic');

nameInput.addEventListener('input', () => updateDisplay(nameDisplay, nameInput));
teamsInput.addEventListener('input', () => updateDisplay(teamsDisplay, teamsInput));
descriptionInput.addEventListener('input', updateDescription);
imageInput.addEventListener('change', updateImage);


function updateDisplay(displayE, inputE){
    displayE.textContent = inputE.value;
}

function updateDescription(){
    descriptionDisplay.textContent = `“${descriptionInput.value}”`;
}


function updateImage(){
    const reader = new FileReader();

    reader.onload = (e) => {
        const imageDataUrl = e.target.result;
        imageDisplay.src = imageDataUrl;
    }

    reader.readAsDataURL(imageInput.files[0]);
}