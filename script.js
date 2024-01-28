// Function to check if the user is within the geofence
function checkLocation() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function (position) {
            // User's current location
            const userLatitude = position.coords.latitude;
            const userLongitude = position.coords.longitude;

            // Define geofence coordinates
            const geofenceLatitude = 17.6045746; // Replace with the actual latitude
            const geofenceLongitude = 78.4859124; // Replace with the actual longitude

            // Define a radius for the geofence (e.g., 100 meters)
            const geofenceRadius = 50; // Replace with the desired radius

            // Calculate the distance between the user's location and the geofence center
            const distance = calculateDistance(userLatitude, userLongitude, geofenceLatitude, geofenceLongitude);

            // Create a message container
            const messageContainer = document.createElement('div');
            document.body.appendChild(messageContainer);

            // Check if the user is within the geofence
            if (distance <= geofenceRadius) {
                // User is within the allowed location
                messageContainer.innerHTML = '<h1>You have accessed the website. Click here to enter your email.</h1>';
                // Create a button
                const button = document.createElement('button');
                button.textContent = 'Click here';
                button.addEventListener('click', function () {
                    // Redirect to "example.html"
                    window.location.href = 'mailcheck.html';
                });
                messageContainer.appendChild(button);
            } else {
                // User is outside the allowed location, restrict access
                messageContainer.innerHTML = '<h1>Access is only allowed within the specified location.</h1>';
            }
        });
    } else {
        // Geolocation is not available in the browser, handle accordingly
        document.body.innerHTML = "<h1>Geolocation is not supported in your browser.</h1>";
    }
}

// Function to calculate the distance between two sets of coordinates (Haversine formula)
function calculateDistance(lat1, lon1, lat2, lon2) {
    const earthRadius = 6371; // Radius of the Earth in kilometers

    // Convert latitude and longitude from degrees to radians
    const lat1Rad = toRadians(lat1);
    const lon1Rad = toRadians(lon1);
    const lat2Rad = toRadians(lat2);
    const lon2Rad = toRadians(lon2);

    // Haversine formula
    const dlat = lat2Rad - lat1Rad;
    const dlon = lon2Rad - lon1Rad;

    const a = Math.sin(dlat / 2) * Math.sin(dlat / 2) +
        Math.cos(lat1Rad) * Math.cos(lat2Rad) *
        Math.sin(dlon / 2) * Math.sin(dlon / 2);

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    // Calculate the distance
    const distance = earthRadius * c;

    return distance;
}

function toRadians(degrees) {
    return degrees * (Math.PI / 180);
}

// Call the checkLocation function when the page loads
window.addEventListener("load", function() {
    // Add a click event listener to the button with id "checkLocationButton"
    const checkLocationButton = document.getElementById("checkLocationButton");
    if (checkLocationButton) {
        checkLocationButton.addEventListener("click", checkLocation);
    }
});
