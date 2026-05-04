import os

filepath = 'app/static/js/router.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('<span class="sponsored-badge">Sponsored <i class="fa-solid fa-star"></i></span>', '<span class="sponsored-badge"><span data-i18n="service.sponsored">Sponsored</span> <i class="fa-solid fa-star"></i></span>'),
    ('<p class="provider-text">Provided by ${s.company_name}</p>', '<p class="provider-text"><span data-i18n="service.provided_by">Provided by</span> ${s.company_name}</p>'),
    ('<p style="font-size:0.9rem; margin:0.5rem 0;">Get an AI-generated 1-day itinerary for this location.</p>', '<p style="font-size:0.9rem; margin:0.5rem 0;" data-i18n="dest.ai_desc">Get an AI-generated 1-day itinerary for this location.</p>'),
    ("onclick=\"window.app.askAIGuide('${dest.name}')\">Generate Itinerary</button>", "onclick=\"window.app.askAIGuide('${dest.name}')\" data-i18n=\"dest.ai_btn\">Generate Itinerary</button>"),
    ("onclick=\"alert('Premium Feature!')\"><i class=\"fa-solid fa-volume-high\"></i> Listen with AI (Premium)</button>", "onclick=\"window.app.showToast(window.i18n.t('toast.premium'));\"><i class=\"fa-solid fa-volume-high\"></i> <span data-i18n=\"dest.ai_premium\">Listen with AI (Premium)</span></button>"),
    
    ('<div class="auth-tab active" id="tab-login" onclick="window.app.toggleAuthTab(\'login\')">Login</div>', '<div class="auth-tab active" id="tab-login" onclick="window.app.toggleAuthTab(\'login\')" data-i18n="auth.login_tab">Login</div>'),
    ('<div class="auth-tab" id="tab-register" onclick="window.app.toggleAuthTab(\'register\')">Register</div>', '<div class="auth-tab" id="tab-register" onclick="window.app.toggleAuthTab(\'register\')" data-i18n="auth.register_tab">Register</div>'),
    ('<h2 style="text-align: center; margin-bottom: 1.5rem; color: var(--secondary);">Create Account</h2>', '<h2 style="text-align: center; margin-bottom: 1.5rem; color: var(--secondary);" data-i18n="auth.create_account">Create Account</h2>'),
    ('<label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);">First Name</label>', '<label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);" data-i18n="auth.fname">First Name</label>'),
    ('<label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);">Last Name</label>', '<label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);" data-i18n="auth.lname">Last Name</label>'),
    ('<label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);">Email Address</label>', '<label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);" data-i18n="auth.email">Email Address</label>'),
    ('<label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);">Password</label>', '<label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);" data-i18n="auth.password">Password</label>'),
    ('<button type="submit" class="btn btn-success" style="width: 100%; padding: 1rem;">Register</button>', '<button type="submit" class="btn btn-success" style="width: 100%; padding: 1rem;" data-i18n="auth.register_btn">Register</button>'),
    
    ('<option value="cash">Cash on Arrival</option>', '<option value="cash" data-i18n="booking.cash">Cash on Arrival</option>'),
    ('<option value="card">Credit Card</option>', '<option value="card" data-i18n="booking.card">Credit Card</option>'),
    ('<option value="baridimob">BaridiMob</option>', '<option value="baridimob" data-i18n="booking.baridimob">BaridiMob</option>'),
    
    ("onclick=\"window.router.navigateTo('/destination/${b.destination_id}')\">View Destination</button>", "onclick=\"window.router.navigateTo('/destination/${b.destination_id}')\" data-i18n=\"dashboard.view_dest\">View Destination</button>"),
    
    ('<label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);">Company Name</label>', '<label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);" data-i18n="partner.company">Company Name</label>'),
    ('<label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);">Service Type</label>', '<label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);" data-i18n="partner.service_type">Service Type</label>'),
    ('<option value="accommodation">Hotel / Accommodation</option>', '<option value="accommodation" data-i18n="partner.type_hotel">Hotel / Accommodation</option>'),
    ('<option value="food">Restaurant / Cafe</option>', '<option value="food" data-i18n="partner.type_food">Restaurant / Cafe</option>'),
    ('<option value="transport">Transport Agency</option>', '<option value="transport" data-i18n="partner.type_transport">Transport Agency</option>'),
    ('<option value="guide">Tour Guide</option>', '<option value="guide" data-i18n="partner.type_guide">Tour Guide</option>'),
    ('<button type="submit" class="btn btn-primary" style="width: 100%; padding: 1rem; font-size: 1.2rem; box-shadow: 0 4px 15px rgba(46, 139, 87, 0.3);">Submit Application</button>', '<button type="submit" class="btn btn-primary" style="width: 100%; padding: 1rem; font-size: 1.2rem; box-shadow: 0 4px 15px rgba(46, 139, 87, 0.3);" data-i18n="partner.submit">Submit Application</button>'),
    
    ('<h3 style="margin-bottom: 1rem;">No favorites yet</h3>', '<h3 style="margin-bottom: 1rem;" data-i18n="favorites.empty_title">No favorites yet</h3>'),
    ('<p style="margin-bottom: 2rem;">Start exploring destinations and tap the heart icon to save them here.</p>', '<p style="margin-bottom: 2rem;" data-i18n="favorites.empty_desc">Start exploring destinations and tap the heart icon to save them here.</p>'),
    ('<button class="btn btn-primary" onclick="window.router.navigateTo(\'/\')">Explore Destinations</button>', '<button class="btn btn-primary" onclick="window.router.navigateTo(\'/\')" data-i18n="favorites.explore_btn">Explore Destinations</button>'),
    
    ('<h3 style="color: var(--primary); margin-bottom: 1.5rem;">Frequently Asked Questions</h3>', '<h3 style="color: var(--primary); margin-bottom: 1.5rem;" data-i18n="help.faq_title">Frequently Asked Questions</h3>'),
    ('<span>How do I cancel a booking?</span>', '<span data-i18n="help.faq_q1">How do I cancel a booking?</span>'),
    ('<div class="service-body" style="padding: 1rem; color: #555;">\n                                You can cancel a booking directly from your Dashboard up to 24 hours before the start date for a full refund.\n                            </div>', '<div class="service-body" style="padding: 1rem; color: #555;" data-i18n="help.faq_a1">\n                                You can cancel a booking directly from your Dashboard up to 24 hours before the start date for a full refund.\n                            </div>'),
    ('<span>What payment methods are supported?</span>', '<span data-i18n="help.faq_q2">What payment methods are supported?</span>'),
    ('<div class="service-body" style="padding: 1rem; color: #555;">\n                                We support Cash on Arrival, Credit Card, and BaridiMob for seamless local transactions.\n                            </div>', '<div class="service-body" style="padding: 1rem; color: #555;" data-i18n="help.faq_a2">\n                                We support Cash on Arrival, Credit Card, and BaridiMob for seamless local transactions.\n                            </div>'),
    ('<span>How do I contact an agency?</span>', '<span data-i18n="help.faq_q3">How do I contact an agency?</span>'),
    ('<div class="service-body" style="padding: 1rem; color: #555;">\n                                Once you book a service, the agency\'s contact information will be provided in your booking details.\n                            </div>', '<div class="service-body" style="padding: 1rem; color: #555;" data-i18n="help.faq_a3">\n                                Once you book a service, the agency\'s contact information will be provided in your booking details.\n                            </div>'),
    ('<h3 style="color: var(--primary); margin-bottom: 1.5rem;">Contact Us</h3>', '<h3 style="color: var(--primary); margin-bottom: 1.5rem;" data-i18n="help.contact_title">Contact Us</h3>'),
    ('<label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);">Your Message</label>', '<label style="display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary);" data-i18n="help.contact_label">Your Message</label>'),
    ('<button type="submit" class="btn btn-primary" style="padding: 1rem 2rem;">Send Message</button>', '<button type="submit" class="btn btn-primary" style="padding: 1rem 2rem;" data-i18n="help.contact_btn">Send Message</button>'),
    
    ('<h2 style="color: var(--secondary); margin-bottom: 1rem; font-size: 2.5rem;">Dalil Delivery</h2>', '<h2 style="color: var(--secondary); margin-bottom: 1rem; font-size: 2.5rem;" data-i18n="delivery.title">Dalil Delivery</h2>'),
    ('<p style="color: #555; margin-bottom: 2rem; font-size: 1.1rem;">Fast and reliable local delivery of food and essentials directly to your hotel or location.</p>', '<p style="color: #555; margin-bottom: 2rem; font-size: 1.1rem;" data-i18n="delivery.subtitle">Fast and reliable local delivery of food and essentials directly to your hotel or location.</p>'),
    ('<h3 style="color: var(--primary); margin-bottom: 1.5rem;">Coming Soon to Your Area</h3>', '<h3 style="color: var(--primary); margin-bottom: 1.5rem;" data-i18n="delivery.coming">Coming Soon to Your Area</h3>'),
    ('<p style="color: #666; margin-bottom: 2rem; line-height: 1.6;">We are currently partnering with top local restaurants and stores to bring Dalil Delivery to all major tourist destinations. Stay tuned for updates!</p>', '<p style="color: #666; margin-bottom: 2rem; line-height: 1.6;" data-i18n="delivery.desc">We are currently partnering with top local restaurants and stores to bring Dalil Delivery to all major tourist destinations. Stay tuned for updates!</p>'),
    ('<input type="email" placeholder="Enter email for updates" style="flex: 1; border: none; padding: 1rem 1.5rem; outline: none;">', '<input type="email" data-i18n="delivery.placeholder" placeholder="Enter email for updates" style="flex: 1; border: none; padding: 1rem 1.5rem; outline: none;">'),
    ("onclick=\"window.app.showToast('Subscribed to delivery updates!');\">Notify Me</button>", "onclick=\"window.app.showToast(window.i18n.t('toast.sub_success'), 'success');\" data-i18n=\"delivery.notify\">Notify Me</button>"),
    
    ('<h3 style="margin: 0; color: var(--secondary);">Explore Algeria</h3>', '<h3 style="margin: 0; color: var(--secondary);" data-i18n="map.explore">Explore Algeria</h3>'),
    
    ("onclick=\"window.router.navigateTo('/destination/${d.id}')\">View</button>", "onclick=\"window.router.navigateTo('/destination/${d.id}')\">${window.i18n.t('btn.view') || 'View'}</button>")
]

for old, new in replacements:
    content = content.replace(old, new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
