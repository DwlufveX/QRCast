# def render_qr(data_bytes, target_label):
#     # 生成二维码
#     qr = qrcode.make(data_bytes)
#
#     # 确保图像为RGB模式
#     if qr.mode != 'RGB':
#         qr = qr.convert('RGB')
#
#     # 创建Tkinter兼容图像并关联到目标窗口
#     tk_img = ImageTk.PhotoImage(qr, master=target_label.winfo_toplevel())
#
#     # 更新标签并保留引用
#     target_label.config(image=tk_img)
#     target_label.image = tk_img
import qrcode
from PIL import Image, ImageTk

from Sender import config


def generate_qr_image(data, master=None):
    qr = qrcode.QRCode(border=1, box_size=10)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # # 获取 master 控件大小
    # if master is not None:
    #     master.update_idletasks()
    #     width = max(master.winfo_width(), 200)
    #     height = max(master.winfo_height(), 200)
    #     img = img.resize((width, height), Image.LANCZOS)
    img = img.resize((config.QR_WIDTH, config.QR_WIDTH), Image.LANCZOS)  # 固定大小
    return ImageTk.PhotoImage(img, master=master)
# def generate_qr_image(data_str, size=400, master=None):
#     qr = qrcode.QRCode(
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=1,
#         border=1,
#     )
#     qr.add_data(data_str)
#     qr.make(fit=True)
#     img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
#     img = img.resize((size, size), Image.NEAREST)
#
#     # ✅ 创建顶层绑定窗口：更安全（尤其防止 master 是 int 的情况）
#     if master and hasattr(master, "winfo_toplevel"):
#         master = master.winfo_toplevel()
#     else:
#         root = tk._default_root or tk.Tk()
#         master = root
#
#     return ImageTk.PhotoImage(img, master=master)
