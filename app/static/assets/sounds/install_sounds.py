#!/usr/bin/env python3
"""
AllCanLearn Sound Effects Installer
Automatically adds sound effects system to index.html
"""

import re
import shutil
from pathlib import Path

def backup_file(file_path):
    """Create a backup of the original file"""
    backup_path = f"{file_path}.sound_backup"
    shutil.copy(file_path, backup_path)
    print(f"✅ Backup created: {backup_path}")
    return backup_path

def add_sound_script(content):
    """Add sound effects script before </head>"""
    sound_script = '''    <!-- Sound Effects System -->
    <script src="/static/assets/sounds/sounds.js"></script>
'''
    if 'sounds.js' in content:
        print("⚠️  Sound script already added")
        return content
    
    content = content.replace('</head>', f'{sound_script}</head>')
    print("✅ Added sound script reference")
    return content

def add_sound_css(content):
    """Add sound toggle CSS after theme-toggle styles"""
    sound_css = '''
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
    
    if 'sound-toggle {' in content:
        print("⚠️  Sound CSS already added")
        return content
    
    # Find .theme-toggle:hover and add after it
    pattern = r'(\.theme-toggle:hover\s*{[^}]+})'
    content = re.sub(pattern, r'\1' + sound_css, content)
    print("✅ Added sound toggle CSS")
    return content

def add_sound_toggle_html(content):
    """Add sound toggle button before theme toggle"""
    sound_html = '''            <div class="sound-toggle" id="sound-toggle" onclick="toggleSound()">
                <span>Sounds</span>
                <span class="sound-icon" id="sound-icon">🔊</span>
            </div>
            
'''
    
    if 'sound-toggle' in content:
        print("⚠️  Sound toggle button already added")
        return content
    
    # Find theme-toggle and add sound toggle before it
    pattern = r'(\s+<div class="theme-toggle")'
    content = re.sub(pattern, sound_html + r'\1', content)
    print("✅ Added sound toggle button")
    return content

def add_sound_functions(content):
    """Add toggleSound and loadSoundPreference functions"""
    sound_functions = '''
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

'''
    
    if 'function toggleSound()' in content:
        print("⚠️  Sound functions already added")
        return content
    
    # Find function toggleTheme and add before it
    pattern = r'(\s+function toggleTheme\(\))'
    content = re.sub(pattern, sound_functions + r'\1', content)
    print("✅ Added sound toggle functions")
    return content

def add_sound_loader(content):
    """Add loadSoundPreference call to DOMContentLoaded"""
    # Check if there's already a DOMContentLoaded with loadTheme
    if "addEventListener('DOMContentLoaded'" in content:
        # Add loadSoundPreference call
        pattern = r"(document\.addEventListener\('DOMContentLoaded',\s*\(\)\s*=>\s*{[^}]*loadTheme\(\);)"
        if re.search(pattern, content):
            content = re.sub(pattern, r'\1\n            loadSoundPreference();', content)
            print("✅ Added loadSoundPreference to existing DOMContentLoaded")
    else:
        # Add new DOMContentLoaded listener before </script>
        loader_code = '''
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', () => {
            loadTheme();
            loadSoundPreference();
        });
'''
        content = content.replace('</script>', loader_code + '\n</script>')
        print("✅ Added DOMContentLoaded listener with sound loader")
    
    return content

def main():
    print("🎵 AllCanLearn Sound Effects Installer\n")
    
    # Get the index.html path
    html_path = Path(__file__).parent.parent / 'index.html'
    
    if not html_path.exists():
        print(f"❌ Error: {html_path} not found")
        return
    
    print(f"📄 Processing: {html_path}\n")
    
    # Backup original file
    backup_file(html_path)
    
    # Read content
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply all modifications
    content = add_sound_script(content)
    content = add_sound_css(content)
    content = add_sound_toggle_html(content)
    content = add_sound_functions(content)
    content = add_sound_loader(content)
    
    # Write modified content
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✨ Sound effects system installed successfully!")
    print("\n📝 Next steps:")
    print("1. Restart your AllCanLearn server")
    print("2. Open the website and click the 'Sounds 🔊' button in sidebar")
    print("3. Test sounds by clicking buttons!")
    print("\n🎧 Test sounds at: /static/assets/sounds/generate-sounds.html")

if __name__ == '__main__':
    main()
