// AllCanLearn Sound Effects System
// Uses Web Audio API - no external files needed

class SoundEffects {
    constructor() {
        this.audioContext = null;
        this.enabled = localStorage.getItem('soundsEnabled') !== 'false';
        this.volume = parseFloat(localStorage.getItem('soundVolume') || '0.3');
        this.initAudioContext();
    }

    initAudioContext() {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
    }

    playTone(frequency, duration, type = 'sine', volume = null) {
        if (!this.enabled) return;
        
        const vol = volume !== null ? volume : this.volume;
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.frequency.value = frequency;
        oscillator.type = type;
        
        gainNode.gain.setValueAtTime(vol, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + duration);
    }

    // Button click sound - Soft water drop
    click() {
        if (!this.enabled) return;
        
        const osc = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        const filter = this.audioContext.createBiquadFilter();
        
        osc.connect(filter);
        filter.connect(gain);
        gain.connect(this.audioContext.destination);
        
        osc.type = 'sine';
        osc.frequency.setValueAtTime(1200, this.audioContext.currentTime);
        osc.frequency.exponentialRampToValueAtTime(600, this.audioContext.currentTime + 0.1);
        
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(2000, this.audioContext.currentTime);
        filter.Q.setValueAtTime(10, this.audioContext.currentTime);
        
        gain.gain.setValueAtTime(this.volume * 0.3, this.audioContext.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.15);
        
        osc.start(this.audioContext.currentTime);
        osc.stop(this.audioContext.currentTime + 0.15);
    }

    // Hover sound - Gentle chime
    hover() {
        if (!this.enabled) return;
        
        const osc1 = this.audioContext.createOscillator();
        const osc2 = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        
        osc1.connect(gain);
        osc2.connect(gain);
        gain.connect(this.audioContext.destination);
        
        osc1.frequency.value = 1760; // A6
        osc2.frequency.value = 2637; // E7 (fifth)
        osc1.type = 'sine';
        osc2.type = 'sine';
        
        gain.gain.setValueAtTime(this.volume * 0.15, this.audioContext.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.2);
        
        osc1.start(this.audioContext.currentTime);
        osc2.start(this.audioContext.currentTime);
        osc1.stop(this.audioContext.currentTime + 0.2);
        osc2.stop(this.audioContext.currentTime + 0.2);
    }

    // Success notification - Wind chimes cascade
    success() {
        if (!this.enabled) return;
        
        const notes = [523.25, 659.25, 783.99, 987.77]; // C-E-G-B
        notes.forEach((freq, i) => {
            setTimeout(() => {
                const osc = this.audioContext.createOscillator();
                const gain = this.audioContext.createGain();
                const filter = this.audioContext.createBiquadFilter();
                
                osc.connect(filter);
                filter.connect(gain);
                gain.connect(this.audioContext.destination);
                
                osc.frequency.value = freq;
                osc.type = 'sine';
                
                filter.type = 'lowpass';
                filter.frequency.value = 3000;
                filter.Q.value = 5;
                
                gain.gain.setValueAtTime(this.volume * 0.25, this.audioContext.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.4);
                
                osc.start(this.audioContext.currentTime);
                osc.stop(this.audioContext.currentTime + 0.4);
            }, i * 80);
        });
    }

    // Error sound - Soft descending tone
    error() {
        if (!this.enabled) return;
        
        const osc = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        const filter = this.audioContext.createBiquadFilter();
        
        osc.connect(filter);
        filter.connect(gain);
        gain.connect(this.audioContext.destination);
        
        osc.type = 'sine';
        osc.frequency.setValueAtTime(400, this.audioContext.currentTime);
        osc.frequency.exponentialRampToValueAtTime(200, this.audioContext.currentTime + 0.3);
        
        filter.type = 'lowpass';
        filter.frequency.value = 800;
        
        gain.gain.setValueAtTime(this.volume * 0.25, this.audioContext.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);
        
        osc.start(this.audioContext.currentTime);
        osc.stop(this.audioContext.currentTime + 0.3);
    }

    // Notification ping - Soft bell
    notification() {
        if (!this.enabled) return;
        
        const frequencies = [880, 1320, 1760]; // Harmonic series
        frequencies.forEach((freq, i) => {
            const osc = this.audioContext.createOscillator();
            const gain = this.audioContext.createGain();
            
            osc.connect(gain);
            gain.connect(this.audioContext.destination);
            
            osc.frequency.value = freq;
            osc.type = 'sine';
            
            const vol = this.volume * 0.2 * (1 - i * 0.3);
            gain.gain.setValueAtTime(vol, this.audioContext.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.5);
            
            osc.start(this.audioContext.currentTime);
            osc.stop(this.audioContext.currentTime + 0.5);
        });
    }

    // Toggle switch - Soft tick
    toggle() {
        if (!this.enabled) return;
        
        const osc = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        const filter = this.audioContext.createBiquadFilter();
        
        osc.connect(filter);
        filter.connect(gain);
        gain.connect(this.audioContext.destination);
        
        osc.type = 'sine';
        osc.frequency.value = 800;
        
        filter.type = 'bandpass';
        filter.frequency.value = 1000;
        filter.Q.value = 20;
        
        gain.gain.setValueAtTime(this.volume * 0.2, this.audioContext.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.05);
        
        osc.start(this.audioContext.currentTime);
        osc.stop(this.audioContext.currentTime + 0.05);
    }

