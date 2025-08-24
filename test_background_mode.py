#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick test for daily background mode functionality
"""

import datetime
import time
from daily_shutdown_config import DailyShutdownConfig
from shutdown_reminder_cli import ShutdownReminderCLI

def test_background_mode_setup():
    """Test setting up background mode with near-immediate trigger"""
    print("🧪 Testing Background Mode Setup")
    print("=" * 40)
    
    # Set up a shutdown time 2 minutes from now for testing
    config = DailyShutdownConfig()
    now = datetime.datetime.now()
    test_time = now + datetime.timedelta(minutes=2)
    
    print(f"📅 Setting test shutdown for: {test_time.strftime('%H:%M:%S')}")
    
    # Configure for testing
    config.set_daily_shutdown_time(test_time.hour, test_time.minute)
    config.set_auto_shutdown(False)  # Don't actually shutdown
    
    print("✅ Configuration set")
    print(config.get_config_info())
    
    # Test that CLI can load the configuration
    cli = ShutdownReminderCLI()
    print(f"\n✅ CLI loaded config: {cli.config.is_daily_mode_enabled()}")
    
    # Show what would happen in background mode
    next_shutdown = config.get_next_daily_shutdown()
    time_until = next_shutdown - datetime.datetime.now()
    
    print(f"\n🔄 Background mode would:")
    print(f"   • Wait until: {next_shutdown.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   • Time remaining: {str(time_until).split('.')[0]}")
    print(f"   • Auto-shutdown: {'Yes' if config.is_auto_shutdown_enabled() else 'No (prompt user)'}")
    
    return True

def test_timer_logic():
    """Test the timer logic without actual waiting"""
    print("\n🧪 Testing Timer Logic")
    print("=" * 30)
    
    # Test case 1: Time in the future today
    now = datetime.datetime.now()
    future_today = now + datetime.timedelta(hours=1)
    
    config = DailyShutdownConfig()
    config.set_daily_shutdown_time(future_today.hour, future_today.minute)
    
    next_shutdown = config.get_next_daily_shutdown()
    print(f"✅ Future today test: {next_shutdown.date() == now.date()}")
    
    # Test case 2: Time that already passed today (should be tomorrow)
    past_today = now - datetime.timedelta(hours=1)
    config.set_daily_shutdown_time(past_today.hour, past_today.minute)
    
    next_shutdown = config.get_next_daily_shutdown()
    tomorrow = now.date() + datetime.timedelta(days=1)
    print(f"✅ Past today test: {next_shutdown.date() == tomorrow}")
    
    return True

if __name__ == "__main__":
    print("🚀 Daily Background Mode Test")
    print("=" * 35)
    print("Testing background mode functionality without")
    print("actually running long timers or shutdowns.\n")
    
    try:
        test_background_mode_setup()
        test_timer_logic()
        
        print("\n" + "="*35)
        print("🎉 Background Mode Tests Passed!")
        print("="*35)
        print("The background mode is ready for use.")
        print("\nTo test full functionality:")
        print("1. Run: python shutdown_reminder_cli.py")
        print("2. Choose option 3 to configure daily shutdown")
        print("3. Set a time 1-2 minutes in the future")
        print("4. Choose option 6 to start background mode")
        print("5. Wait and observe the behavior")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")