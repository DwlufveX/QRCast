import tkinter as tk
from tkinter import messagebox
import sender_main_ui

def show_disclaimer():
    root = tk.Tk()
    root.withdraw()
    result = messagebox.askyesno("免责声明", "你确认你不会将本工具用于非法用途？")
    if result:
        sender_main_ui.start()
    else:
        print("用户取消启动。")

if __name__ == "__main__":
    show_disclaimer()
