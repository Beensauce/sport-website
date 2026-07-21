const selectedYear = document.getElementById('season-select');
const legendsGrid = document.querySelector('.legends-grid')

selectedYear.addEventListener('change', () => getLegend(selectedYear.value));

function getLegend(class_of){
    fetch(`/api/legends/${class_of}`)
    .then(response => response.json())
    .then(data => {
        let legendsAppend = '';
        if (data.legends_data.length === 0){
            console.log('No legends available');
        }        
        else{
            data.legends_data.forEach(legend => {
                legendsAppend += `
                    <div class="legend-card">
                        <img src="${legend.image}" alt="${legend.name}" class="legend-pic"/>
                        <div class="legend-name">${legend.name}</div>
                        <div class="legend-team">${legend.teams}</div>
                        <div class="legend-honors">“${legend.description}”</div>
                    </div>
                `
            })
        }
        legendsGrid.innerHTML = legendsAppend;
    }).catch(error => {
            console.log(error);
            console.log("Error loading legends")
        })
}