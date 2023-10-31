document.addEventListener('DOMContentLoaded', function() {
    // Fetch live in-play events from the API
    fetch('/api/inplay-events')
    .then(response => response.json())
    .then(data => {
        const tableBody = document.getElementById('inplay-events');
        data.forEach(event => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${event.sport}</td>
                <td>${event.eventName}</td>
                <td>${event.homeTeam}</td>
                <td>${event.awayTeam}</td>
                <td>${event.currentScore}</td>
                <td>${event.timeElapsed}</td>
            `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error fetching in-play events:', error);
    });
});
