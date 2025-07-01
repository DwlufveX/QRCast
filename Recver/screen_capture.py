import pyautogui
from pyzbar.pyzbar import decode
import contextlib
import io

# 设定截图区域（根据你的发送窗口位置）
REGION = (100, 100, 800, 800)  # 调大以覆盖 2x2 多图区域

def decode_qr():
    try:
        img = pyautogui.screenshot(region=REGION)
        results = decode(img)
        if results:
            return results[0].data.decode()
    except Exception:
        pass
    return None

def decode_qr_multi():
    try:
        img = pyautogui.screenshot()
        # f = io.StringIO()
        # with contextlib.redirect_stderr(f):
        results = decode(img)
        # results = decode(img)
        return [r.data.decode() for r in results if r.data]
    except Exception:
        return []
