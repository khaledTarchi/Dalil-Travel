// Main JS Logic for MVP

document.addEventListener('DOMContentLoaded', () => {
    
    // --- MOBILE NAVIGATION ---
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileNav = document.getElementById('mobileNav');
    if (mobileMenuBtn && mobileNav) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileNav.classList.toggle('active');
            // Toggle icon between bars and times
            const icon = mobileMenuBtn.querySelector('i');
            if (icon.classList.contains('fa-bars')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }

    // --- MAP LOGIC (Home Page) ---
    const mapElement = document.getElementById('map');
    if (mapElement && typeof L !== 'undefined') {
        // Initialize Leaflet map (centered on Algeria)
        const map = L.map('map').setView([28.0339, 1.6596], 5);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors',
            maxZoom: 18,
        }).addTo(map);

        // Define a custom icon matching the desert aesthetic
        const desertIcon = L.divIcon({
            className: 'custom-map-icon',
            html: '<div style="background-color: var(--primary); width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>',
            iconSize: [20, 20],
            iconAnchor: [10, 10]
        });

        // Add some mock markers
        const locations = [
            { name: "Tassili N'Ajjer", coords: [25.5, 8.5], link: "/explore?region=Tassili" },
            { name: "Brezina", coords: [33.098, 1.261], link: "/explore?region=Brezina" },
            { name: "Timimoun", coords: [29.263, 0.230], link: "/explore?region=Timimoun" }
        ];

        locations.forEach(loc => {
            L.marker(loc.coords, {icon: desertIcon}).addTo(map)
                .bindPopup(`<b>${loc.name}</b><br><a href="${loc.link}">Explore</a>`);
        });
    }

    // --- PROPERTY PRICING & MEALS (Property Page) ---
    const basePriceEl = document.getElementById('base-price');
    const totalPriceEl = document.getElementById('total-price');
    const mealCheckboxes = document.querySelectorAll('.meal-checkbox');
    const numNightsInput = document.getElementById('num-nights');

    function calculateTotal() {
        if (!basePriceEl || !totalPriceEl || !numNightsInput) return;
        
        let basePrice = parseFloat(basePriceEl.dataset.price);
        let nights = parseInt(numNightsInput.value) || 1;
        
        let totalMealsPrice = 0;
        mealCheckboxes.forEach(cb => {
            if (cb.checked) {
                totalMealsPrice += parseFloat(cb.dataset.price);
            }
        });

        // Total = (Base Price * Nights) + (Total Meals Price * Nights)
        // Adjust formula based on whether meals are per night or per stay. Let's do per night for simplicity.
        let grandTotal = (basePrice + totalMealsPrice) * nights;
        
        totalPriceEl.textContent = grandTotal.toLocaleString() + ' DZD';
        
        // Update hidden input for form submission if it exists
        const hiddenTotal = document.getElementById('hidden-total-amount');
        if (hiddenTotal) hiddenTotal.value = grandTotal;
    }

    if (mealCheckboxes.length > 0 || numNightsInput) {
        mealCheckboxes.forEach(cb => cb.addEventListener('change', calculateTotal));
        if (numNightsInput) numNightsInput.addEventListener('input', calculateTotal);
        // Initial calc
        calculateTotal();
    }

    // --- PAYMENT MOCKUP MODAL (Property Page) ---
    const bookNowBtn = document.getElementById('book-now-btn');
    const paymentModal = document.getElementById('payment-modal-overlay');
    const closePaymentModal = document.getElementById('close-payment-modal');
    const mockPayBtn = document.getElementById('mock-pay-btn');
    const successMsg = document.getElementById('payment-success-msg');
    const paymentFormInner = document.getElementById('payment-form-inner');

    if (bookNowBtn && paymentModal) {
        bookNowBtn.addEventListener('click', (e) => {
            e.preventDefault();
            paymentModal.classList.add('active');
        });
    }

    if (closePaymentModal) {
        closePaymentModal.addEventListener('click', () => {
            paymentModal.classList.remove('active');
        });
    }

    if (mockPayBtn) {
        mockPayBtn.addEventListener('click', (e) => {
            e.preventDefault();
            // Simulate processing
            mockPayBtn.textContent = "Processing...";
            mockPayBtn.disabled = true;
            
            setTimeout(() => {
                if(paymentFormInner) paymentFormInner.style.display = 'none';
                if(successMsg) successMsg.style.display = 'block';
                
                // Submit actual form after short delay
                setTimeout(() => {
                    const bookingForm = document.getElementById('booking-form');
                    if (bookingForm) bookingForm.submit();
                }, 1500);
            }, 1000);
        });
    }

});
