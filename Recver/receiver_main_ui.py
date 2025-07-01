# receiver_main_ui.py
import tkinter as tk
from threading import Thread
import receiver_logic

log_area = None
state_label = None


def start():
    global log_area, state_label
    root = tk.Tk()
    root.title("QR Receiver")

    start_btn = tk.Button(root, text="Start", width=10)
    start_btn.pack(pady=10)

    state_label = tk.Label(root, text="等待开始", anchor='w')
    state_label.pack(fill='x')

    log_area = tk.Text(root, height=25, width=60)
    log_area.pack(padx=10, pady=10)

    def on_start():
        start_btn.config(state=tk.DISABLED)
        Thread(target=lambda: receiver_logic.start(log_area, state_label), daemon=True).start()
        # print("结束任务")
    start_btn.config(command=on_start)

    root.mainloop()