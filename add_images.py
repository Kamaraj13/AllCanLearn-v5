#!/usr/bin/env python3
"""
Automatically extract images from zip file and add to slideshow.

Usage:
    python add_images.py images.zip
    python add_images.py  # Finds any .zip file in current directory
"""

import os
import sys
import zipfile
import shutil
from pathlib import Path

def find_zip_files(directory):
    """Find all zip files in directory"""
    return list(Path(directory).glob('*.zip'))

def extract_images(zip_path, assets_dir):
    """Extract image files from zip to assets directory"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'}
    extracted_count = 0
    
    print(f"📦 Opening {zip_path.name}...")
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        image_files = [f for f in file_list if Path(f).suffix.lower() in image_extensions]
        
        print(f"🖼️  Found {len(image_files)} images in zip file")
        
        for file in image_files:
            # Skip hidden files and __MACOSX folder
            if file.startswith('__MACOSX') or '/.DS_Store' in file or file.startswith('.'):
                continue
            
            # Get just the filename without path
            filename = Path(file).name
            
            # Skip if file already exists
            target_path = assets_dir / filename
            if target_path.exists():
                print(f"⏭️  Skipping {filename} (already exists)")
                continue
            
            try:
                # Extract to assets folder
                source = zip_ref.open(file)
                with open(target_path, 'wb') as target:
                    target.write(source.read())
                
                print(f"✅ Extracted: {filename}")
                extracted_count += 1
            except Exception as e:
                print(f"❌ Error extracting {filename}: {e}")
    
    return extracted_count

def main():
    """Main function"""
    # Get paths
    script_dir = Path(__file__).parent
    assets_dir = script_dir / 'app' / 'static' / 'assets'
    
    # Ensure assets directory exists
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    # Get zip file path
    if len(sys.argv) > 1:
        zip_path = Path(sys.argv[1])
        if not zip_path.exists():
            print(f"❌ Zip file not found: {zip_path}")
            return
    else:
        # Find any zip files in current directory
        zip_files = find_zip_files(script_dir)
        if not zip_files:
            print("❌ No zip files found in current directory")
            print("\nUsage:")
            print("  1. Copy your images.zip to AllCanLearn folder")
            print("  2. Run: python add_images.py")
            print("  OR: python add_images.py path/to/images.zip")
            return
        
        if len(zip_files) == 1:
            zip_path = zip_files[0]
        else:
            print("📦 Multiple zip files found:")
            for i, zf in enumerate(zip_files, 1):
                print(f"  {i}. {zf.name}")
            
            choice = input("\nWhich file to extract? (1-{}): ".format(len(zip_files)))
            try:
                zip_path = zip_files[int(choice) - 1]
            except (ValueError, IndexError):
                print("❌ Invalid choice")
                return
    
    print(f"\n🚀 Extracting images from: {zip_path.name}")
    print(f"📁 Target directory: {assets_dir}")
    print()
    
    # Extract images
    count = extract_images(zip_path, assets_dir)
    
    if count == 0:
        print("\n⚠️  No new images were extracted")
        return
    
    print(f"\n✨ Successfully extracted {count} new images!")
    
    # Ask if user wants to update slideshow
    response = input("\n🔄 Update slideshow now? (y/n): ").lower()
    if response == 'y':
        update_script = script_dir / 'update_slideshow.py'
        if update_script.exists():
            print("\n📝 Updating slideshow...")
            os.system(f'python "{update_script}"')
        else:
            print("⚠️  update_slideshow.py not found")
            print("💡 Refresh your browser to see the new images!")
    else:
        print("\n💡 Run 'python update_slideshow.py' later to update the slideshow")
    
    # Ask if user wants to delete the zip file
    response = input("\n🗑️  Delete zip file? (y/n): ").lower()
    if response == 'y':
        zip_path.unlink()
        print(f"✅ Deleted {zip_path.name}")
    
    print("\n🎉 Done! Your images are ready to use!")
    print(f"🌐 View at: http://localhost:8001/quiz")

if __name__ == '__main__':
    main()
