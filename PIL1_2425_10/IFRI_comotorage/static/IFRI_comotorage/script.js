const map = L.map('map').setView([6.4975, 2.6036], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
}).addTo(map);
let marker;

function geocode() {
    const query = document.getElementById('search').value;
    const searchResultsContainer = document.getElementById('searchResults');
    searchResultsContainer.innerHTML = ''; // Clear previous results

    fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
            if (data.length > 0) {
                data.forEach(result => {
                    const lat = parseFloat(result.lat);
                    const lon = parseFloat(result.lon);
                    const name = result.display_name;

                    // Create a div for each result and append to searchResultsContainer
                    const resultDiv = document.createElement('div');
                    resultDiv.classList.add('search-result-item'); // Add a class for styling
                    resultDiv.innerHTML = `
                        <h4>${name}</h4>
                        <p>Latitude: ${lat}, Longitude: ${lon}</p>
                    `;
                    resultDiv.onclick = () => {
                        // When a result is clicked, update the map marker and view
                        map.setView([lat, lon], 13);
                        if (marker) map.removeLayer(marker);
                        marker = L.marker([lat, lon]).addTo(map).bindPopup(name).openPopup();
                        // You might want to clear the search results after clicking one
                        searchResultsContainer.innerHTML = ''; 
                        document.getElementById('search').value = name; // Populate search bar with selected location
                    };
                    searchResultsContainer.appendChild(resultDiv);
                });

                // Optionally, if you want to automatically set the first result as the map marker
                const firstResult = data[0];
                const lat = parseFloat(firstResult.lat);
                const lon = parseFloat(firstResult.lon);
                const name = firstResult.display_name;
                
                map.setView([lat, lon], 13);
                if (marker) map.removeLayer(marker);
                marker = L.marker([lat, lon]).addTo(map).bindPopup(name).openPopup();


                // Envoie au backend Django (this part remains the same)
                fetch('/save_location/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ name: name, lat: lat, lon: lon })
                }).then(res => res.json()).then(data => {
                    console.log("Localisation enregistrée :", data);
                });

            } else {
                searchResultsContainer.innerHTML = '<p>Aucun lieu trouvé.</p>';
                alert("Rentrer un lieu");
            }
        });
}

function getCSRFToken() {
    let cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
    return cookie ? cookie.trim().split('=')[1] : '';
}