    // Pop/drop sound - Raindrop
    pop() {
        if (!this.enabled) return;
        
        const osc = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        const filter = this.audioContext.createBiquadFilter();
        
        osc.connect(filter);
        filter.connect(gain);
        gain.connect(this.audioContext.destination);
        
        osc.type = 'sine';
        osc.frequency.setValueAtTime(1800, this.audioContext.currentTime);
        osc.frequency.exponentialRampToValueAtTime(400, this.audioContext.currentTime + 0.08);
        
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(3000, this.audioContext.currentTime);
        filter.frequency.exponentialRampToValueAtTime(800, this.audioContext.currentTime + 0.08);
        filter.Q.value = 8;
        
        gain.gain.setValueAtTime(this.volume * 0.4, this.audioContext.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.12);
        
        osc.start(this.audioContext.currentTime);
        osc.stop(this.audioContext.currentTime + 0.12);
    }

    // Whoosh sound - Gentle breeze
    whoosh() {
        if (!this.enabled) return;
        
        // Create noise buffer
        const bufferSize = this.audioContext.sampleRate * 0.3;
        const buffer = this.audioContext.createBuffer(1, bufferSize, this.audioContext.sampleRate);
        const data = buffer.getChannelData(0);
        
        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }
        
        const noise = this.audioContext.createBufferSource();
        const filter = this.audioContext.createBiquadFilter();
        const gain = this.audioContext.createGain();
        
        noise.buffer = buffer;
        noise.connect(filter);
        filter.connect(gain);
        gain.connect(this.audioContext.destination);
        
        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(2000, this.audioContext.currentTime);
        filter.frequency.exponentialRampToValueAtTime(400, this.audioContext.currentTime + 0.3);
        filter.Q.value = 2;
        
        gain.gain.setValueAtTime(this.volume * 0.15, this.audioContext.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);
        
        noise.start(this.audioContext.currentTime);
        noise.stop(this.audioContext.currentTime + 0.3);
    }

    // Tab switch - Soft marimba
    tabSwitch() {
        if (!this.enabled) return;
        
        const osc = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        const filter = this.audioContext.createBiquadFilter();
        
        osc.connect(filter);
        filter.connect(gain);
        gain.connect(this.audioContext.destination);
        
        osc.type = 'sine';
        osc.frequency.value = 880;
        
        filter.type = 'lowpass';
        filter.frequency.value = 2000;
        filter.Q.value = 3;
        
        gain.gain.setValueAtTime(this.volume * 0.25, this.audioContext.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.2);
        
        osc.start(this.audioContext.currentTime);
        osc.stop(this.audioContext.currentTime + 0.2);
    }

    // Modal open - Ascending sparkle
    modalOpen() {
        if (!this.enabled) return;
        
        const notes = [523, 659, 784]; // C-E-G chord
        notes.forEach((freq, i) => {
            setTimeout(() => {
                const osc = this.audioContext.createOscillator();
                const gain = this.audioContext.createGain();
                
                osc.connect(gain);
                gain.connect(this.audioContext.destination);
                
                osc.frequency.value = freq;
                osc.type = 'sine';
                
                gain.gain.setValueAtTime(this.volume * 0.2, this.audioContext.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);
                
                osc.start(this.audioContext.currentTime);
                osc.stop(this.audioContext.currentTime + 0.3);
            }, i * 40);
        });
    }

    // Modal close - Descending sparkle
    modalClose() {
        if (!this.enabled) return;
        
        const notes = [784, 659, 523]; // G-E-C chord (reversed)
        notes.forEach((freq, i) => {
            setTimeout(() => {
                const osc = this.audioContext.createOscillator();
                const gain = this.audioContext.createGain();
                
                osc.connect(gain);
                gain.connect(this.audioContext.destination);
                
                osc.frequency.value = freq;
                osc.type = 'sine';
                
                gain.gain.setValueAtTime(this.volume * 0.2, this.audioContext.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);
                
                osc.start(this.audioContext.currentTime);
                osc.stop(this.audioContext.currentTime + 0.3);
            }, i * 40);
        });
    }

    // Enable/disable sounds
    setEnabled(enabled) {
        this.enabled = enabled;
        localStorage.setItem('soundsEnabled', enabled);
        if (enabled) {
            this.click(); // Play confirmation sound
        }
    }

    // Set volume (0.0 to 1.0)
    setVolume(volume) {
        this.volume = Math.max(0, Math.min(1, volume));
        localStorage.setItem('soundVolume', this.volume);
    }

    // Toggle sounds on/off
    toggleEnabled() {
        this.setEnabled(!this.enabled);
        return this.enabled;
    }
}

// Initialize global sound effects instance
const sounds = new SoundEffects();

// Auto-attach click sounds to common elements when DOM loads
document.addEventListener('DOMContentLoaded', () => {
    // Add click sounds to all buttons
    document.querySelectorAll('button').forEach(button => {
        button.addEventListener('click', () => sounds.click());
    });

    // Add hover sounds to interactive elements (optional - can be removed if annoying)
    // document.querySelectorAll('button, a.btn, .card').forEach(element => {
    //     element.addEventListener('mouseenter', () => sounds.hover());
    // });

    // Add sounds to navigation tabs
    document.querySelectorAll('.nav-btn, .tab-btn').forEach(tab => {
        tab.addEventListener('click', () => sounds.tabSwitch());
    });

    // Add pop sound to dropdown/accordion elements
    document.querySelectorAll('select, details, .dropdown').forEach(element => {
        element.addEventListener('click', () => sounds.pop());
    });

    // Add success sound to submit buttons
    document.querySelectorAll('button[type="submit"], .submit-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            // Play success sound after a short delay (simulating successful action)
            setTimeout(() => sounds.success(), 500);
        });
    });
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SoundEffects;
}
