# AllCanLearn Sound Effects System

## Overview
Interactive sound effects added to make the website more engaging and fun! Sounds play on button clicks, navigation, and user interactions.

## Features Implemented

### 1. **Sound Effects Library** (`sounds.js`)
- ✅ Button click sounds
- ✅ Hover effects (subtle)
- ✅ Success notifications (3-tone melody)
- ✅ Error sounds
- ✅ Pop/drop effects
- ✅ Whoosh transitions
- ✅ Tab switch sounds
- ✅ Modal open/close
- ✅ Toggle switch sounds

### 2. **User Controls**
- **Sound Toggle Button** - Turn sounds on/off
- **Volume Control** - Adjustable (stored in localStorage)
- **Persistent Settings** - Remembers user preference

### 3. **Auto-Attach System**
Sounds automatically attach to:
- All `<button>` elements → click sound
- Navigation tabs → tab switch sound
- Dropdowns/accordions → pop sound
- Submit buttons → success sound (delayed)

## Files Created

1. **`sounds.js`** - Main sound effects class (Web Audio API)
2. **`generate-sounds.html`** - Preview/test all sounds
3. **`sound-styles.css`** - Sound toggle button styles
4. **`sound-functions.js`** - Toggle and preference functions
5. **`sound-toggle-html.txt`** - HTML snippet for toggle button

## Installation Steps

### Step 1: Add Sound Script to HTML
In your `index.html`, add before `</head>`:
```html
<!-- Sound Effects System -->
<script src="/static/assets/sounds/sounds.js"></script>
```

### Step 2: Add Sound Toggle CSS
In your `<style>` section, after `.theme-toggle:hover`, add:
```css
.sound-toggle {
    padding: 14px;
    background: rgba(26, 31, 58, 0.7);
    backdrop-filter: blur(20px);
    border: 2px solid rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-weight: 600;
    transition: all 0.3s;
    margin-bottom: 10px;
}

body.bright-mode .sound-toggle {
    background: rgba(255, 255, 255, 0.8);
    border-color: rgba(0, 0, 0, 0.15);
}

.sound-toggle:hover {
    transform: scale(1.02);
    border-color: #10b981;
}

.sound-toggle.disabled {
    opacity: 0.6;
}
```

### Step 3: Add Sound Toggle Button HTML
In your sidebar, BEFORE the `theme-toggle` div:
```html
<div class="sound-toggle" id="sound-toggle" onclick="toggleSound()">
    <span>Sounds</span>
    <span class="sound-icon" id="sound-icon">🔊</span>
</div>
```

### Step 4: Add Toggle Functions to JavaScript
In your `<script>` section, add:
```javascript
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

// Call after DOM loads
document.addEventListener('DOMContentLoaded', loadSoundPreference);
```

## Usage

### For Users
1. Click the **Sounds** toggle button in the sidebar
2. Icon shows 🔊 when ON, 🔇 when OFF
3. Setting persists across sessions

### For Developers

**Play sounds manually:**
```javascript
sounds.click();        // Button click
sounds.success();      // Success notification
sounds.error();        // Error sound
sounds.pop();          // Drop/pop effect
sounds.whoosh();       // Transition sound
sounds.notification(); // Notification ping
```

**Configure:**
```javascript
sounds.setVolume(0.5);     // Set volume (0.0 to 1.0)
sounds.setEnabled(false);   // Disable sounds
sounds.toggleEnabled();     // Toggle on/off
```

**Check status:**
```javascript
console.log(sounds.enabled);  // true/false
console.log(sounds.volume);   // 0.0 to 1.0
```

## Testing

Open `generate-sounds.html` in a browser to preview all sound effects:
```
http://localhost:8000/static/assets/sounds/generate-sounds.html
```

## Advanced Customization

### Adjust Specific Sounds
Edit `sounds.js` and modify the playTone parameters:
- **frequency**: Higher = higher pitch (Hz)
- **duration**: Length in seconds
- **type**: 'sine', 'square', 'sawtooth', 'triangle'
- **volume**: 0.0 to 1.0

Example:
```javascript
// Make click sound higher pitched and longer
click() {
    this.playTone(1000, 0.08, 'sine', this.volume * 0.7);
    setTimeout(() => this.playTone(800, 0.08, 'sine', this.volume * 0.5), 40);
}
```

### Add Custom Sounds
```javascript
// In sounds.js class, add new method:
celebration() {
    // Play ascending notes
    this.playTone(261.63, 0.1, 'sine', this.volume);
    setTimeout(() => this.playTone(329.63, 0.1, 'sine', this.volume), 100);
    setTimeout(() => this.playTone(392.00, 0.1, 'sine', this.volume), 200);
    setTimeout(() => this.playTone(523.25, 0.2, 'sine', this.volume), 300);
}
```

### Attach to Custom Elements
```javascript
// Add sound to specific element
document.getElementById('my-button').addEventListener('click', () => {
    sounds.whoosh();
});
```

## Browser Compatibility
- ✅ Chrome/Edge (Full support)
- ✅ Firefox (Full support)
- ✅ Safari (Full support)
- ✅ Mobile browsers (Requires user interaction first)

## Performance
- **Zero external files** - Uses Web Audio API
- **Tiny footprint** - ~4KB JavaScript
- **Instant playback** - No loading delays
- **No bandwidth usage** - Generated in browser

## Future Enhancements
- [ ] Volume slider control
- [ ] Individual sound preferences
- [ ] Custom sound themes
- [ ] Sound effect library expansion
- [ ] Haptic feedback on mobile

## Troubleshooting

**No sounds playing:**
1. Check browser console for errors
2. Verify sounds.enabled is true
3. Check browser tab isn't muted
4. Try clicking the page first (browser autoplay policy)

**Sounds too loud/quiet:**
```javascript
sounds.setVolume(0.2);  // Quieter (20%)
sounds.setVolume(0.8);  // Louder (80%)
```

**Remove hover sounds (if annoying):**
Comment out the hover event listeners in sounds.js:
```javascript
// document.querySelectorAll('button, a.btn, .card').forEach(element => {
//     element.addEventListener('mouseenter', () => sounds.hover());
// });
```

---

**Made with ❤️ for AllCanLearn**
