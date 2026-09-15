document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star');
    const ratingInput = document.getElementById('ratingValue');
    const ratingText = document.getElementById('ratingText');
    const form = document.getElementById('feedbackForm');

    let currentRating = 0;

    // Highlight stars on hover
    stars.forEach(star => {
        star.addEventListener('mouseover', function() {
            const value = parseInt(this.getAttribute('data-value'));
            highlightStars(value);
        });

        // Reset to selected rating when mouse leaves
        star.addEventListener('mouseout', function() {
            highlightStars(currentRating);
        });

        // Set rating on click
        star.addEventListener('click', function() {
            currentRating = parseInt(this.getAttribute('data-value'));
            ratingInput.value = currentRating;
            ratingText.textContent = `You selected ${currentRating} out of 5 stars`;
            highlightStars(currentRating);
        });
    });

    function highlightStars(count) {
        stars.forEach(star => {
            const value = parseInt(star.getAttribute('data-value'));
            if (value <= count) {
                star.classList.add('active');
            } else {
                star.classList.remove('active');
            }
        });
    }

    // Form validation before submit
    form.addEventListener('submit', function(e) {
        if (currentRating === 0) {
            e.preventDefault();
            ratingText.textContent = "Please select a rating before submitting.";
            ratingText.style.color = "red";
        }
    });
});