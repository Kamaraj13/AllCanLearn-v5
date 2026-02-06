#!/usr/bin/env python3
"""
Auto-generate slideshow background HTML for all images in assets folder.
Run this script after adding new images to automatically update quiz.html
"""

import os
import re
from pathlib import Path

def get_image_files(assets_dir):
    """Get all image files from assets directory, excluding logos"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    exclude_patterns = ['logo', 'icon', 'favicon']
    
    image_files = []
    for file in sorted(os.listdir(assets_dir)):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            # Skip logo files
            if not any(pattern in file.lower() for pattern in exclude_patterns):
                image_files.append(file)
    
    return image_files

def generate_slideshow_html(image_files):
    """Generate HTML for slideshow background"""
    html_lines = ['    <div class="slideshow-background">']
    
    for i, image in enumerate(image_files, 1):
        html_lines.append(f'        <img src="/static/assets/{image}" alt="Background {i}">')
    
    html_lines.append('    </div>')
    return '\n'.join(html_lines)

def calculate_keyframe_css(num_images):
    """Generate CSS keyframes for slideshow animation"""
    if num_images == 0:
        return ""
    
    # Each image shows for 5 seconds
    fade_duration = 2  # seconds for fade in/out
    visible_duration = 3  # seconds fully visible
    total_per_image = fade_duration + visible_duration
    
    total_duration = num_images * total_per_image
    
    css_lines = ['        @keyframes slideshow {']
    
    for i in range(num_images):
        delay = i * total_per_image
        
        # Start (invisible)
        start_percent = (delay / total_duration) * 100
        css_lines.append(f'            {start_percent:.1f}% {{ opacity: 0; }}')
        
        # Fade in complete
        fade_in_percent = ((delay + fade_duration) / total_duration) * 100
        css_lines.append(f'            {fade_in_percent:.1f}% {{ opacity: 1; }}')
        
        # Start fade out
        fade_out_start = ((delay + fade_duration + visible_duration) / total_duration) * 100
        css_lines.append(f'            {fade_out_start:.1f}% {{ opacity: 1; }}')
        
        # Fade out complete
        fade_out_end = ((delay + total_per_image) / total_duration) * 100
        if fade_out_end < 100:
            css_lines.append(f'            {fade_out_end:.1f}% {{ opacity: 0; }}')
    
    css_lines.append('            100% { opacity: 0; }')
    css_lines.append('        }')
    
    return '\n'.join(css_lines)

def update_quiz_html(quiz_file, image_files):
    """Update quiz.html with new slideshow HTML"""
    with open(quiz_file, 'r') as f:
        content = f.read()
    
    # Generate new slideshow HTML
    new_slideshow = generate_slideshow_html(image_files)
    
    # Replace slideshow section
    pattern = r'(<div class="slideshow-background">)(.*?)(</div>)'
    replacement = new_slideshow
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Update animation duration in CSS
        num_images = len(image_files)
        total_duration = num_images * 5  # 5 seconds per image
        
        # Update animation duration
        content = re.sub(
            r'animation: slideshow \d+s infinite;',
            f'animation: slideshow {total_duration}s infinite;',
            content
        )
        
        # Update animation delays for staggered effect
        delay_pattern = r'\.slideshow-background img:nth-child\(\d+\) \{[^}]*\}'
        content = re.sub(delay_pattern, '', content)
        
        # Add new staggered delays
        delay_css = []
        for i in range(1, num_images + 1):
            delay = (i - 1) * 5
            delay_css.append(f'        .slideshow-background img:nth-child({i}) {{ animation-delay: {delay}s; }}')
        
        # Insert delays before closing style tag
        style_close = content.rfind('</style>')
        if style_close != -1:
            content = content[:style_close] + '\n        \n' + '\n'.join(delay_css) + '\n' + content[style_close:]
        
        with open(quiz_file, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated quiz.html with {num_images} background images")
        print(f"📊 Total slideshow duration: {total_duration} seconds ({total_duration/60:.1f} minutes)")
        return True
    else:
        print("❌ Could not find slideshow section in quiz.html")
        return False

def main():
    """Main function"""
    # Get paths
    script_dir = Path(__file__).parent
    assets_dir = script_dir / 'app' / 'static' / 'assets'
    quiz_file = script_dir / 'app' / 'static' / 'quiz.html'
    
    if not assets_dir.exists():
        print(f"❌ Assets directory not found: {assets_dir}")
        return
    
    if not quiz_file.exists():
        print(f"❌ Quiz file not found: {quiz_file}")
        return
    
    # Get all image files
    image_files = get_image_files(assets_dir)
    
    if not image_files:
        print("⚠️ No background images found in assets folder")
        return
    
    print(f"🎨 Found {len(image_files)} background images:")
    for img in image_files[:5]:
        print(f"   - {img}")
    if len(image_files) > 5:
        print(f"   ... and {len(image_files) - 5} more")
    
    # Update quiz.html
    success = update_quiz_html(quiz_file, image_files)
    
    if success:
        print("\n✨ Done! Refresh your browser to see the updated slideshow")
        print(f"🌐 http://localhost:8001/quiz")

if __name__ == '__main__':
    main()
