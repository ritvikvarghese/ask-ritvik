#!/usr/bin/env python3
"""
Simple script to generate Open Graph image for social media sharing.
This creates a basic image that can be used as og:image.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_og_image():
    # Image dimensions for Open Graph (1200x630)
    width, height = 1200, 630
    
    # Create image with dark gradient background
    image = Image.new('RGB', (width, height), color='#0e1117')
    draw = ImageDraw.Draw(image)
    
    # Add gradient effect (simplified)
    for y in range(height):
        alpha = int(255 * (1 - y / height * 0.3))
        color = (int(26 + (y / height) * 10), int(17 + (y / height) * 10), int(23 + (y / height) * 10))
        draw.line([(0, y), (width, y)], fill=color)
    
    try:
        # Try to use a system font
        title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 60)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 30)
        desc_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()
    
    # Title
    title = "Chat with Ritvik Varghese"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 150), title, fill='#4CAF50', font=title_font)
    
    # Subtitle
    subtitle = "3x Entrepreneur | AI Chat"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    draw.text((subtitle_x, 220), subtitle, fill='#cccccc', font=subtitle_font)
    
    # Description
    description = "Ask me anything about my journey, startups, and entrepreneurship."
    desc_bbox = draw.textbbox((0, 0), description, font=desc_font)
    desc_width = desc_bbox[2] - desc_bbox[0]
    desc_x = (width - desc_width) // 2
    draw.text((desc_x, 280), description, fill='#999999', font=desc_font)
    
    # URL
    url = "ask.ritvik.io"
    url_bbox = draw.textbbox((0, 0), url, font=desc_font)
    url_width = url_bbox[2] - url_bbox[0]
    url_x = (width - url_width) // 2
    draw.text((url_x, 350), url, fill='#4CAF50', font=desc_font)
    
    # Add robot emoji (simplified as text)
    draw.text((width - 100, 50), "🤖", fill='#4CAF50', font=ImageFont.load_default())
    
    # Save the image
    image.save('og-image.png')
    print("✅ Open Graph image created: og-image.png")
    
    return 'og-image.png'

if __name__ == "__main__":
    create_og_image()
