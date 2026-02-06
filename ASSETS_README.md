# 🎨 AllCanLearn Assets Guide

## Background Images for Slideshow

The animated slideshow background uses all images from `app/static/assets/` automatically!

### Current Images (20 backgrounds)
✅ Already included:
- `bg-frame-1.jpg` through `bg-frame-4.jpg`
- `download-2026-01-30T20:47:19-1.jpg` through `download-2026-01-30T20:47:19-4.jpg`
- `download-2026-01-30T20:50:02-1.jpg` through `download-2026-01-30T20:50:02-4.jpg`
- `download-2026-01-30T20:51:00-1.jpg` through `download-2026-01-30T20:51:00-4.jpg`
- `download-2026-01-30T20:51:31-1.jpg` through `download-2026-01-30T20:51:31-4.jpg`

### How to Add More Images

**Option 1: Drop & Play (Automatic)**
Simply copy new images into `app/static/assets/` and the slideshow will automatically include them!

```bash
# Copy images
cp ~/Downloads/my-image-*.jpg app/static/assets/

# Restart server to see changes
```

**Option 2: Organized Naming**
Use a consistent naming pattern for easy management:
- `bg-frame-*.jpg` - Main backgrounds
- `bg-tech-*.jpg` - Technology themed
- `bg-nature-*.jpg` - Nature themed
- `bg-education-*.jpg` - Learning themed

### Recommended Image Specs

- **Format**: JPG or PNG
- **Dimensions**: 1920x1080 or higher (16:9 ratio)
- **File Size**: Under 500KB each (compress for web performance)
- **Style**: High quality, vibrant, relevant to education/learning
- **Quantity**: 20-50 images recommended for variety

### Slideshow Timing

- **Total Duration**: 5 seconds per image × number of images
- Example: 20 images = 100 seconds full cycle
- Example: 50 images = 250 seconds (4+ minutes)

### Image Compression Tools

Before adding images, compress them for fast loading:
```bash
# Using ImageMagick
magick mogrify -resize 1920x1080 -quality 85 app/static/assets/*.jpg

# Using Python Pillow
pip install pillow
python -c "from PIL import Image; [Image.open(f'app/static/assets/{f}').save(f'app/static/assets/{f}', optimize=True, quality=85) for f in os.listdir('app/static/assets/') if f.endswith('.jpg')]"
```

### Testing Your Images

1. Add images to `app/static/assets/`
2. Refresh the page (Cmd+R)
3. Watch the slideshow cycle through all images
4. Adjust timing in CSS if needed (search for `@keyframes slideshow`)

### Current Slideshow Animation

The slideshow uses staggered animations where each image:
- Fades in over 2 seconds
- Stays visible for 3 seconds  
- Fades out over 2 seconds
- Next image starts before previous ends (smooth transition)

### Performance Notes

- Browser caches images after first load
- Lazy loading not needed (background only)
- More images = longer cycle time (but won't slow down page)
- Keep total assets under 10MB for fast initial load

---

**Quick Test**: After adding images, open http://localhost:8001/quiz and watch the background!
