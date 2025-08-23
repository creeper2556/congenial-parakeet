#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时关机提醒程序 - 命令行版本
Scheduled Shutdown Reminder Application - Command Line Version
"""

import datetime
import threading
import time
import subprocess
import platform
import sys
import signal
import os


class ShutdownReminderCLI:
    def __init__(self):
        self.reminder_time = None
        self.timer_thread = None
        self.is_running = False
        self.shutdown_cancelled = False
        
        # Handle Ctrl+C gracefully
        signal.signal(signal.SIGINT, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        """处理Ctrl+C信号"""
        print("\n\n程序被中断，正在退出...")
        self.is_running = False
        sys.exit(0)
    
    def display_banner(self):
        """显示程序标题"""
        banner = """
╔═══════════════════════════════════════════════╗
║              定时关机提醒程序                  ║
║         Scheduled Shutdown Reminder          ║
╚═══════════════════════════════════════════════╝
"""
        print(banner)
        print(f"当前时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"操作系统: {platform.system()} {platform.release()}")
        print()
    
    def get_user_time(self):
        """获取用户输入的时间"""
        while True:
            try:
                print("请设置关机提醒时间:")
                hour_input = input("小时 (0-23): ").strip()
                minute_input = input("分钟 (0-59): ").strip()
                
                hour = int(hour_input)
                minute = int(minute_input)
                
                if not (0 <= hour <= 23) or not (0 <= minute <= 59):
                    print("❌ 时间格式错误，请重新输入！\n")
                    continue
                
                # Set reminder time for today or tomorrow
                now = datetime.datetime.now()
                reminder_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                # If the time has passed today, set it for tomorrow
                if reminder_time <= now:
                    reminder_time += datetime.timedelta(days=1)
                    print(f"⚠️  设定时间已过，自动设置为明天 {reminder_time.strftime('%H:%M')}")
                
                return reminder_time
                
            except ValueError:
                print("❌ 请输入有效的数字！\n")
            except KeyboardInterrupt:
                self.signal_handler(None, None)
    
    def confirm_setting(self, reminder_time):
        """确认设置"""
        print(f"\n⏰ 关机提醒时间设置为: {reminder_time.strftime('%Y年%m月%d日 %H:%M')}")
        
        time_diff = reminder_time - datetime.datetime.now()
        hours = int(time_diff.total_seconds() // 3600)
        minutes = int((time_diff.total_seconds() % 3600) // 60)
        
        if hours > 0:
            print(f"📅 距离提醒时间还有: {hours}小时{minutes}分钟")
        else:
            print(f"📅 距离提醒时间还有: {minutes}分钟")
        
        while True:
            confirm = input("\n确认设置吗? (y/n): ").strip().lower()
            if confirm in ['y', 'yes', '是']:
                return True
            elif confirm in ['n', 'no', '否']:
                return False
            else:
                print("请输入 y 或 n")
    
    def start_reminder(self, reminder_time):
        """开始提醒倒计时"""
        self.reminder_time = reminder_time
        self.is_running = True
        
        print("\n✅ 定时关机提醒已启动！")
        print("💡 按 Ctrl+C 可以随时取消")
        print("=" * 50)
        
        # Start timer thread
        self.timer_thread = threading.Thread(target=self.timer_worker, daemon=True)
        self.timer_thread.start()
        
        # Main loop - show countdown
        self.show_countdown()
    
    def timer_worker(self):
        """定时器工作线程"""
        while self.is_running:
            now = datetime.datetime.now()
            if now >= self.reminder_time:
                self.is_running = False
                break
            time.sleep(1)
    
    def show_countdown(self):
        """显示倒计时"""
        try:
            while self.is_running:
                now = datetime.datetime.now()
                time_diff = self.reminder_time - now
                
                if time_diff.total_seconds() <= 0:
                    break
                
                hours = int(time_diff.total_seconds() // 3600)
                minutes = int((time_diff.total_seconds() % 3600) // 60)
                seconds = int(time_diff.total_seconds() % 60)
                
                # Clear line and show countdown
                print(f"\r⏳ 倒计时: {hours:02d}:{minutes:02d}:{seconds:02d} | 当前时间: {now.strftime('%H:%M:%S')}", end="", flush=True)
                time.sleep(1)
            
            if self.is_running or not self.shutdown_cancelled:
                print("\n")  # New line after countdown
                self.show_shutdown_reminder()
                
        except KeyboardInterrupt:
            self.signal_handler(None, None)
    
    def show_shutdown_reminder(self):
        """显示关机提醒"""
        print("\n")
        print("🔔" * 50)
        print("⚠️  关机提醒时间到了！")
        print("⚠️  SHUTDOWN REMINDER TIME!")
        print("🔔" * 50)
        print(f"⏰ 当前时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📅 设定时间: {self.reminder_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Ask user what to do
        while True:
            print("请选择操作:")
            print("1. 立即关机 (Shutdown now)")
            print("2. 取消关机 (Cancel)")
            print("3. 延迟关机 (Delay)")
            
            try:
                choice = input("\n请输入选择 (1/2/3): ").strip()
                
                if choice == '1':
                    self.shutdown_computer()
                    break
                elif choice == '2':
                    self.shutdown_cancelled = True
                    print("✅ 已取消关机")
                    break
                elif choice == '3':
                    self.delay_shutdown()
                    break
                else:
                    print("❌ 无效选择，请重新输入")
                    
            except KeyboardInterrupt:
                self.signal_handler(None, None)
    
    def delay_shutdown(self):
        """延迟关机"""
        print("\n延迟关机选项:")
        print("1. 延迟 10 分钟")
        print("2. 延迟 30 分钟")
        print("3. 延迟 1 小时")
        print("4. 自定义延迟时间")
        
        try:
            choice = input("请选择延迟时间 (1-4): ").strip()
            
            delay_minutes = 0
            if choice == '1':
                delay_minutes = 10
            elif choice == '2':
                delay_minutes = 30
            elif choice == '3':
                delay_minutes = 60
            elif choice == '4':
                delay_minutes = int(input("请输入延迟分钟数: "))
            else:
                print("❌ 无效选择")
                return
            
            new_time = datetime.datetime.now() + datetime.timedelta(minutes=delay_minutes)
            print(f"✅ 已延迟 {delay_minutes} 分钟，新的提醒时间: {new_time.strftime('%H:%M:%S')}")
            
            # Restart with new time
            self.start_reminder(new_time)
            
        except (ValueError, KeyboardInterrupt):
            print("❌ 输入错误或被中断")
    
    def shutdown_computer(self):
        """关闭计算机"""
        print("\n⚠️  最终确认 ⚠️")
        print("这将关闭您的计算机!")
        
        confirm = input("确定要关闭计算机吗? (输入 'YES' 确认): ").strip()
        
        if confirm.upper() == 'YES':
            print("\n🔄 准备关闭计算机...")
            
            # Countdown
            for i in range(5, 0, -1):
                print(f"⏰ {i} 秒后关机... (按 Ctrl+C 取消)")
                time.sleep(1)
            
            try:
                system = platform.system()
                print(f"\n💻 检测到操作系统: {system}")
                
                # Execute shutdown command based on OS
                if system == "Windows":
                    print("🔄 执行 Windows 关机命令...")
                    subprocess.run(["shutdown", "/s", "/t", "1"], check=True)
                elif system == "Darwin":  # macOS
                    print("🔄 执行 macOS 关机命令...")
                    subprocess.run(["sudo", "shutdown", "-h", "+1"], check=True)
                elif system == "Linux":
                    print("🔄 执行 Linux 关机命令...")
                    subprocess.run(["shutdown", "-h", "+1"], check=True)
                else:
                    print(f"❌ 不支持的操作系统: {system}")
                    return
                
                print("✅ 关机命令已执行")
                
            except subprocess.CalledProcessError as e:
                print(f"❌ 关机命令执行失败: {e}")
                print("💡 可能需要管理员权限")
            except FileNotFoundError:
                print("❌ 找不到关机命令")
            except Exception as e:
                print(f"❌ 关机失败: {e}")
        else:
            print("❌ 关机已取消")
            self.shutdown_cancelled = True
    
    def run(self):
        """运行主程序"""
        try:
            self.display_banner()
            
            while True:
                reminder_time = self.get_user_time()
                
                if self.confirm_setting(reminder_time):
                    self.start_reminder(reminder_time)
                    break
                else:
                    print("❌ 已取消设置，请重新输入\n")
            
            # Wait for thread to complete
            if self.timer_thread and self.timer_thread.is_alive():
                self.timer_thread.join()
            
            if not self.shutdown_cancelled:
                print("\n📝 程序结束")
            
        except KeyboardInterrupt:
            self.signal_handler(None, None)
        except Exception as e:
            print(f"❌ 程序出现错误: {e}")


def show_help():
    """显示帮助信息"""
    help_text = """
定时关机提醒程序 - 命令行版本
Scheduled Shutdown Reminder Application - CLI Version

使用方法 Usage:
  python shutdown_reminder_cli.py [选项]

选项 Options:
  -h, --help     显示此帮助信息并退出
  --version      显示版本信息并退出

功能说明 Features:
  - 设置自定义关机提醒时间
  - 实时倒计时显示
  - 多种关机选项（立即、延迟、取消）
  - 跨平台支持 (Windows/Linux/macOS)

示例 Example:
  python shutdown_reminder_cli.py

注意 Note:
  - 使用 Ctrl+C 可以随时取消程序
  - 关机命令需要相应的系统权限
  - 建议先测试程序功能后再实际使用
"""
    print(help_text)


def main():
    """主函数"""
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            show_help()
            sys.exit(0)
        elif sys.argv[1] == '--version':
            print("定时关机提醒程序 v1.0.0")
            print("Shutdown Reminder CLI v1.0.0")
            sys.exit(0)
        else:
            print(f"未知选项: {sys.argv[1]}")
            print("使用 -h 或 --help 查看帮助信息")
            sys.exit(1)
    
    app = ShutdownReminderCLI()
    app.run()


if __name__ == "__main__":
    main()