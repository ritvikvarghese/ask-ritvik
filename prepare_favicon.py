#!/usr/bin/env python3
"""
Script to help prepare the robot image for favicon use.
This will create multiple sizes needed for different devices.
"""

from PIL import Image
import os

def create_favicon_sizes():
    """
    Create multiple favicon sizes from the robot image.
    You'll need to save your robot image as 'robot-original.png' first.
    """
    
    # Check if robot image exists
    if not os.path.exists('robot-original.png'):
        print("❌ Please save your robot image as 'robot-original.png' first")
        print("   Then run this script to create favicon sizes")
        return
    
    try:
        # Open the original robot image
        original = Image.open('robot-original.png')
        
        # Create different favicon sizes
        sizes = [
            (16, 16, 'favicon-16x16.png'),
            (32, 32, 'favicon-32x32.png'),
            (64, 64, 'favicon-64x64.png'),
            (180, 180, 'apple-touch-icon.png'),
            (192, 192, 'android-chrome-192x192.png'),
            (512, 512, 'android-chrome-512x512.png')
        ]
        
        for width, height, filename in sizes:
            # Resize the image
            resized = original.resize((width, height), Image.Resampling.LANCZOS)
            
            # Save the resized image
            resized.save(filename)
            print(f"✅ Created {filename} ({width}x{height})")
        
        # Create ICO file for maximum compatibility
        ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
        ico_images = []
        
        for size in ico_sizes:
            resized = original.resize(size, Image.Resampling.LANCZOS)
            ico_images.append(resized)
        
        # Save as ICO file
        ico_images[0].save('favicon.ico', format='ICO', sizes=ico_sizes)
        print("✅ Created favicon.ico")
        
        print("\n🎉 All favicon sizes created!")
        print("📁 Files created:")
        for _, _, filename in sizes:
            print(f"   - {filename}")
        print("   - favicon.ico")
        
        print("\n📝 Next steps:")
        print("1. Upload these files to your Railway deployment")
        print("2. Update the favicon URLs in app.py to point to the correct files")
        print("3. Test the favicon in different browsers")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure you have Pillow installed: pip install Pillow")

if __name__ == "__main__":
    create_favicon_sizes()
