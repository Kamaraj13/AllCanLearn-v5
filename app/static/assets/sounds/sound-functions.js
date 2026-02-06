// Sound Toggle Functions - Add to your main JavaScript

// Toggle sound effects
function toggleSound() {
    const enabled = sounds.toggleEnabled();
    const soundIcon = document.getElementById('sound-icon');
    const soundToggle = document.getElementById('sound-toggle');
    
    if (enabled) {
        soundIcon.textContent = '🔊';
        soundToggle.classList.remove('disabled');
    } else {
        soundIcon.textContent = '🔇';
        soundToggle.classList.add('disabled');
    }
}

// Load sound preference on page load
function loadSoundPreference() {
    const soundIcon = document.getElementById('sound-icon');
    const soundToggle = document.getElementById('sound-toggle');
    
    if (!sounds.enabled) {
        soundIcon.textContent = '🔇';
        soundToggle.classList.add('disabled');
    }
}

// Call this after DOM loads
document.addEventListener('DOMContentLoaded', loadSoundPreference);
