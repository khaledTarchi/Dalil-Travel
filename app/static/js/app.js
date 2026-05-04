window.app = {
    heroImages: [],
    heroSliderInterval: null,
    currentHeroIndex: 0,
    currentBookingPrice: 0,
    currentBookingDuration: 1,

    async init() {
        await window.i18n.init();
        await window.router.init();

        this.setupMenu();
        this.updateAuthMenu();
        window.addEventListener('userStateChanged', () => this.updateAuthMenu());

        // Update active nav based on current path
        this.updateActiveNav(location.pathname);
        // Monkey-patch history.pushState to track navigation
        const originalPushState = history.pushState;
        history.pushState = function (state, unused, url) {
            originalPushState.apply(this, arguments);
            window.app.updateActiveNav(url);
        };
        window.addEventListener('popstate', () => this.updateActiveNav(location.pathname));
    },

    showLoader() {
        const loader = document.getElementById('global-loader');
        if (loader) loader.classList.add('active');
    },

    hideLoader() {
        const loader = document.getElementById('global-loader');
        if (loader) loader.classList.remove('active');
    },

    showToast(message, type = 'success') {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const icon = type === 'success' ? '<i class="fa-solid fa-circle-check" style="color: var(--success); font-size: 1.5rem;"></i>'
            : '<i class="fa-solid fa-circle-exclamation" style="color: #ff4757; font-size: 1.5rem;"></i>';

        toast.innerHTML = `${icon} <span>${message}</span>`;
        container.appendChild(toast);

        // Trigger reflow for animation
        setTimeout(() => toast.classList.add('show'), 10);

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },

    setupMenu() {
        const toggle = document.getElementById('menu-toggle');
        const menu = document.getElementById('mobile-menu');

        toggle.addEventListener('click', () => {
            menu.classList.toggle('active');
        });
    },

    updateAuthMenu() {
        const authItem = document.getElementById('auth-menu-item');
        const logoutItem = document.getElementById('logout-menu-item');

        if (window.state.user) {
            authItem.style.display = 'none';
            logoutItem.style.display = 'block';
        } else {
            authItem.style.display = 'block';
            logoutItem.style.display = 'none';
        }
    },

    updateActiveNav(path) {
        document.querySelectorAll('.bottom-nav a').forEach(a => a.classList.remove('active'));
        if (path === '/') {
            const el = document.getElementById('bnav-home');
            if (el) el.classList.add('active');
        } else if (path.startsWith('/dashboard')) {
            const el = document.getElementById('bnav-bookings');
            if (el) el.classList.add('active');
        } else if (path.startsWith('/login') || path.startsWith('/profile')) {
            const el = document.getElementById('bnav-profile');
            if (el) el.classList.add('active');
        }
    },

    toggleAuthTab(tab) {
        document.getElementById('login-form-container').style.display = tab === 'login' ? 'block' : 'none';
        document.getElementById('register-form-container').style.display = tab === 'register' ? 'block' : 'none';

        document.querySelectorAll('.auth-tab').forEach(el => el.classList.remove('active'));
        document.getElementById(`tab-${tab}`).classList.add('active');
    },

    async handleLogin(e) {
        e.preventDefault();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

        this.showLoader();
        try {
            const res = await window.api.login(email, password);
            this.hideLoader();
            if (res.success) {
                window.state.setUser(res.user);
                this.showToast(window.i18n.t('toast.login_success'));
                window.router.navigateTo('/dashboard');
            } else {
                this.showToast(res.error, 'error');
            }
        } catch (err) {
            this.hideLoader();
            this.showToast(window.i18n.t('toast.net_error'), 'error');
        }
    },

    async handleRegister(e) {
        e.preventDefault();
        const firstName = document.getElementById('reg-first-name').value;
        const lastName = document.getElementById('reg-last-name').value;
        const email = document.getElementById('reg-email').value;
        const password = document.getElementById('reg-password').value;

        this.showLoader();
        try {
            const res = await window.api.register(firstName, lastName, email, password);
            this.hideLoader();
            if (res.success) {
                this.showToast(window.i18n.t('toast.reg_success'));
                this.toggleAuthTab('login');
            } else {
                this.showToast(res.error, 'error');
            }
        } catch (err) {
            this.hideLoader();
            this.showToast(window.i18n.t('toast.net_error'), 'error');
        }
    },

    logout() {
        window.state.setUser(null);
        document.getElementById('mobile-menu').classList.remove('active');
        window.router.navigateTo('/');
    },

    startHeroSlider() {
        if (this.heroSliderInterval) clearInterval(this.heroSliderInterval);
        this.heroSliderInterval = setInterval(() => {
            if (this.heroImages.length > 0) {
                this.currentHeroIndex = (this.currentHeroIndex + 1) % this.heroImages.length;
                const heroEl = document.getElementById('home-hero');
                if (heroEl) {
                    heroEl.style.backgroundImage = `url('${this.heroImages[this.currentHeroIndex]}')`;
                }
            }
        }, 5000);
    },

    stopHeroSlider() {
        if (this.heroSliderInterval) {
            clearInterval(this.heroSliderInterval);
            this.heroSliderInterval = null;
        }
    },

    toggleAccordion(element) {
        const body = element.nextElementSibling;
        const icon = element.querySelector('i');

        if (body.classList.contains('active')) {
            body.classList.remove('active');
            icon.classList.remove('fa-chevron-up');
            icon.classList.add('fa-chevron-down');
        } else {
            body.classList.add('active');
            icon.classList.remove('fa-chevron-down');
            icon.classList.add('fa-chevron-up');
        }
    },

    updateDuration(change, basePrice) {
        let newDuration = this.currentBookingDuration + change;
        if (newDuration < 1) newDuration = 1;
        if (newDuration > 30) newDuration = 30; // max 30 days

        this.currentBookingDuration = newDuration;
        this.currentBookingPrice = basePrice * newDuration;

        document.getElementById('duration-display').innerText = newDuration;
        document.getElementById('total-price-display').innerText = this.currentBookingPrice;
    },

    async handleBooking(e, serviceId, destinationId) {
        e.preventDefault();

        const dateInput = document.getElementById('booking-date').value;
        const paymentMethod = document.getElementById('booking-payment').value;

        // Calculate end date
        const startDate = new Date(dateInput);
        const endDate = new Date(startDate);
        endDate.setDate(startDate.getDate() + this.currentBookingDuration);

        const bookingData = {
            user_id: window.state.user.id,
            service_id: serviceId,
            start_date: startDate.toISOString().split('T')[0],
            end_date: endDate.toISOString().split('T')[0],
            total_amount: this.currentBookingPrice,
            payment_method: paymentMethod
        };

        this.showLoader();
        try {
            const res = await window.api.createBooking(bookingData);
            this.hideLoader();
            if (res.success) {
                this.showToast(window.i18n.t('toast.book_success'));
                window.router.navigateTo('/dashboard');
            } else {
                this.showToast(window.i18n.t('toast.book_fail') + ' ' + res.error, 'error');
            }
        } catch (err) {
            this.hideLoader();
            this.showToast(window.i18n.t('toast.net_error'), 'error');
        }
    },

    async askAIGuide(locationName) {
        const container = document.getElementById('ai-response-container');
        container.style.display = 'block';
        container.innerHTML = '<div style="text-align: center;"><i class="fa-solid fa-spinner fa-spin" style="font-size: 2rem; color: var(--primary);"></i><br>' + window.i18n.t('toast.ai_loading') + '</div>';

        try {
            const res = await window.api.getAIGuide(locationName, window.state.currentLanguage);
            if (res.info) {
                // Parse the timeline format: HH:MM AM/PM|Activity
                const lines = res.info.split('\n').map(l => l.trim()).filter(l => l.includes('|'));
                if (lines.length > 0) {
                    let timelineHtml = '<div class="timeline-container">';
                    lines.forEach(line => {
                        const parts = line.split('|');
                        if (parts.length >= 2) {
                            const time = parts[0].trim();
                            const activity = parts.slice(1).join('|').trim();
                            timelineHtml += `
                                <div class="timeline-item">
                                    <div class="timeline-time">${time}</div>
                                    <div class="timeline-content">${activity}</div>
                                </div>
                            `;
                        }
                    });
                    timelineHtml += '</div>';
                    container.innerHTML = timelineHtml;
                } else {
                    container.innerText = res.info; // fallback
                }
            } else {
                container.innerText = window.i18n.t('toast.ai_fail');
            }
        } catch (err) {
            container.innerText = window.i18n.t('toast.ai_err');
        }
    },

    initMap(dest, services) {
        if (!document.getElementById('map-container')) return;

        // Initialize Map
        const map = L.map('map-container').setView([dest.lat, dest.lng], 12);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Add Destination Pin
        L.marker([dest.lat, dest.lng]).addTo(map)
            .bindPopup(`<b>${dest.name}</b><br>City Center`)
            .openPopup();

        // Add Service Pins (Mocking slight offsets for pins based on id)
        services.forEach(s => {
            const latOffset = (Math.random() - 0.5) * 0.05;
            const lngOffset = (Math.random() - 0.5) * 0.05;
            const serviceLat = dest.lat + latOffset;
            const serviceLng = dest.lng + lngOffset;

            let iconHtml = '<i class="fa-solid fa-location-dot"></i>';
            if (s.type === 'accommodation') iconHtml = '<i class="fa-solid fa-bed"></i>';
            if (s.type === 'food') iconHtml = '<i class="fa-solid fa-utensils"></i>';
            if (s.type === 'transport') iconHtml = '<i class="fa-solid fa-car"></i>';
            if (s.type === 'guide') iconHtml = '<i class="fa-solid fa-person-hiking"></i>';

            const customIcon = L.divIcon({
                className: 'custom-leaflet-icon',
                html: `<div style="background: var(--primary); color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 2px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3); font-size: 14px;">${iconHtml}</div>`,
                iconSize: [30, 30],
                iconAnchor: [15, 15]
            });

            const popupContent = `
                <div style="text-align: center;">
                    <h4 style="margin-bottom: 5px; color: var(--secondary);">${s.name}</h4>
                    <p style="margin: 0; font-size: 0.8rem;">${s.rating} <i class="fa-solid fa-star" style="color: gold;"></i> | ${s.base_price} DZD</p>
                    <button class="btn btn-primary" style="padding: 5px 10px; font-size: 0.8rem; margin-top: 10px;" onclick="window.router.navigateTo('/booking/${s.id}')">${window.i18n.t('btn.book') || 'Book Now'}</button>
                </div>
            `;

            L.marker([serviceLat, serviceLng], { icon: customIcon }).addTo(map)
                .bindPopup(popupContent);
        });
    },

    search() {
        const query = document.getElementById('search-input').value.toLowerCase();
        if (!query) return;

        this.showLoader();
        window.api.fetchDestinations(window.state.currentLanguage).then(dests => {
            this.hideLoader();
            const match = dests.find(d => d.name.toLowerCase().includes(query) || d.description.toLowerCase().includes(query));
            if (match) {
                window.router.navigateTo(`/destination/${match.id}`);
            } else {
                this.showToast(window.i18n.t('toast.search_fail'), 'error');
            }
        }).catch(err => {
            this.hideLoader();
            this.showToast(window.i18n.t('toast.search_err'), 'error');
        });
    },

    showEmergencyModal() {
        document.getElementById('emergency-modal').classList.add('active');
        document.getElementById('mobile-menu').classList.remove('active');
    },

    closeEmergencyModal() {
        document.getElementById('emergency-modal').classList.remove('active');
    },

    toggleFavorite(id, event) {
        event.stopPropagation();
        let favorites = JSON.parse(localStorage.getItem('dalil_favorites') || '[]');
        if (favorites.includes(id)) {
            favorites = favorites.filter(favId => favId !== id);
            this.showToast(window.i18n.t('toast.fav_remove'), 'success');
        } else {
            favorites.push(id);
            this.showToast(window.i18n.t('toast.fav_add'), 'success');
        }
        localStorage.setItem('dalil_favorites', JSON.stringify(favorites));
        
        if (window.location.pathname === '/favorites') {
            window.router.renderFavorites();
        }
    }
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    window.app.init();
});
