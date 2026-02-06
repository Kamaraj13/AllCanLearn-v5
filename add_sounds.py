#!/usr/bin/env python3
import re
import shutil

html_file = 'app/static/index.html'

# Backup
shutil.copy(html_file, f'{html_file}.sound_backup')
print('Backup created')

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add script before </head>
if 'sounds.js' not in content:
    content = content.replace('</head>', '    <script src="/static/assets/sounds/sounds.js"></script>\n</head>')
    print('Added sound script')

# 2. Add CSS
if 'sound-toggle {' not in content:
    css = '''
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
'''
    pattern = r'(\.theme-toggle:hover\s*{[^}]+})'
    content = re.sub(pattern, r'\1' + css, content)
    print('Added CSS')

# 3. Add HTML button
if 'id="sound-toggle"' not in content:
    button_html = '''            <div class="sound-toggle" id="sound-toggle" onclick="toggleSound()">
                <span>Sounds</span>
                <span class="sound-icon" id="sound-icon">🔊</span>
            </div>
            
'''
    pattern = r'(\s+<div class="theme-toggle")'
    content = re.sub(pattern, button_html + r'\1', content)
    print('Added toggle button')

# 4. Add JavaScript functions
if 'function toggleSound()' not in content:
    js_functions = '''
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
        
        function loadSoundPreference() {
            const soundIcon = document.getElementById('sound-icon');
            const soundToggle = document.getElementById('sound-toggle');
            if (!sounds.enabled) {
                soundIcon.textContent = '🔇';
                soundToggle.classList.add('disabled');
            }
        }

'''
    pattern = r'(\s+function toggleTheme\(\))'
    content = re.sub(pattern, js_functions + r'\1', content)
    print('Added toggle functions')

# 5. Call loadSoundPreference
if 'loadSoundPreference()' not in content:
    pattern = r"(loadTheme\(\);)"
    content = re.sub(pattern, r'\1\n            loadSoundPreference();', content)
    print('Added sound loader call')

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print('\n✨ Sound effects installed! Restart server and test.')
