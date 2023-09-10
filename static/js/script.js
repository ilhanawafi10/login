const wrapper = document.querySelector('.wrapper');
const registerLink = document.querySelector('.register-link');
const loginLink = document.querySelector('.login-link');

registerLink.onclick = () => {
    wrapper.classList.add('active');
}

loginLink.onclick = () => {
    wrapper.classList.remove('active');
}
const notification = document.getElementById('notification');
        const notificationMessage = document.getElementById('notificationMessage');
        const notificationClose = document.getElementById('notificationClose');
    
        function showNotification(message) {
            notificationMessage.textContent = message;
            notification.classList.add('active');
        }
    
        notificationClose.addEventListener('click', function() {
            notification.classList.remove('active');
        });
    
        const signupForm = document.querySelector('.form-box.register form');
    
        signupForm.addEventListener('submit', function(event) {
            const passwordInput = signupForm.querySelector('input[name="password"]');
            if (passwordInput.value.length < 8) {
                event.preventDefault();
                showNotification('Password minimal harus terdiri dari 8 karakter');
            } else if (!/^(?=.*[a-zA-Z])(?=.*\d).+$/.test(passwordValue)) {
                event.preventDefault();
                showNotification('Password harus terdiri dari huruf dan angka');
            }
        });


// toogle icon navbar
let menuIcon = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menuIcon.onclick = () => {
    menuIcon.classList.toggle('bx-x');
    navbar.classList.toggle('active');
}


// End Login & Register
