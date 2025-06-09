const map = L.map('map').setView([6.4975, 2.6036], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
    }).addTo(map);
    let marker;

    function geocode() {
    const query = document.getElementById('search').value;
    fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
        if (data.length > 0) {
            const lat = parseFloat(data[0].lat);
            const lon = parseFloat(data[0].lon);
            const name = data[0].display_name;

            map.setView([lat, lon], 13);
            if (marker) map.removeLayer(marker);
            marker = L.marker([lat, lon]).addTo(map).bindPopup(name).openPopup();

            // Envoie au backend Django
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
            alert("Rentrer un lieu");
        }
        });
    }

    function getCSRFToken() {
    let cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
    return cookie ? cookie.trim().split('=')[1] : '';
    }