window.i18n = {
    dictionary: {},

    async init() {
        await this.loadLanguage(window.state.currentLanguage);
        
        // Listen for language changes
        window.addEventListener('languageChanged', async () => {
            await this.loadLanguage(window.state.currentLanguage);
            this.translateDOM();
        });
    },

    async loadLanguage(lang) {
        try {
            const response = await fetch(`/static/locales/${lang}.json`);
            this.dictionary = await response.json();
            
            // Set RTL/LTR
            if (lang === 'ar') {
                document.body.setAttribute('dir', 'rtl');
            } else {
                document.body.setAttribute('dir', 'ltr');
            }
        } catch (error) {
            console.error('Error loading language dictionary:', error);
        }
    },

    setLanguage(lang) {
        window.state.setLanguage(lang);
    },

    t(key) {
        return this.dictionary[key] || key;
    },

    translateDOM() {
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                el.placeholder = this.t(key);
            } else {
                el.innerHTML = this.t(key);
            }
        });
    }
};
