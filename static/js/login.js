document.addEventListener('DOMContentLoaded', function() {
    // Add loading effect to login button
    const loginForm = document.querySelector('form');
    const loginButton = document.querySelector('.btn-login');

    if (loginForm) {
        loginForm.addEventListener('submit', function() {
            loginButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Logging in...';
            loginButton.disabled = true;
        });
    }

    // Add animation to form fields
    const formControls = document.querySelectorAll('.form-control');
    formControls.forEach(control => {
        control.addEventListener('focus', function() {
            this.closest('.mb-3').classList.add('focused');
        });
        
        control.addEventListener('blur', function() {
            if (!this.value) {
                this.closest('.mb-3').classList.remove('focused');
            }
        });
    });

    // Add entrance animation
    const loginCard = document.querySelector('.login-card');
    setTimeout(() => {
        loginCard.style.opacity = '1';
        loginCard.style.transform = 'translateY(0)';
    }, 100);
});

// Add ripple effect to buttons
const buttons = document.querySelectorAll('.btn');
buttons.forEach(button => {
    button.addEventListener('click', function(e) {
        let ripple = document.createElement('div');
        ripple.classList.add('ripple');
        this.appendChild(ripple);
        
        let x = e.clientX - e.target.offsetLeft;
        let y = e.clientY - e.target.offsetTop;
        
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
});
