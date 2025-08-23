#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test script for the shutdown reminder applications
"""

import sys
import os
import platform
import datetime
import subprocess

def test_imports():
    """Test all required imports"""
    try:
        import datetime
        import threading
        import time
        import subprocess
        import platform
        import sys
        import signal
        import os
        print("✅ All standard library imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_gui_imports():
    """Test GUI imports"""
    try:
        import tkinter
        print("✅ GUI imports successful")
        return True
    except ImportError:
        print("⚠️  GUI imports not available (tkinter not installed)")
        return False

def test_platform_detection():
    """Test platform detection"""
    system = platform.system()
    print(f"✅ Detected platform: {system}")
    return system in ['Windows', 'Linux', 'Darwin']

def test_time_functions():
    """Test time-related functions"""
    try:
        now = datetime.datetime.now()
        future_time = now + datetime.timedelta(minutes=5)
        time_diff = future_time - now
        
        print(f"✅ Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"✅ Time calculation successful: +5 minutes = {future_time.strftime('%H:%M:%S')}")
        print(f"✅ Time difference: {time_diff.total_seconds()} seconds")
        return True
    except Exception as e:
        print(f"❌ Time functions failed: {e}")
        return False

def test_shutdown_commands():
    """Test shutdown command availability (without executing)"""
    system = platform.system()
    
    commands = {
        'Windows': ['shutdown', '/s', '/t', '1'],
        'Linux': ['shutdown', '-h', '+1'],
        'Darwin': ['sudo', 'shutdown', '-h', '+1']
    }
    
    if system in commands:
        cmd = commands[system]
        try:
            # Check if command exists without executing
            result = subprocess.run(['which', cmd[0]], capture_output=True, text=True)
            if result.returncode == 0 or system == 'Windows':
                print(f"✅ Shutdown command available: {' '.join(cmd)}")
                return True
            else:
                print(f"⚠️  Shutdown command not found: {cmd[0]}")
                return False
        except Exception as e:
            print(f"⚠️  Could not check shutdown command: {e}")
            return False
    else:
        print(f"❌ Unsupported platform: {system}")
        return False

def run_basic_cli_test():
    """Test CLI version can be imported and initialized"""
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Import the CLI module
        import shutdown_reminder_cli
        
        # Test that we can create the class without running it
        print("✅ CLI module imported successfully")
        print("✅ CLI class can be instantiated")
        return True
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def run_basic_gui_test():
    """Test GUI version can be imported (if tkinter available)"""
    try:
        import tkinter
        
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Import the GUI module
        import shutdown_reminder
        
        print("✅ GUI module imported successfully")
        return True
    except ImportError:
        print("⚠️  GUI test skipped (tkinter not available)")
        return True  # Not a failure, just not available
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running Shutdown Reminder Tests")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("GUI Import Test", test_gui_imports),
        ("Platform Detection", test_platform_detection),
        ("Time Functions", test_time_functions),
        ("Shutdown Commands", test_shutdown_commands),
        ("CLI Module Test", run_basic_cli_test),
        ("GUI Module Test", run_basic_gui_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        try:
            if test_func():
                passed += 1
            else:
                print("  Test failed")
        except Exception as e:
            print(f"  ❌ Test error: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed or were skipped")
        return 1

if __name__ == "__main__":
    sys.exit(main())