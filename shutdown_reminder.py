#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时关机提醒程序
Scheduled Shutdown Reminder Application
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import threading
import time
import subprocess
import platform
import sys


class ShutdownReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("定时关机提醒 - Shutdown Reminder")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Variables
        self.reminder_time = None
        self.timer_thread = None
        self.is_running = False
        
        # Create GUI
        self.create_widgets()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """居中显示窗口"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (300 // 2)
        self.root.geometry(f"400x300+{x}+{y}")
    
    def create_widgets(self):
        """创建GUI组件"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="定时关机提醒程序", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Time setting
        time_frame = ttk.LabelFrame(main_frame, text="设置提醒时间", padding="10")
        time_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Hour
        ttk.Label(time_frame, text="小时:").grid(row=0, column=0, padx=(0, 5))
        self.hour_var = tk.StringVar(value="22")
        hour_spinbox = ttk.Spinbox(time_frame, from_=0, to=23, width=5, textvariable=self.hour_var)
        hour_spinbox.grid(row=0, column=1, padx=(0, 20))
        
        # Minute
        ttk.Label(time_frame, text="分钟:").grid(row=0, column=2, padx=(0, 5))
        self.minute_var = tk.StringVar(value="30")
        minute_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, width=5, textvariable=self.minute_var)
        minute_spinbox.grid(row=0, column=3)
        
        # Current time display
        self.current_time_label = ttk.Label(main_frame, text="", font=("Arial", 12))
        self.current_time_label.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        # Status
        self.status_label = ttk.Label(main_frame, text="状态: 未设置", font=("Arial", 10))
        self.status_label.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(0, 10))
        
        self.start_button = ttk.Button(button_frame, text="开始提醒", command=self.start_reminder)
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="停止提醒", command=self.stop_reminder, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=(0, 10))
        
        self.test_button = ttk.Button(button_frame, text="测试关机提醒", command=self.test_reminder)
        self.test_button.grid(row=0, column=2)
        
        # Instructions
        instructions = """使用说明:
1. 设置希望收到关机提醒的时间
2. 点击"开始提醒"启动定时器
3. 到达设定时间时会弹出提醒窗口
4. 在提醒窗口中选择是否立即关机"""
        
        instruction_label = ttk.Label(main_frame, text=instructions, font=("Arial", 9), justify=tk.LEFT)
        instruction_label.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        
        # Start clock update
        self.update_clock()
    
    def update_clock(self):
        """更新当前时间显示"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.current_time_label.config(text=f"当前时间: {current_time}")
        self.root.after(1000, self.update_clock)
    
    def start_reminder(self):
        """开始定时提醒"""
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            
            if not (0 <= hour <= 23) or not (0 <= minute <= 59):
                messagebox.showerror("错误", "请输入有效的时间 (小时: 0-23, 分钟: 0-59)")
                return
            
            # Set reminder time for today or tomorrow
            now = datetime.datetime.now()
            self.reminder_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # If the time has passed today, set it for tomorrow
            if self.reminder_time <= now:
                self.reminder_time += datetime.timedelta(days=1)
            
            self.is_running = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            
            self.status_label.config(text=f"状态: 已设置提醒时间 {self.reminder_time.strftime('%Y-%m-%d %H:%M')}")
            
            # Start timer thread
            self.timer_thread = threading.Thread(target=self.timer_worker, daemon=True)
            self.timer_thread.start()
            
            messagebox.showinfo("成功", f"定时关机提醒已设置为 {self.reminder_time.strftime('%Y-%m-%d %H:%M')}")
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
    
    def stop_reminder(self):
        """停止定时提醒"""
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="状态: 已停止")
        messagebox.showinfo("提示", "定时关机提醒已停止")
    
    def timer_worker(self):
        """定时器工作线程"""
        while self.is_running:
            now = datetime.datetime.now()
            if now >= self.reminder_time:
                # Show reminder
                self.root.after(0, self.show_shutdown_reminder)
                break
            time.sleep(1)
    
    def show_shutdown_reminder(self):
        """显示关机提醒窗口"""
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="状态: 提醒已触发")
        
        # Create reminder window
        reminder_window = tk.Toplevel(self.root)
        reminder_window.title("关机提醒 - Shutdown Reminder")
        reminder_window.geometry("350x200")
        reminder_window.resizable(False, False)
        reminder_window.grab_set()  # Make it modal
        
        # Center the reminder window
        reminder_window.update_idletasks()
        x = (reminder_window.winfo_screenwidth() // 2) - (350 // 2)
        y = (reminder_window.winfo_screenheight() // 2) - (200 // 2)
        reminder_window.geometry(f"350x200+{x}+{y}")
        
        # Reminder content
        reminder_frame = ttk.Frame(reminder_window, padding="20")
        reminder_frame.pack(fill=tk.BOTH, expand=True)
        
        # Warning icon and message
        message_label = ttk.Label(reminder_frame, text="⚠️ 关机提醒", font=("Arial", 16, "bold"))
        message_label.pack(pady=(0, 10))
        
        info_label = ttk.Label(reminder_frame, text=f"设定的提醒时间已到！\n当前时间: {datetime.datetime.now().strftime('%H:%M:%S')}\n\n是否要立即关闭计算机？", 
                              font=("Arial", 12), justify=tk.CENTER)
        info_label.pack(pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(reminder_frame)
        button_frame.pack()
        
        def shutdown_now():
            reminder_window.destroy()
            self.shutdown_computer()
        
        def cancel_shutdown():
            reminder_window.destroy()
            messagebox.showinfo("提示", "已取消关机，您可以重新设置提醒时间。")
        
        ttk.Button(button_frame, text="立即关机", command=shutdown_now).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="取消", command=cancel_shutdown).pack(side=tk.LEFT)
        
        # Auto-close after 60 seconds
        def auto_close():
            if reminder_window.winfo_exists():
                reminder_window.destroy()
                messagebox.showinfo("提示", "提醒窗口已自动关闭，关机已取消。")
        
        reminder_window.after(60000, auto_close)  # 60 seconds
    
    def test_reminder(self):
        """测试关机提醒（不实际关机）"""
        self.show_shutdown_reminder()
    
    def shutdown_computer(self):
        """关闭计算机"""
        try:
            system = platform.system()
            
            # Show final confirmation
            if messagebox.askyesno("最终确认", "确定要关闭计算机吗？\n\n点击"是"将在3秒后开始关机\n点击"否"取消关机", icon="warning"):
                
                # Show countdown
                countdown_window = tk.Toplevel(self.root)
                countdown_window.title("关机倒计时")
                countdown_window.geometry("250x100")
                countdown_window.resizable(False, False)
                countdown_window.grab_set()
                
                countdown_label = ttk.Label(countdown_window, text="", font=("Arial", 14, "bold"))
                countdown_label.pack(expand=True)
                
                # Center countdown window
                countdown_window.update_idletasks()
                x = (countdown_window.winfo_screenwidth() // 2) - (250 // 2)
                y = (countdown_window.winfo_screenheight() // 2) - (100 // 2)
                countdown_window.geometry(f"250x100+{x}+{y}")
                
                # Countdown from 3
                for i in range(3, 0, -1):
                    countdown_label.config(text=f"关机倒计时: {i}")
                    countdown_window.update()
                    time.sleep(1)
                
                countdown_window.destroy()
                
                # Execute shutdown command based on OS
                if system == "Windows":
                    subprocess.run(["shutdown", "/s", "/t", "1"], check=False)
                elif system == "Darwin":  # macOS
                    subprocess.run(["sudo", "shutdown", "-h", "+1"], check=False)
                elif system == "Linux":
                    subprocess.run(["shutdown", "-h", "+1"], check=False)
                else:
                    messagebox.showerror("错误", f"不支持的操作系统: {system}")
                    return
                
                messagebox.showinfo("关机", "关机命令已执行")
                self.root.quit()
                
        except Exception as e:
            messagebox.showerror("错误", f"关机失败: {str(e)}")
    
    def on_closing(self):
        """处理窗口关闭事件"""
        if self.is_running:
            if messagebox.askokcancel("退出", "定时提醒正在运行，确定要退出吗？"):
                self.is_running = False
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """主函数"""
    root = tk.Tk()
    app = ShutdownReminderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()