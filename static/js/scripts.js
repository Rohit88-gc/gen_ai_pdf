document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('question-form');
    if (form) {
        form.addEventListener('submit', function() {
            const button = form.querySelector('button');
            button.textContent = 'Asking...';
            button.disabled = true;
        });
    }
});