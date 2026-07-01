#!/usr/bin/env python3
"""
Test script for SharePoint to Storage Connector

Run this after starting the server to verify the connection and API.
"""

import requests
import json
from typing import Optional

# Configuration
SERVER_URL = "http://localhost:8000"


def test_health():
    """Test the health check endpoint"""
    print("\n=== Testing Health Check ===")
    response = requests.get(f"{SERVER_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_list_files(folder_path: str = ""):
    """Test listing files in a SharePoint folder"""
    print(f"\n=== Testing List Files: {folder_path or '/'} ===")
    try:
        response = requests.get(f"{SERVER_URL}/api/v1/list/{folder_path}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Files found: {len(data['files'])}")
            for file in data['files']:
                print(f"  - {file['name']} ({file['type']})")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False


def test_transfer_file(sharepoint_path: str, storage_key: Optional[str] = None):
    """Test transferring a file"""
    print("\n=== Testing File Transfer ===")
    print(f"SharePoint Path: {sharepoint_path}")

    payload = {
        "sharepoint_path": sharepoint_path,
        "preserve_path": True
    }
    if storage_key:
        payload["storage_key"] = storage_key

    try:
        response = requests.post(
            f"{SERVER_URL}/api/v1/transfer",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Transferred {data['size_bytes']} bytes")
            print(f"Storage Backend: {data['storage_backend']}")
            location_json = json.dumps(data['storage_location'])
            print(f"Storage Location: {location_json}")
            print(f"Storage Key: {data['storage_key']}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("SharePoint to Storage Connector Test Suite")
    print("=" * 50)

    # Test 1: Health check
    if not test_health():
        print("\n❌ Health check failed! Is the server running?")
        return

    print("\n✅ Health check passed!")

    # Test 2: List files (optional - requires valid SharePoint setup)
    print("\n" + "=" * 50)
    print("NOTE: The following tests require valid SharePoint credentials.")
    print("Press Ctrl+C to skip if not configured.")
    print("=" * 50)

    try:
        # Test listing root folder
        test_list_files()
    except KeyboardInterrupt:
        print("\n\nSkipping file listing tests.")
    except Exception as e:
        print(f"\nList test failed: {e}")

    # Test 3: Transfer file (requires specific path)
    print("\n" + "=" * 50)
    print("To test file transfer, uncomment and edit the test_transfer_file")
    print("call below with your actual SharePoint file path.")
    print("=" * 50)

    # Uncomment and modify to test:
    # test_transfer_file("Shared Documents/example.pdf", "test/uploaded.pdf")


if __name__ == "__main__":
    main()
