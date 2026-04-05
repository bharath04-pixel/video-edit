#!/usr/bin/env python3
"""
Comprehensive test script for AI Video Editor API
Tests all endpoints with sample data
"""

import requests
import json
from pathlib import Path
import time

BASE_URL = "http://localhost:8000"
TEST_VIDEO = "test_video.mp4"  # You'll need to provide this
TIMEOUT = 30

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(message):
    print(f"{Colors.BLUE}❯ {message}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

# ============================================================================
# TEST 1: Health Check
# ============================================================================

def test_health():
    """Test health endpoint"""
    print_test("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health check passed: {data['status']}")
            print(f"  API Version: {data['version']}")
            print(f"  Max file size: {data['max_file_size_mb']}MB")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {str(e)}")
        return False

# ============================================================================
# TEST 2: Info Endpoint
# ============================================================================

def test_info():
    """Test info endpoint"""
    print_test("Testing info endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/info", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print_success("Info retrieved")
            print(f"  Uploads: {data['uploads']}")
            print(f"  Outputs: {data['outputs']}")
            return True
        else:
            print_error(f"Info endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Info endpoint error: {str(e)}")
        return False

# ============================================================================
# TEST 3: Video Upload
# ============================================================================

def test_upload():
    """Test video upload"""
    print_test("Testing video upload...")
    
    # Create a minimal valid MP4 file for testing
    if not Path(TEST_VIDEO).exists():
        print_warning(f"{TEST_VIDEO} not found, creating minimal test video...")
        create_test_video()
    
    try:
        with open(TEST_VIDEO, 'rb') as f:
            files = {'file': (TEST_VIDEO, f, 'video/mp4')}
            response = requests.post(
                f"{BASE_URL}/api/upload",
                files=files,
                timeout=TIMEOUT
            )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Video uploaded successfully")
            print(f"  Video ID: {data['id']}")
            print(f"  Filename: {data['filename']}")
            print(f"  File size: {data['file_size']} bytes")
            return data['id']
        else:
            print_error(f"Upload failed: {response.status_code}")
            print_error(f"Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Upload error: {str(e)}")
        return None

# ============================================================================
# TEST 4: Process Video - Text Detection
# ============================================================================

def test_process_text_detection(video_id):
    """Test text detection processing"""
    print_test("Testing text detection...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/process",
            params={
                "video_id": video_id,
                "operation": "text_detection"
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Text detection completed")
            print(f"  Frame count: {data.get('frame_count', 0)}")
            return True
        else:
            print_error(f"Text detection failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Text detection error: {str(e)}")
        return False

# ============================================================================
# TEST 5: Process Video - Person Detection
# ============================================================================

def test_process_person_detection(video_id):
    """Test person detection processing"""
    print_test("Testing person detection...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/process",
            params={
                "video_id": video_id,
                "operation": "person_detection"
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Person detection completed")
            print(f"  Person count: {data.get('person_count', 0)}")
            return True
        else:
            print_error(f"Person detection failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Person detection error: {str(e)}")
        return False

# ============================================================================
# TEST 6: Export Video
# ============================================================================

def test_export(video_id):
    """Test video export"""
    print_test("Testing video export...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/export",
            params={"video_id": video_id},
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Video exported")
            print(f"  Download URL: {data['download_url']}")
            return data['download_url']
        else:
            print_error(f"Export failed: {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Export error: {str(e)}")
        return None

# ============================================================================
# TEST 7: Cleanup
# ============================================================================

def test_cleanup(video_id):
    """Test cleanup endpoint"""
    print_test("Testing cleanup...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/cleanup/{video_id}",
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Cleanup completed")
            return True
        else:
            print_error(f"Cleanup failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Cleanup error: {str(e)}")
        return False

# ============================================================================
# HELPER: Create Test Video
# ============================================================================

def create_test_video():
    """Create a minimal MP4 file for testing"""
    try:
        # This creates a simple MP4 file header
        # In production, use ffmpeg or similar
        print_warning("Creating minimal test video (1 second, 640x480)...")
        import subprocess
        
        cmd = [
            "ffmpeg",
            "-f", "lavfi",
            "-i", "color=c=blue:s=640x480:d=1",
            "-f", "lavfi",
            "-i", "anullsrc=r=44100:cl=mono",
            "-pix_fmt", "yuv420p",
            "-y",
            TEST_VIDEO
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=10)
        if result.returncode == 0:
            print_success(f"Test video created: {TEST_VIDEO}")
        else:
            print_error("Failed to create test video")
    except Exception as e:
        print_error(f"Error creating test video: {str(e)}")

# ============================================================================
# RUN ALL TESTS
# ============================================================================

def run_all_tests():
    """Run all tests"""
    print(f"\n{Colors.BLUE}======= AI VIDEO EDITOR - API TEST SUITE ======={Colors.END}\n")
    
    results = {
        "health": False,
        "info": False,
        "upload": None,
        "text_detection": False,
        "person_detection": False,
        "export": False,
        "cleanup": False
    }
    
    # Test 1: Health Check
    results["health"] = test_health()
    print()
    
    if not results["health"]:
        print_error("Backend is not running. Start it with: python app/main.py")
        return results
    
    # Test 2: Info
    results["info"] = test_info()
    print()
    
    # Test 3: Upload
    video_id = test_upload()
    results["upload"] = video_id is not None
    print()
    
    if not results["upload"]:
        print_error("Upload failed. Cannot continue with other tests.")
        return results
    
    # Test 4: Text Detection
    results["text_detection"] = test_process_text_detection(video_id)
    print()
    
    # Test 5: Person Detection
    results["person_detection"] = test_process_person_detection(video_id)
    print()
    
    # Test 6: Export
    download_url = test_export(video_id)
    results["export"] = download_url is not None
    print()
    
    # Test 7: Cleanup
    results["cleanup"] = test_cleanup(video_id)
    print()
    
    # Summary
    print(f"{Colors.BLUE}======= TEST SUMMARY ======={Colors.END}")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = Colors.GREEN + "PASS" + Colors.END if result else Colors.RED + "FAIL" + Colors.END
        print(f"{test_name:20} : {status}")
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print(Colors.GREEN + "All tests passed! ✓" + Colors.END)
    else:
        print(Colors.YELLOW + "Some tests failed. Check errors above." + Colors.END)
    
    return results

if __name__ == "__main__":
    run_all_tests()
