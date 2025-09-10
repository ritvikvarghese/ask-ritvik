#!/usr/bin/env python3
"""
Script to extract content from PDF and text files for deployment
Run this to get the content that should be set as environment variables
"""

from pypdf import PdfReader
import os

def extract_content():
    # Extract LinkedIn content
    linkedin_content = ""
    if os.path.exists('ask-me/me/linkedin.pdf'):
        reader = PdfReader('ask-me/me/linkedin.pdf')
        for page in reader.pages:
            text = page.extract_text()
            if text:
                linkedin_content += text
    
    # Extract summary content
    summary_content = ""
    if os.path.exists('ask-me/me/summary.txt'):
        with open('ask-me/me/summary.txt', 'r', encoding='utf-8') as f:
            summary_content = f.read()
    
    print("=== LINKEDIN_CONTENT ===")
    print(linkedin_content)
    print("\n=== SUMMARY_CONTENT ===")
    print(summary_content)
    
    print("\n=== FOR DEPLOYMENT ===")
    print("Set these as environment variables in your deployment platform:")
    print(f"LINKEDIN_CONTENT='{linkedin_content[:100]}...'")
    print(f"SUMMARY_CONTENT='{summary_content[:100]}...'")

if __name__ == "__main__":
    extract_content()
