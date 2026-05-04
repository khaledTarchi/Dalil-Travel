window.router = {
    routes: {
        '/': 'renderHome',
        '/destination/:id': 'renderDestination',
        '/dashboard': 'renderDashboard',
        '/login': 'renderLogin',
        '/booking/:id': 'renderBooking',
        '/partner': 'renderPartner',
        '/favorites': 'renderFavorites',
        '/help': 'renderHelp',
        '/delivery': 'renderDelivery',
        '/map': 'renderMap'
    },

    async init() {
        document.body.addEventListener('click', e => {
            if (e.target.matches('[data-link]') || e.target.closest('[data-link]')) {
                e.preventDefault();
                const link = e.target.matches('[data-link]') ? e.target : e.target.closest('[data-link]');
                this.navigateTo(link.href);
            }
        });

        window.addEventListener('popstate', () => this.route());

        // Re-render current route on language or user change
        window.addEventListener('languageChanged', () => this.route());
        window.addEventListener('userStateChanged', () => this.route());

        await this.route();
    },

    navigateTo(url) {
        history.pushState(null, null, url);
        this.route();
        // Close mobile menu if open
        document.getElementById('mobile-menu').classList.remove('active');
    },

    async route() {
        const path = location.pathname;
        let match = null;

        // Simple router logic
        for (const [routePath, handler] of Object.entries(this.routes)) {
            const regex = new RegExp('^' + routePath.replace(/:[^\s/]+/g, '([\\w-]+)') + '$');
            const result = path.match(regex);
            if (result) {
                match = { handler, params: result.slice(1) };
                break;
            }
        }

        if (match) {
            await this[match.handler](...match.params);
            window.i18n.translateDOM();
        } else {
            this.navigateTo('/');
        }
    },

    async renderHome() {
        const lang = window.state.currentLanguage;
        const destinations = await window.api.fetchDestinations(lang);

        // Pick top images for hero
        const heroImages = destinations.map(d => d.image_url);
        // We will cycle through them in app.js
        window.app.heroImages = heroImages;

        let html = `
            <section class="hero" id="home-hero" style="background-image: url('${heroImages[0]}')">
                <div class="search-container">
                    <h1 data-i18n="home.hero.title">Discover the Magic of Algeria</h1>
                    <div class="search-bar">
                        <input type="text" id="search-input" data-i18n="home.search.placeholder" placeholder="Where do you want to go?">
                        <button onclick="window.app.search()"><i class="fa-solid fa-magnifying-glass"></i></button>
                    </div>
                </div>
            </section>

            <!-- Quick Services Grid -->
            <div class="quick-services">
                <a href="/help" data-link class="quick-btn">
                    <i class="fa-solid fa-circle-info"></i> <span data-i18n="quick.help">Help</span>
                </a>
                <a href="/delivery" data-link class="quick-btn">
                    <i class="fa-solid fa-motorcycle"></i> <span data-i18n="quick.delivery">Delivery</span>
                </a>
                <a href="/map" data-link class="quick-btn">
                    <i class="fa-solid fa-map"></i> <span data-i18n="quick.map">Map</span>
                </a>
                <a href="#" class="quick-btn" onclick="window.app.showEmergencyModal()">
                    <i class="fa-solid fa-truck-medical"></i> <span data-i18n="quick.emergency">Emergency</span>
                </a>
            </div>

            <!-- Promotional Banner -->
            <div class="promo-banner">
                <div class="promo-content">
                    <h2 data-i18n="promo.title">20% OFF Hotel Bookings</h2>
                    <p data-i18n="promo.desc">Limited time offer on all premium accommodations.</p>
                </div>
                <button class="btn btn-success" style="padding: 1rem 2rem; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(0,0,0,0.2);" onclick="window.router.navigateTo('/partner')" data-i18n="promo.btn">Claim Offer</button>
            </div>

            <section class="section">
                <h2 class="section-title" data-i18n="home.popular">Popular Destinations</h2>
                <div class="destinations-grid">
                    ${destinations.map(d => `
                        <div class="destination-card" onclick="window.router.navigateTo('/destination/${d.id}')">
                            <img src="${d.image_url}" alt="${d.name}" class="card-img">
                            <div class="card-content">
                                <h3>${d.name}</h3>
                                <p>${d.description}</p>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </section>
        `;
        document.getElementById('app').innerHTML = html;

        // Start hero slider if not already started
        window.app.startHeroSlider();
    },

    async renderDestination(id) {
        window.app.stopHeroSlider();
        const lang = window.state.currentLanguage;
        const dest = await window.api.fetchDestination(id, lang);
        if (dest.error) {
            this.navigateTo('/');
            return;
        }

        const services = await window.api.fetchServices(id, lang);

        const categories = {
            'accommodation': [],
            'food': [],
            'guide': [],
            'transport': [],
            'insurance': []
        };

        services.forEach(s => {
            if (categories[s.type]) {
                categories[s.type].push(s);
            }
        });

        let html = `
            <div class="dest-header" style="background-image: url('${dest.image_url}')">
                <h1>${dest.name}</h1>
            </div>
            <div class="dest-content">
                <div class="left-col">
                    <h2 data-i18n="dest.services">Available Services</h2>
                    <div class="services-accordion" id="services-accordion">
                        ${Object.keys(categories).map(cat => {
            if (categories[cat].length === 0) return '';
            return `
                                <div class="service-category">
                                    <div class="service-header" onclick="window.app.toggleAccordion(this)">
                                        <span data-i18n="service.${cat}">${cat}</span>
                                        <i class="fa-solid fa-chevron-down"></i>
                                    </div>
                                    <div class="service-body">
                                        ${categories[cat].map(s => `
                                            <div class="service-item">
                                                <img src="${s.image_url}" alt="${s.name}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 8px; margin-right: 1rem;">
                                                <div style="flex: 1;">
                                                    ${s.is_sponsored ? '<span class="sponsored-badge"><span data-i18n="service.sponsored">Sponsored</span> <i class="fa-solid fa-star"></i></span>' : ''}
                                                    <h4>${s.name}</h4>
                                                    <p style="font-size: 0.9rem; color: #666;">${s.description}</p>
                                                    <p><i class="fa-solid fa-star" style="color: gold;"></i> ${s.rating}</p>
                                                    <p><strong>${s.base_price}</strong> <span data-i18n="price.currency">DZD</span></p>
                                                    ${s.company_name ? `<p class="provider-text"><span data-i18n="service.provided_by">Provided by</span> ${s.company_name}</p>` : ''}
                                                </div>
                                                <button class="btn btn-primary" onclick="window.router.navigateTo('/booking/${s.id}')" data-i18n="btn.book">Book</button>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            `;
        }).join('')}
                    </div>
                </div>
                <div class="right-col">
                    <div id="map-container" class="glass-panel" style="height: 400px; width: 100%; border-radius: 16px; overflow: hidden; margin-bottom: 2rem;"></div>
                    
                    <div class="ai-guide-widget">
                        <i class="fa-solid fa-robot"></i>
                        <h3 data-i18n="dest.ai_guide">1-Day AI Itinerary</h3>
                        <p style="font-size:0.9rem; margin:0.5rem 0;" data-i18n="dest.ai_desc">Get an AI-generated 1-day itinerary for this location.</p>
                        <button class="btn btn-primary" style="width: 100%; margin-top: 1rem;" onclick="window.app.askAIGuide('${dest.name}')" data-i18n="dest.ai_btn">Generate Itinerary</button>
                        <div id="ai-response-container" class="ai-response" style="display:none;"></div>
                        <button class="btn btn-success" style="width: 100%; margin-top: 1rem; background: var(--secondary);" onclick="window.app.showToast(window.i18n.t('toast.premium'));"><i class="fa-solid fa-volume-high"></i> <span data-i18n="dest.ai_premium">Listen with AI (Premium)</span></button>
                    </div>
                </div>
            </div>
        `;
        document.getElementById('app').innerHTML = html;

        // Initialize Map after rendering DOM
        setTimeout(() => window.app.initMap(dest, services), 100);
    },

    async renderLogin() {
        window.app.stopHeroSlider();
        if (window.state.user) {
            this.navigateTo('/dashboard');
            return;
        }
        let html = `
            <div class="login-container" style="min-height: calc(100vh - 70px); display: flex; align-items: center; justify-content: center; background: url('/static/img/sahara.png') center/cover;">
                <div class="glass-panel" style="padding: 2rem; width: 100%; max-width: 400px;">
                    <div class="auth-tabs">
                        <div class="auth-tab active" id="tab-login" onclick="window.app.toggleAuthTab('login')" data-i18n="auth.login_tab">Login</div>
                        <div class="auth-tab" id="tab-register" onclick="window.app.toggleAuthTab('register')" data-i18n="auth.register_tab">Register</div>
                    </div>
                    
                    <div id="login-form-container">
                        <h2 data-i18n="login.title" style="text-align: center; margin-bottom: 1.5rem; color: var(--secondary);">Welcome Back</h2>
                        <form id="login-form" onsubmit="window.app.handleLogin(event)">
                            <div style="margin-bottom: 1rem;">
                                <label data-i18n="login.email" style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);">Email Address</label>
                                <input type="email" id="login-email" required style="width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 8px;">
                            </div>
                            <div style="margin-bottom: 1.5rem;">
                                <label data-i18n="login.password" style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);">Password</label>
                                <input type="password" id="login-password" required style="width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 8px;">
                            </div>
                            <button type="submit" class="btn btn-primary" style="width: 100%; padding: 1rem;" data-i18n="login.submit">Login</button>
                        </form>
                    </div>

                    <div id="register-form-container" style="display: none;">
                        <h2 style="text-align: center; margin-bottom: 1.5rem; color: var(--secondary);" data-i18n="auth.create_account">Create Account</h2>
                        <form id="register-form" onsubmit="window.app.handleRegister(event)">
                            <div style="margin-bottom: 1rem;">
                                <label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);" data-i18n="auth.fname">First Name</label>
                                <input type="text" id="reg-first-name" required style="width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 8px;">
                            </div>
                            <div style="margin-bottom: 1rem;">
                                <label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);" data-i18n="auth.lname">Last Name</label>
                                <input type="text" id="reg-last-name" required style="width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 8px;">
                            </div>
                            <div style="margin-bottom: 1rem;">
                                <label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);" data-i18n="auth.email">Email Address</label>
                                <input type="email" id="reg-email" required style="width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 8px;">
                            </div>
                            <div style="margin-bottom: 1.5rem;">
                                <label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);" data-i18n="auth.password">Password</label>
                                <input type="password" id="reg-password" required style="width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 8px;">
                            </div>
                            <button type="submit" class="btn btn-success" style="width: 100%; padding: 1rem;" data-i18n="auth.register_btn">Register</button>
                        </form>
                    </div>
                </div>
            </div>
        `;
        document.getElementById('app').innerHTML = html;
    },

    async renderBooking(serviceId) {
        window.app.stopHeroSlider();
        if (!window.state.user) {
            window.app.showToast(window.i18n.t('toast.login_first'), 'error');
            this.navigateTo('/login');
            return;
        }

        const lang = window.state.currentLanguage;
        const service = await window.api.fetchService(serviceId, lang);

        if (service.error) {
            this.navigateTo('/');
            return;
        }

        window.app.currentBookingPrice = service.base_price;
        window.app.currentBookingDuration = 1;

        let html = `
            <div class="section" style="max-width: 600px; margin: 3rem auto;">
                <div class="glass-panel" style="padding: 2rem;">
                    <h2 data-i18n="booking.title" style="margin-bottom: 1.5rem; color: var(--secondary); text-align: center; font-size: 2rem;">Book Service</h2>
                    
                    <div style="background: rgba(46, 139, 87, 0.1); padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; border-left: 4px solid var(--primary);">
                        <h3 style="color: var(--primary); margin-bottom: 0.5rem;">${service.name}</h3>
                        <p style="color: #555; margin-bottom: 0.5rem;">${service.description}</p>
                        <p style="font-weight: bold; font-size: 1.1rem; color: var(--secondary);">${service.base_price} <span data-i18n="price.currency">DZD</span> / day</p>
                    </div>

                    <form id="booking-form" onsubmit="window.app.handleBooking(event, ${service.id}, ${service.destination_id})">
                        <div style="margin-bottom: 1.5rem;">
                            <label data-i18n="booking.date" style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);">Start Date</label>
                            <input type="date" id="booking-date" required style="width: 100%; padding: 1rem; border: 2px solid #eee; border-radius: 8px; font-family: 'Outfit', sans-serif;">
                        </div>

                        <div style="margin-bottom: 1.5rem;">
                            <label data-i18n="booking.duration" style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);">Duration (Days)</label>
                            <div style="display: flex; align-items: center; gap: 1rem;">
                                <button type="button" class="btn" style="background: #eee; color: #333; font-size: 1.2rem; width: 40px; height: 40px; border-radius: 50%;" onclick="window.app.updateDuration(-1, ${service.base_price})">-</button>
                                <span id="duration-display" style="font-weight: bold; font-size: 1.5rem; min-width: 40px; text-align: center;">1</span>
                                <button type="button" class="btn" style="background: #eee; color: #333; font-size: 1.2rem; width: 40px; height: 40px; border-radius: 50%;" onclick="window.app.updateDuration(1, ${service.base_price})">+</button>
                            </div>
                        </div>

                        <div style="margin-bottom: 2rem;">
                            <label data-i18n="booking.payment" style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);">Payment Method</label>
                            <select id="booking-payment" style="width: 100%; padding: 1rem; border: 2px solid #eee; border-radius: 8px; background: white; font-family: 'Outfit', sans-serif;">
                                <option value="cash" data-i18n="booking.cash">Cash on Arrival</option>
                                <option value="card" data-i18n="booking.card">Credit Card</option>
                                <option value="baridimob" data-i18n="booking.baridimob">BaridiMob</option>
                            </select>
                        </div>

                        <div style="margin-top: 2rem; border-top: 2px dashed #ccc; padding-top: 1.5rem; margin-bottom: 2rem; text-align: right;">
                            <h3 style="color: #666;"><span data-i18n="booking.total">Total Amount</span>: <span id="total-price-display" style="font-size: 2rem; color: var(--success);">${service.base_price}</span> <span data-i18n="price.currency" style="color: var(--success); font-weight: bold;">DZD</span></h3>
                        </div>

                        <div style="display: flex; gap: 1rem;">
                            <button type="button" class="btn" style="flex: 1; background: #ddd; color: #333;" onclick="window.router.navigateTo('/destination/${service.destination_id}')" data-i18n="btn.cancel">Cancel</button>
                            <button type="submit" class="btn btn-primary" style="flex: 2; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(46, 139, 87, 0.4);" data-i18n="btn.book">Confirm Booking</button>
                        </div>
                    </form>
                </div>
            </div>
        `;
        document.getElementById('app').innerHTML = html;
    },

    async renderDashboard() {
        window.app.stopHeroSlider();
        if (!window.state.user) {
            this.navigateTo('/login');
            return;
        }

        const lang = window.state.currentLanguage;
        const bookings = await window.api.fetchUserBookings(window.state.user.id, lang);

        let headerImage = '/static/img/oran.png';
        if (bookings.length > 0) {
            headerImage = bookings[0].destination_image;
        }

        let html = `
            <div class="dashboard-header" style="background-image: url('${headerImage}')">
                <h1 data-i18n="dashboard.title">Your Active Trips</h1>
            </div>
            <div class="dashboard-content">
                <div class="glass-panel" style="padding: 2rem; min-height: 400px;">
                    ${bookings.length === 0 ? `<p style="text-align: center; color: #666; font-size: 1.2rem; padding: 3rem 0;" data-i18n="dashboard.empty">You have no active bookings.</p>` : `
                        <div class="bookings-list">
                            ${bookings.map(b => `
                                <div class="booking-item">
                                    <div class="booking-info">
                                        <h4>${b.destination_name} - ${b.service_name}</h4>
                                        <p><i class="fa-regular fa-calendar"></i> ${b.start_date} to ${b.end_date}</p>
                                        <p><i class="fa-solid fa-money-bill"></i> ${b.total_amount} <span data-i18n="price.currency">DZD</span> (${b.payment_status})</p>
                                    </div>
                                    <div class="booking-actions">
                                        <button class="btn" style="background: var(--primary); color: white;" onclick="window.router.navigateTo('/destination/${b.destination_id}')" data-i18n="dashboard.view_dest">View Destination</button>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    `}
                </div>
            </div>
        `;
        document.getElementById('app').innerHTML = html;
    },

    async renderPartner() {
        window.app.stopHeroSlider();
        let html = `
            <div class="section" style="min-height: calc(100vh - 70px); display: flex; align-items: center; justify-content: center; background: url('/static/img/oran.png') center/cover;">
                <div class="glass-panel" style="padding: 3rem; width: 90%; max-width: 600px;">
                    <h2 data-i18n="partner.title" style="text-align: center; color: var(--secondary); margin-bottom: 1rem; font-size: 2.5rem;">Partner With Us</h2>
                    <p data-i18n="partner.subtitle" style="text-align: center; color: #555; margin-bottom: 2rem; font-size: 1.1rem;">Join Dalil Travel and grow your tourism business.</p>
                    <form id="partner-form" onsubmit="event.preventDefault(); window.app.showToast(window.i18n.t('toast.apply_success')); window.router.navigateTo('/');">
                        <div style="margin-bottom: 1.5rem;">
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);" data-i18n="partner.company">Company Name</label>
                            <input type="text" required style="width: 100%; padding: 1rem; border: 2px solid #eee; border-radius: 8px;">
                        </div>
                        <div style="margin-bottom: 1.5rem;">
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);" data-i18n="partner.service_type">Service Type</label>
                            <select style="width: 100%; padding: 1rem; border: 2px solid #eee; border-radius: 8px; background: white;">
                                <option value="accommodation" data-i18n="partner.type_hotel">Hotel / Accommodation</option>
                                <option value="food" data-i18n="partner.type_food">Restaurant / Cafe</option>
                                <option value="transport" data-i18n="partner.type_transport">Transport Agency</option>
                                <option value="guide" data-i18n="partner.type_guide">Tour Guide</option>
                            </select>
                        </div>
                        <div style="margin-bottom: 1.5rem;">
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);" data-i18n="auth.email">Email Address</label>
                            <input type="email" required style="width: 100%; padding: 1rem; border: 2px solid #eee; border-radius: 8px;">
                        </div>
                        <button type="submit" class="btn btn-primary" style="width: 100%; padding: 1rem; font-size: 1.2rem; box-shadow: 0 4px 15px rgba(46, 139, 87, 0.3);" data-i18n="partner.submit">Submit Application</button>
                    </form>
                </div>
            </div>
        `;
        document.getElementById('app').innerHTML = html;
    },

    async renderFavorites() {
        window.app.stopHeroSlider();
        
        const favorites = JSON.parse(localStorage.getItem('dalil_favorites') || '[]');
        
        let html = `
            <div class="dashboard-header" style="background-image: url('/static/img/tlemcen.png')">
                <h1 data-i18n="favorites.title">Your Favorites</h1>
            </div>
            <div class="section" style="max-width: 1000px; margin: 3rem auto;">
                <div class="glass-panel" style="padding: 2rem; min-height: 400px;">
                    <div id="favorites-container">
                        <div style="text-align: center; padding: 3rem 0;">
                            <i class="fa-solid fa-spinner fa-spin" style="font-size: 2rem; color: var(--primary);"></i>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.getElementById('app').innerHTML = html;

        const container = document.getElementById('favorites-container');
        
        if (favorites.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 3rem 0; color: #666;">
                    <i class="fa-regular fa-heart" style="font-size: 4rem; color: #ccc; margin-bottom: 1rem;"></i>
                    <h3 style="margin-bottom: 1rem;" data-i18n="favorites.empty_title">No favorites yet</h3>
                    <p style="margin-bottom: 2rem;" data-i18n="favorites.empty_desc">Start exploring destinations and tap the heart icon to save them here.</p>
                    <button class="btn btn-primary" onclick="window.router.navigateTo('/')" data-i18n="favorites.explore_btn">Explore Destinations</button>
                </div>
            `;
            return;
        }

        const lang = window.state.currentLanguage;
        const allDests = await window.api.fetchDestinations(lang);
        const favDests = allDests.filter(d => favorites.includes(d.id));

        container.innerHTML = `
            <div class="destinations-grid">
                ${favDests.map(d => `
                    <div class="destination-card">
                        <div style="position: absolute; top: 10px; right: 10px; z-index: 2; background: white; width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.2);" onclick="window.app.toggleFavorite(${d.id}, event)">
                            <i class="fa-solid fa-heart" style="color: #ff4757; font-size: 1.2rem;"></i>
                        </div>
                        <img src="${d.image_url}" alt="${d.name}" class="card-img" onclick="window.router.navigateTo('/destination/${d.id}')" style="cursor: pointer;">
                        <div class="card-content" onclick="window.router.navigateTo('/destination/${d.id}')" style="cursor: pointer;">
                            <h3>${d.name}</h3>
                            <p>${d.description}</p>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    },

    async renderHelp() {
        window.app.stopHeroSlider();
        let html = `
            <div class="section" style="max-width: 800px; margin: 3rem auto;">
                <h2 data-i18n="help.title" style="color: var(--secondary); margin-bottom: 2rem; text-align: center; font-size: 2.5rem;">Help & Support</h2>
                
                <div class="glass-panel" style="padding: 2rem; margin-bottom: 2rem;">
                    <h3 style="color: var(--primary); margin-bottom: 1.5rem;" data-i18n="help.faq_title">Frequently Asked Questions</h3>
                    <div class="services-accordion">
                        <div class="service-category">
                            <div class="service-header" onclick="window.app.toggleAccordion(this)">
                                <span data-i18n="help.faq_q1">How do I cancel a booking?</span>
                                <i class="fa-solid fa-chevron-down"></i>
                            </div>
                            <div class="service-body" style="padding: 1rem; color: #555;" data-i18n="help.faq_a1">
                                You can cancel a booking directly from your Dashboard up to 24 hours before the start date for a full refund.
                            </div>
                        </div>
                        <div class="service-category">
                            <div class="service-header" onclick="window.app.toggleAccordion(this)">
                                <span data-i18n="help.faq_q2">What payment methods are supported?</span>
                                <i class="fa-solid fa-chevron-down"></i>
                            </div>
                            <div class="service-body" style="padding: 1rem; color: #555;" data-i18n="help.faq_a2">
                                We support Cash on Arrival, Credit Card, and BaridiMob for seamless local transactions.
                            </div>
                        </div>
                        <div class="service-category">
                            <div class="service-header" onclick="window.app.toggleAccordion(this)">
                                <span data-i18n="help.faq_q3">How do I contact an agency?</span>
                                <i class="fa-solid fa-chevron-down"></i>
                            </div>
                            <div class="service-body" style="padding: 1rem; color: #555;" data-i18n="help.faq_a3">
                                Once you book a service, the agency's contact information will be provided in your booking details.
                            </div>
                        </div>
                    </div>
                </div>

                <div class="glass-panel" style="padding: 2rem;">
                    <h3 style="color: var(--primary); margin-bottom: 1.5rem;" data-i18n="help.contact_title">Contact Us</h3>
                    <form onsubmit="event.preventDefault(); window.app.showToast(window.i18n.t('toast.msg_sent')); this.reset();">
                        <div style="margin-bottom: 1rem;">
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);" data-i18n="help.contact_label">Your Message</label>
                            <textarea required rows="4" style="width: 100%; padding: 1rem; border: 2px solid #eee; border-radius: 8px; font-family: 'Outfit', sans-serif; resize: vertical;"></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary" style="padding: 1rem 2rem;" data-i18n="help.contact_btn">Send Message</button>
                    </form>
                </div>
            </div>
        `;
        document.getElementById('app').innerHTML = html;
    },

    async renderDelivery() {
        window.app.stopHeroSlider();
        let html = `
            <div class="section" style="max-width: 800px; margin: 3rem auto; text-align: center;">
                <h2 style="color: var(--secondary); margin-bottom: 1rem; font-size: 2.5rem;" data-i18n="delivery.title">Dalil Delivery</h2>
                <p style="color: #555; margin-bottom: 2rem; font-size: 1.1rem;" data-i18n="delivery.subtitle">Fast and reliable local delivery of food and essentials directly to your hotel or location.</p>
                
                <div class="glass-panel" style="padding: 3rem; background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));">
                    <i class="fa-solid fa-motorcycle" style="font-size: 5rem; color: #f39c12; margin-bottom: 1.5rem;"></i>
                    <h3 style="color: var(--primary); margin-bottom: 1.5rem;" data-i18n="delivery.coming">Coming Soon to Your Area</h3>
                    <p style="color: #666; margin-bottom: 2rem; line-height: 1.6;" data-i18n="delivery.desc">We are currently partnering with top local restaurants and stores to bring Dalil Delivery to all major tourist destinations. Stay tuned for updates!</p>
                    <div style="display: inline-flex; background: white; border-radius: 30px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 100%; max-width: 400px;">
                        <input type="email" data-i18n="delivery.placeholder" placeholder="Enter email for updates" style="flex: 1; border: none; padding: 1rem 1.5rem; outline: none;">
                        <button class="btn btn-primary" style="border-radius: 0; padding: 1rem 2rem;" onclick="window.app.showToast(window.i18n.t('toast.sub_success'), 'success');" data-i18n="delivery.notify">Notify Me</button>
                    </div>
                </div>
            </div>
        `;
        document.getElementById('app').innerHTML = html;
    },

    async renderMap() {
        window.app.stopHeroSlider();
        const lang = window.state.currentLanguage;
        const destinations = await window.api.fetchDestinations(lang);
        
        let html = `
            <div style="height: calc(100vh - 70px); width: 100%; position: relative;">
                <div id="global-map" style="height: 100%; width: 100%; z-index: 1;"></div>
                <div class="glass-panel" style="position: absolute; top: 20px; left: 20px; right: 20px; z-index: 2; padding: 1rem; border-radius: 12px; display: flex; align-items: center; gap: 1rem; max-width: 500px; margin: 0 auto;">
                    <i class="fa-solid fa-earth-africa" style="color: var(--primary); font-size: 1.5rem;"></i>
                    <h3 style="margin: 0; color: var(--secondary);" data-i18n="map.explore">Explore Algeria</h3>
                </div>
            </div>
        `;
        document.getElementById('app').innerHTML = html;

        setTimeout(() => {
            const map = L.map('global-map').setView([33.0, 3.0], 5);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);

            destinations.forEach(d => {
                const icon = L.divIcon({
                    className: 'custom-leaflet-icon',
                    html: '<div style="background: var(--secondary); color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 2px solid white; box-shadow: 0 4px 10px rgba(0,0,0,0.3);"><i class="fa-solid fa-location-dot" style="font-size: 18px;"></i></div>',
                    iconSize: [40, 40],
                    iconAnchor: [20, 20]
                });

                L.marker([d.lat, d.lng], {icon: icon}).addTo(map)
                    .bindPopup(`
                        <div style="text-align: center; min-width: 150px;">
                            <img src="${d.image_url}" style="width: 100%; height: 80px; object-fit: cover; border-radius: 8px; margin-bottom: 10px;">
                            <h4 style="margin: 0 0 5px 0; color: var(--secondary);">${d.name}</h4>
                            <button class="btn btn-primary" style="padding: 5px 15px; font-size: 0.9rem;" onclick="window.router.navigateTo('/destination/${d.id}')">${window.i18n.t('btn.view') || 'View'}</button>
                        </div>
                    `);
            });
        }, 100);
    }
};
