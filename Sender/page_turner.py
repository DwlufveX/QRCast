import win32con
import win32api

from qr_util import generate_qr_image
import keyboard
import time
import pyautogui
def press_real_key_up(hex_key):
    win32api.keybd_event(ord(hex_key), 0, win32con.KEYEVENTF_KEYUP, 0)

def press_real_key_down(hex_key):
    win32api.keybd_event(ord(hex_key), 0, 0, 0)
class PageTurner:
    def __init__(self, qr_labels, log_widget, pages_iter, batch_size):
        self.qr_labels = qr_labels
        self.log_widget = log_widget
        self.pages = list(pages_iter)
        self.cursor = -1
        self.batch_size = batch_size
        self.last_flip_time = 0
        self.start_time = None
        self.start_sent = False
        self.total_bytes = sum(len(data) for (n, data) in self.pages if n >= 0)
        self.sent_bytes = 0

    def log(self, text):
        self.log_widget.insert("end", text + "\n")
        self.log_widget.see("end")

    def show_end(self):
        payload = "END"
        img = generate_qr_image(payload, master=self.qr_labels[0])
        self.qr_labels[0].config(image=img)
        self.qr_labels[0].image = img
        for i in range(1, self.batch_size):
            self.qr_labels[i].config(image=None)
        self.log("所有数据已发送，显示 END 帧")

    def show_batch(self):
        if self.cursor == -1:
            # 第一次先只显示 START
            payload = f"START:{len(self.pages)}"
            img = generate_qr_image(payload, master=self.qr_labels[0])
            self.qr_labels[0].config(image=img)
            self.qr_labels[0].image = img

            # 其余 Label 置空
            for i in range(1, self.batch_size):
                self.qr_labels[i].config(image=None)

            self.log("显示 START 帧，等待收端")
            self.start_sent = True
            return
        # 正常批次
        batch_bytes = 0
        for i in range(self.batch_size):
            if self.cursor + i < len(self.pages):
                page_num, data = self.pages[self.cursor + i]
                if page_num == -2:
                    payload = "END"
                else:
                    payload = f"{page_num}:{data.hex()}"

                img = generate_qr_image(payload, master=self.qr_labels[i])
                self.qr_labels[i].config(image=img)
                self.qr_labels[i].image = img

                if page_num >= 0:
                    self.log(f"page {page_num}, size={len(data)}")
                    batch_bytes += len(data)
                else:
                    self.log(f"信号帧: {payload}")
            else:
                self.qr_labels[i].config(image=None)
        # 累加已发送字节数
        self.sent_bytes += batch_bytes

        # 计算速率与预估时间
        elapsed = time.time() - self.start_time if self.start_time else 0
        speed = self.sent_bytes / elapsed if elapsed > 0 else 0
        # eta = (self.total_bytes - self.sent_bytes) / speed if speed > 0 else float("inf")

        self.log(
            f"已发送 {self.sent_bytes}/{self.total_bytes} bytes | "
            f"平均速度 {speed:.2f} B/s | "
            f"耗时 {elapsed:.1f}s | "
            # f"预计剩余 {eta:.1f}s"
        )
    def on_key(self, event):
        if self.start_time is None:
            self.start_time = time.time()
        if event.name == '2' and event.event_type == 'down':
            press_real_key_up('2')  # 收到 '2' 后松开 '2'
            now = time.time()
            if now - self.last_flip_time < 0.3:
                return  # 忽略重复触发
            self.last_flip_time = now
            if self.cursor == -1:
                # START结束
                self.cursor = 0
            else:
                # 后续批次正常累加
                self.cursor += self.batch_size
                if self.cursor >= len(self.pages):
                    self.cursor = 0
                    # 所有数据页已发完，显示END
                    # self.show_end()
                    keyboard.unhook_all()
                    return
            self.show_batch()
            # time.sleep(0.1)
            win32api.keybd_event(ord('1'), 0, 0, 0)
            win32api.keybd_event(ord('1'), 0, win32con.KEYEVENTF_KEYUP, 0)

    def start(self):
        self.show_batch()
        keyboard.hook(self.on_key)  # 全局钩子
