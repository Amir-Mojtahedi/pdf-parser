#!/usr/bin/env python3
"""
Debug script for testing PDF extraction functionality
"""
import requests
import json
from extractor import extract_pdf_text_from_url

def test_pdf_extraction():
    """Test PDF extraction with a sample URL"""
    
    # Sample PDF URL (you can replace this with any public PDF URL)
    test_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    
    print("Testing PDF extraction...")
    print(f"URL: {test_url}")
    
    try:
        # Test direct extraction
        print("\n1. Testing direct extraction...")
        text = extract_pdf_text_from_url(test_url)
        
        if text:
            print(f"✅ Success! Extracted {len(text)} characters")
            print(f"First 200 characters: {text[:200]}...")
        else:
            print("❌ Extraction failed")
            
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
    
    # Test API endpoint
    print("\n2. Testing API endpoint...")
    try:
        response = requests.post(
            "http://localhost:8000/extract",
            json={"fileUrl": test_url},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API Success! Extracted {result.get('character_count', 0)} characters")
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ API not running. Start the server first with 'python main.py'")
    except Exception as e:
        print(f"❌ API Error: {e}")

def test_api_status():
    """Test API status endpoint"""
    print("\n3. Testing API status...")
    try:
        response = requests.get("http://localhost:8000/status")
        if response.status_code == 200:
            print(f"✅ API Status: {response.json()}")
        else:
            print(f"❌ Status Error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ API not running. Start the server first with 'python main.py'")
    except Exception as e:
        print(f"❌ Status Error: {e}")

if __name__ == "__main__":
    print("=== PDF Extractor Debug Test ===\n")
    
    # Test API status first
    test_api_status()
    
    # Test PDF extraction
    test_pdf_extraction()
    
    print("\n=== Debug Test Complete ===") 