import tkinter as tk
from Sender.file_reader import read_head, read_pages
# from qr_util import render_qr
from page_turner import PageTurner
import config

qr_canvas = None
log_area = None
page_turner = None
import sys
# sender_main_ui.py

def start():
    global qr_canvas, log_area, page_turner
    root = tk.Tk()
    root.title("Sender")
    def on_close():
        root.destroy()
        sys.exit(0)  # 退出 Python 程序
    root.protocol("WM_DELETE_WINDOW", on_close)
    # 多图区域（2x2 布局）
    qr_frame = tk.Frame(root)
    qr_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    qr_labels = []
    nRow = int(config.Show_Code.split('x')[0])
    nCol = int(config.Show_Code.split('x')[1])
    total_images = nRow * nCol
    for row in range(nRow):
        for col in range(nCol):
            lbl = tk.Label(qr_frame)
            lbl.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            qr_labels.append(lbl)

    log_area = tk.Text(root, width=40, height=20)
    log_area.pack(side=tk.RIGHT, fill=tk.Y)

    head = read_head(config.TARGET_FILE)
    log_area.insert(tk.END, f"文件载入完成\nMD5: {head.md5}\nSize: {head.file_size} bytes\n")

    pages = read_pages(config.TARGET_FILE, config.INIT_QR_SIZE)

    # 启动多图页面控制器
    page_turner = PageTurner(qr_labels, log_area, pages, total_images)
    # 延迟启动 PageTurner 的后台监听线程（确保 UI 构建完成）
    # def start_listener():
        # time.sleep(0.3)  # 小延迟避免卡 UI
    page_turner.start()

    # import threading, time
    # threading.Thread(target=start_listener, daemon=True).start()

    root.mainloop()
