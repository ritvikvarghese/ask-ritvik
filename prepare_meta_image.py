#!/usr/bin/env python3
"""
Script to prepare the mosaic image for optimal social media sharing.
This will create the proper size and format for Open Graph images.
"""

from PIL import Image
import os

def create_meta_image():
    """
    Create optimized meta image for social media sharing.
    You'll need to save your mosaic image as 'mosaic-original.png' first.
    """
    
    # Check if mosaic image exists
    if not os.path.exists('mosaic-original.png'):
        print("❌ Please save your mosaic image as 'mosaic-original.png' first")
        print("   Then run this script to create the meta image")
        return
    
    try:
        # Open the original mosaic image
        original = Image.open('mosaic-original.png')
        
        # Create Open Graph image (1200x630 is the recommended size)
        og_width, og_height = 1200, 630
        
        # Resize the image to fit the Open Graph dimensions
        # We'll crop it to maintain aspect ratio
        original_ratio = original.width / original.height
        og_ratio = og_width / og_height
        
        if original_ratio > og_ratio:
            # Image is wider than needed, crop width
            new_width = int(original.height * og_ratio)
            left = (original.width - new_width) // 2
            cropped = original.crop((left, 0, left + new_width, original.height))
        else:
            # Image is taller than needed, crop height
            new_height = int(original.width / og_ratio)
            top = (original.height - new_height) // 2
            cropped = original.crop((0, top, original.width, top + new_height))
        
        # Resize to exact Open Graph dimensions
        meta_image = cropped.resize((og_width, og_height), Image.Resampling.LANCZOS)
        
        # Save the meta image
        meta_image.save('meta-image.png')
        print(f"✅ Created meta-image.png ({og_width}x{og_height})")
        
        # Also create a square version for other uses
        square_size = 512
        square_image = original.resize((square_size, square_size), Image.Resampling.LANCZOS)
        square_image.save('meta-image-square.png')
        print(f"✅ Created meta-image-square.png ({square_size}x{square_size})")
        
        print("\n🎉 Meta images created!")
        print("📁 Files created:")
        print("   - meta-image.png (1200x630) - for Open Graph/Twitter")
        print("   - meta-image-square.png (512x512) - for other uses")
        
        print("\n📝 Next steps:")
        print("1. Upload meta-image.png to your Railway deployment")
        print("2. Make sure it's accessible at https://ask.ritvik.io/meta-image.png")
        print("3. Test the social media preview using:")
        print("   - Facebook: https://developers.facebook.com/tools/debug/")
        print("   - Twitter: https://cards-dev.twitter.com/validator")
        print("   - LinkedIn: https://www.linkedin.com/post-inspector/")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure you have Pillow installed: pip install Pillow")

if __name__ == "__main__":
    create_meta_image()
