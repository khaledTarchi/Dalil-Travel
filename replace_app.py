import os

filepath = 'app/static/js/app.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ("this.showToast('Login successful!');", "this.showToast(window.i18n.t('toast.login_success'));"),
    ("this.showToast(\"Network error. Please try again.\", 'error');", "this.showToast(window.i18n.t('toast.net_error'), 'error');"),
    ("this.showToast('Registration successful! Please login.');", "this.showToast(window.i18n.t('toast.reg_success'));"),
    ("this.showToast('Booking completed successfully!');", "this.showToast(window.i18n.t('toast.book_success'));"),
    ("this.showToast('Booking failed: ' + res.error, 'error');", "this.showToast(window.i18n.t('toast.book_fail') + ' ' + res.error, 'error');"),
    ("this.showToast('Network error. Please try again.', 'error');", "this.showToast(window.i18n.t('toast.net_error'), 'error');"),
    ("container.innerHTML = '<div style=\"text-align: center;\"><i class=\"fa-solid fa-spinner fa-spin\" style=\"font-size: 2rem; color: var(--primary);\"></i><br>Generating Itinerary...</div>';", "container.innerHTML = '<div style=\"text-align: center;\"><i class=\"fa-solid fa-spinner fa-spin\" style=\"font-size: 2rem; color: var(--primary);\"></i><br>' + window.i18n.t('toast.ai_loading') + '</div>';"),
    ("container.innerText = 'Sorry, could not fetch itinerary at this time.';", "container.innerText = window.i18n.t('toast.ai_fail');"),
    ("container.innerText = 'Error connecting to AI service.';", "container.innerText = window.i18n.t('toast.ai_err');"),
    ("this.showToast('No destinations found matching your search.', 'error');", "this.showToast(window.i18n.t('toast.search_fail'), 'error');"),
    ("this.showToast('Error searching destinations.', 'error');", "this.showToast(window.i18n.t('toast.search_err'), 'error');"),
    ("this.showToast('Removed from favorites', 'success');", "this.showToast(window.i18n.t('toast.fav_remove'), 'success');"),
    ("this.showToast('Added to favorites', 'success');", "this.showToast(window.i18n.t('toast.fav_add'), 'success');"),
    (">Book Now</button>", ">${window.i18n.t('btn.book') || 'Book Now'}</button>")
]

for old, new in replacements:
    content = content.replace(old, new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# Update router.js alerts
filepath = 'app/static/js/router.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("alert(\"Please login first to book a service.\");", "window.app.showToast(window.i18n.t('toast.login_first'), 'error');")
content = content.replace("window.app.showToast('Application submitted successfully!');", "window.app.showToast(window.i18n.t('toast.apply_success'));")
content = content.replace("window.app.showToast('Message sent! We will reply soon.');", "window.app.showToast(window.i18n.t('toast.msg_sent'));")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
