#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Shutdown Configuration Management
每日关机配置管理
"""

import json
import os
import datetime
from typing import Dict, Optional, Tuple


class DailyShutdownConfig:
    """Daily shutdown configuration manager"""
    
    def __init__(self):
        self.config_file = os.path.expanduser("~/.shutdown_reminder_config.json")
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️  Failed to load config: {e}")
        
        # Return default configuration
        return {
            "daily_mode_enabled": False,
            "daily_shutdown_hour": 22,
            "daily_shutdown_minute": 30,
            "auto_shutdown": False,
            "last_updated": None
        }
    
    def _save_config(self) -> bool:
        """Save configuration to file"""
        try:
            self.config["last_updated"] = datetime.datetime.now().isoformat()
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ Failed to save config: {e}")
            return False
    
    def set_daily_shutdown_time(self, hour: int, minute: int) -> bool:
        """Set daily shutdown time"""
        if not (0 <= hour <= 23) or not (0 <= minute <= 59):
            return False
        
        self.config["daily_shutdown_hour"] = hour
        self.config["daily_shutdown_minute"] = minute
        self.config["daily_mode_enabled"] = True
        return self._save_config()
    
    def get_daily_shutdown_time(self) -> Tuple[int, int]:
        """Get daily shutdown time"""
        return (
            self.config.get("daily_shutdown_hour", 22),
            self.config.get("daily_shutdown_minute", 30)
        )
    
    def is_daily_mode_enabled(self) -> bool:
        """Check if daily mode is enabled"""
        return self.config.get("daily_mode_enabled", False)
    
    def set_daily_mode(self, enabled: bool) -> bool:
        """Enable or disable daily mode"""
        self.config["daily_mode_enabled"] = enabled
        return self._save_config()
    
    def set_auto_shutdown(self, enabled: bool) -> bool:
        """Enable or disable automatic shutdown (no user confirmation)"""
        self.config["auto_shutdown"] = enabled
        return self._save_config()
    
    def is_auto_shutdown_enabled(self) -> bool:
        """Check if automatic shutdown is enabled"""
        return self.config.get("auto_shutdown", False)
    
    def get_next_daily_shutdown(self) -> datetime.datetime:
        """Get the next daily shutdown time"""
        hour, minute = self.get_daily_shutdown_time()
        now = datetime.datetime.now()
        
        # Set for today
        next_shutdown = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # If the time has passed today, set for tomorrow
        if next_shutdown <= now:
            next_shutdown += datetime.timedelta(days=1)
        
        return next_shutdown
    
    def get_config_info(self) -> str:
        """Get formatted configuration information"""
        if not self.is_daily_mode_enabled():
            return "❌ Daily mode is disabled"
        
        hour, minute = self.get_daily_shutdown_time()
        auto_shutdown = "enabled" if self.is_auto_shutdown_enabled() else "disabled"
        next_time = self.get_next_daily_shutdown()
        
        info = f"""📅 Daily Shutdown Configuration:
  • Time: {hour:02d}:{minute:02d} daily
  • Auto shutdown: {auto_shutdown}
  • Next shutdown: {next_time.strftime('%Y-%m-%d %H:%M:%S')}
  • Config file: {self.config_file}"""
        
        return info