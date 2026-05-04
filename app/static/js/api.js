const API_BASE = '/api';

window.api = {
    async fetchDestinations(lang = 'en') {
        const response = await fetch(`${API_BASE}/destinations?lang=${lang}`);
        return response.json();
    },

    async fetchDestination(id, lang = 'en') {
        const response = await fetch(`${API_BASE}/destinations/${id}?lang=${lang}`);
        return response.json();
    },

    async fetchServices(destinationId, lang = 'en') {
        const response = await fetch(`${API_BASE}/services/${destinationId}?lang=${lang}`);
        return response.json();
    },

    async fetchService(id, lang = 'en') {
        const response = await fetch(`${API_BASE}/service/${id}?lang=${lang}`);
        return response.json();
    },

    async login(email, password) {
        const response = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        return response.json();
    },

    async createBooking(bookingData) {
        const response = await fetch(`${API_BASE}/bookings`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bookingData)
        });
        return response.json();
    },

    async fetchUserBookings(userId, lang = 'en') {
        const response = await fetch(`${API_BASE}/bookings/${userId}?lang=${lang}`);
        return response.json();
    },

    async getAIGuide(locationName, userLanguage) {
        const response = await fetch(`${API_BASE}/ai-guide`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ location_name: locationName, user_language: userLanguage })
        });
        return response.json();
    }
};
