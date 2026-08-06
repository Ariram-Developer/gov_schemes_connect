// app/static/js/main.js

document.addEventListener('DOMContentLoaded', () => {
    // Light/Dark Mode Toggle Logic
    const themeToggleBtn = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    // Apply the saved theme on load
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateButtonText(currentTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            let theme = document.documentElement.getAttribute('data-theme');
            let switchToTheme = theme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', switchToTheme);
            localStorage.setItem('theme', switchToTheme);
            updateButtonText(switchToTheme);
        });
    }

    function updateButtonText(theme) {
        if (themeToggleBtn) {
            themeToggleBtn.innerText = theme === 'dark' ? '☀️ Light Mode' : '🌙 Dark Mode';
        }
    }
});