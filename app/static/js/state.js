window.state = {
    user: JSON.parse(localStorage.getItem('dalil_user')) || null,
    currentLanguage: localStorage.getItem('dalil_lang') || 'en',
    destinations: [],
    currentDestination: null,
    bookings: [],

    setUser(user) {
        this.user = user;
        if (user) {
            localStorage.setItem('dalil_user', JSON.stringify(user));
        } else {
            localStorage.removeItem('dalil_user');
        }
        // Trigger UI update
        window.dispatchEvent(new Event('userStateChanged'));
    },

    setLanguage(lang) {
        this.currentLanguage = lang;
        localStorage.setItem('dalil_lang', lang);
        // Dispatch event so UI can re-render text and fetch new data
        window.dispatchEvent(new Event('languageChanged'));
    }
};
