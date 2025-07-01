import time
import keyboard

from Sender import config
from file_writer import write_data, get_md5
from screen_capture import decode_qr_multi
import win32api
import win32con


start_time = time.time()
log_widget = None
state_label = None

waiting_ack = False
ack_received = False
def log(text):
    if log_widget:
        log_widget.insert('end', text + '\n')
        log_widget.see('end')

def press_real_key_down(hex_key):
    win32api.keybd_event(ord(hex_key), 0, 0, 0)

def press_real_key_up(hex_key):
    win32api.keybd_event(ord(hex_key), 0, win32con.KEYEVENTF_KEYUP, 0)
def set_state(text):
    if state_label:
        duration = int(time.time() - start_time)
        state_label.config(text=f"{text} | 已用时: {duration}s")
def on_key(event):
    global waiting_ack, ack_received
    if waiting_ack and event.name == '1' and event.event_type == 'down':
        ack_received = True
        log("🔄1 收到发端模拟输入的 '1'，准备进入下一轮")

keyboard.hook(on_key)

def start(log_area, state):
    global log_widget, state_label, waiting_ack, ack_received
    log_widget, state_label = log_area, state
    totalPages = int(config.Show_Code.split('x')[0]) * int(config.Show_Code.split('x')[1])
    log("收端启动，等待 START 帧...")
    seen_pages = set()
    receiving = False

    # 当前批次
    batch_no = 0
    current_batch_indexes = set()
    total_page_count = None
    while not receiving:
        for payload in decode_qr_multi():
            if payload.startswith("START"):
                receiving = True
                seen_pages.clear()
                parts = payload.split(":")
                if len(parts) == 2:
                    total_page_count = int(parts[1])
                    log(f"收到 START，总页数={total_page_count}")
                else:
                    total_page_count = None
                    log("收到 START，但未携带总页数")
                press_real_key_down('2')
                break

        time.sleep(0.1)

    while True:
        payloads = decode_qr_multi()
        if not payloads:
            log("当前没有检测到二维码，可能发端未激活或最小化")
            time.sleep(0.05)
            continue
        # pages_this_round = 0
        for payload in payloads:
            # if any(p == "END" for p in payloads):
            #     log("收到 END，准备结束")
            #     break
            if ":" in payload:
                try:
                    index_str, hexdata = payload.split(":")
                    index = int(index_str)
                    if index in seen_pages:
                        continue
                    seen_pages.add(index)
                    current_batch_indexes.add(index)
                    data = bytes.fromhex(hexdata)
                    write_data(index, data)
                    log(f"收到页 {index}, 大小={len(data)}")
                    set_state(f"接收页 {index}")
                except Exception as e:
                    log(f"解码失败: {e}")
                    # 期望页号
        if total_page_count is not None:
            start_index = batch_no * totalPages
            end_index = min(start_index + totalPages, total_page_count)
            expected_indexes = set(range(start_index, end_index))
        else:
            # 如果没有总页数就保留原来的逻辑
            expected_indexes = set(range(batch_no * totalPages, (batch_no + 1) * totalPages))
        # 判断是否批次收齐
        if expected_indexes.issubset(current_batch_indexes):
            if total_page_count is not None and len(seen_pages) >= total_page_count:
                log("所有页都收齐，准备结束")
                break
            log(f"批次 {batch_no} 全部收齐，准备翻页")
            waiting_ack = True
            ack_received = False
            log("📨 收端已解码完，发送 '2' 等待 '1' 确认")
            press_real_key_down('2')

            while not ack_received:
                time.sleep(0.05)

            press_real_key_up('2')
            log("收到 '1'，进入下一批解码")

            # 下一批
            batch_no += 1
            current_batch_indexes = set()
            waiting_ack = False
        # if "END" in payloads:
        #     break

    while not get_md5():
        time.sleep(0.1)
    log("接收完成，MD5: " + get_md5())
    set_state("接收完成")
