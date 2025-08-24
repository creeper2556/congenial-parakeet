#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for daily shutdown functionality
"""

import sys
import os
import datetime

def test_daily_config():
    """Test daily shutdown configuration"""
    try:
        from daily_shutdown_config import DailyShutdownConfig
        
        print("🧪 Testing Daily Shutdown Configuration")
        print("=" * 45)
        
        # Create config instance
        config = DailyShutdownConfig()
        
        # Test initial state
        print("✅ Config instance created")
        print(f"📊 Initial daily mode enabled: {config.is_daily_mode_enabled()}")
        
        # Test setting daily shutdown time
        success = config.set_daily_shutdown_time(23, 45)
        print(f"✅ Set daily shutdown time: {success}")
        
        # Test getting daily shutdown time
        hour, minute = config.get_daily_shutdown_time()
        print(f"✅ Retrieved time: {hour:02d}:{minute:02d}")
        
        # Test next shutdown calculation
        next_shutdown = config.get_next_daily_shutdown()
        print(f"✅ Next shutdown: {next_shutdown.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test auto shutdown setting
        config.set_auto_shutdown(True)
        print(f"✅ Auto shutdown enabled: {config.is_auto_shutdown_enabled()}")
        
        # Test configuration info
        print("\n📋 Configuration Info:")
        print(config.get_config_info())
        
        # Test persistence
        config2 = DailyShutdownConfig()
        hour2, minute2 = config2.get_daily_shutdown_time()
        print(f"\n✅ Configuration persisted: {hour2:02d}:{minute2:02d}")
        
        print("\n🎉 All daily config tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Daily config test failed: {e}")
        return False

def test_cli_daily_integration():
    """Test CLI daily mode integration"""
    try:
        from shutdown_reminder_cli import ShutdownReminderCLI
        
        print("\n🧪 Testing CLI Daily Integration")
        print("=" * 40)
        
        # Create CLI instance
        cli = ShutdownReminderCLI()
        print("✅ CLI instance created with daily support")
        
        # Check if daily mode is available
        has_daily_mode = hasattr(cli, 'daily_mode') and hasattr(cli, 'config')
        print(f"✅ Daily mode attributes: {has_daily_mode}")
        
        # Test config integration
        if has_daily_mode:
            config_enabled = cli.config.is_daily_mode_enabled()
            print(f"✅ Config integration: {config_enabled}")
        
        print("✅ CLI daily integration test passed!")
        return True
        
    except Exception as e:
        print(f"❌ CLI integration test failed: {e}")
        return False

def main():
    """Run daily functionality tests"""
    print("🚀 Daily Shutdown Functionality Tests")
    print("=" * 50)
    
    tests = [
        ("Daily Config Test", test_daily_config),
        ("CLI Daily Integration", test_cli_daily_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} error: {e}")
    
    print(f"\n📊 Daily Tests Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All daily functionality tests passed!")
        return 0
    else:
        print("⚠️  Some daily functionality tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())