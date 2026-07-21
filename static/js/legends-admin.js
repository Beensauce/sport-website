const selectedYear = document.getElementById('season-select');
const regLegends = document.getElementById('reg-legends')
const unregLegends = document.getElementById('unreg-legends')

selectedYear.addEventListener('change', () => getLegend(selectedYear.value));

function getLegend(class_of){
    fetch(`/legends-approval/get/${class_of}`)
    .then(response => response.json())
    .then(data => {
        let regLegendsAppend = '';
        let unregLegendsAppend = '';
        if (data.legends_data.length === 0){
            console.log('No legends available');
        }        
        else{
            data.legends_data.forEach(legend => {
                if (legend.is_correct){
                    regLegendsAppend += `
                    <tr>
                        <td>
                            <img src="${legend.image}" alt="${legend}" class="profile-pic-thumb"/>
                        </td>
                        
                        <!-- Name & Captain Badge Column -->
                        <td class="player-name">
                            ${legend.name}
                        </td>
                        
                        <!-- Details Columns -->
                        <td class="player-number">${legend.teams}</td>
                        <td>${legend.description}</td>
                        <td>${legend.class_of}</td>
                        

                        <td><input type="checkbox" name="legend_ids" value="${legend.id}"></td>
                    </tr>
                    `
                }
                else{
                    unregLegendsAppend += `
                    <tr>
                        <td>
                            <img src="${legend.image}" alt="${legend}" class="profile-pic-thumb"/>
                        </td>
                        
                        <!-- Name & Captain Badge Column -->
                        <td class="player-name">
                            ${legend.name}
                        </td>
                        
                        <!-- Details Columns -->
                        <td class="player-number">${legend.teams}</td>
                        <td>${legend.description}</td>
                        <td>${legend.class_of}</td>
                        

                        <td><input type="checkbox" name="legend_ids" value="${legend.id}"></td>
                    </tr>
                `
                }
            })
        }
        regLegends.innerHTML = regLegendsAppend;
        unregLegends.innerHTML = unregLegendsAppend;
    }).catch(error => {
            console.log(error);
            console.log("Error loading legends")
        })
}