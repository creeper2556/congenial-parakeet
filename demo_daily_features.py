#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Shutdown Functionality Demo Script
每日关机功能演示脚本
"""

import sys
import os
import datetime
from daily_shutdown_config import DailyShutdownConfig

def demo_daily_configuration():
    """演示每日配置功能"""
    print("🔧 Daily Configuration Demo")
    print("=" * 40)
    
    config = DailyShutdownConfig()
    
    # Show initial state
    print(f"📊 Current daily mode: {'Enabled' if config.is_daily_mode_enabled() else 'Disabled'}")
    
    if config.is_daily_mode_enabled():
        hour, minute = config.get_daily_shutdown_time()
        next_shutdown = config.get_next_daily_shutdown()
        auto_mode = config.is_auto_shutdown_enabled()
        
        print(f"⏰ Daily shutdown time: {hour:02d}:{minute:02d}")
        print(f"🤖 Auto shutdown: {'Enabled' if auto_mode else 'Disabled'}")
        print(f"📅 Next shutdown: {next_shutdown.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏱️  Time until next shutdown: {next_shutdown - datetime.datetime.now()}")
    
    print()

def demo_config_operations():
    """演示配置操作"""
    print("⚙️  Configuration Operations Demo")
    print("=" * 45)
    
    config = DailyShutdownConfig()
    
    # Save current config
    old_hour, old_minute = config.get_daily_shutdown_time()
    old_auto = config.is_auto_shutdown_enabled()
    
    # Demo: Set a new daily shutdown time
    demo_hour, demo_minute = 22, 15
    print(f"🔧 Setting daily shutdown to {demo_hour:02d}:{demo_minute:02d}")
    success = config.set_daily_shutdown_time(demo_hour, demo_minute)
    print(f"✅ Configuration saved: {success}")
    
    # Demo: Enable auto shutdown
    print("🤖 Enabling auto shutdown mode")
    config.set_auto_shutdown(True)
    
    # Show updated config
    print("\n📋 Updated configuration:")
    print(config.get_config_info())
    
    # Restore original config
    print(f"\n🔄 Restoring original config: {old_hour:02d}:{old_minute:02d}")
    config.set_daily_shutdown_time(old_hour, old_minute)
    config.set_auto_shutdown(old_auto)
    
    print()

def demo_time_calculations():
    """演示时间计算功能"""
    print("🕐 Time Calculation Demo")
    print("=" * 35)
    
    config = DailyShutdownConfig()
    
    # Test different shutdown times
    test_times = [
        (1, 30),   # Early morning
        (12, 0),   # Noon
        (18, 30),  # Evening
        (23, 59),  # Late night
    ]
    
    current_time = datetime.datetime.now()
    print(f"🕐 Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    for hour, minute in test_times:
        # Temporarily set time
        config.set_daily_shutdown_time(hour, minute)
        next_shutdown = config.get_next_daily_shutdown()
        time_diff = next_shutdown - current_time
        
        print(f"⏰ Shutdown time {hour:02d}:{minute:02d} -> Next: {next_shutdown.strftime('%Y-%m-%d %H:%M')}")
        print(f"   ⏱️  Time difference: {str(time_diff).split('.')[0]}")
        print()

def show_current_status():
    """显示当前状态"""
    print("📊 Current System Status")
    print("=" * 35)
    
    config = DailyShutdownConfig()
    
    print(f"🕐 Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if config.is_daily_mode_enabled():
        print(config.get_config_info())
    else:
        print("❌ Daily mode is currently disabled")
        print("💡 Use option 3 in CLI to configure daily shutdown")
    
    # Check if config file exists
    import os
    config_exists = os.path.exists(config.config_file)
    print(f"\n📄 Config file exists: {config_exists}")
    if config_exists:
        stat = os.stat(config.config_file)
        print(f"📄 Config file size: {stat.st_size} bytes")
        print(f"📄 Last modified: {datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """主演示函数"""
    print("🚀 Daily Shutdown Functionality Demo")
    print("=" * 50)
    print("This demo showcases the daily recurring shutdown features")
    print("added to the Shutdown Reminder application.")
    print()
    
    demos = [
        show_current_status,
        demo_daily_configuration,
        demo_config_operations,
        demo_time_calculations,
    ]
    
    for i, demo_func in enumerate(demos, 1):
        print(f"\n{'='*60}")
        print(f"Demo {i}/{len(demos)}")
        print('='*60)
        
        try:
            demo_func()
        except Exception as e:
            print(f"❌ Demo error: {e}")
        
        if i < len(demos):
            input("Press Enter to continue to next demo...")
    
    print("\n" + "="*60)
    print("🎉 Demo Complete!")
    print("="*60)
    print("Key Features Demonstrated:")
    print("  ✅ Persistent daily configuration")
    print("  ✅ Smart time calculation (today/tomorrow)")
    print("  ✅ Auto-shutdown mode support")
    print("  ✅ Configuration file management")
    print("  ✅ Real-time status display")
    print("\nTo use these features:")
    print("  • Run: python shutdown_reminder_cli.py")
    print("  • Choose option 3 to configure daily shutdown")
    print("  • Choose option 6 for background mode")

if __name__ == "__main__":
    main()