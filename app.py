import gradio as gr
import pandas as pd
from PIL.ImageOps import scale

from web_fire_database.utils import *
from web_fire_database import models
from web_fire_database.database import engine
models.Base.metadata.create_all(bind=engine)

id_now = str(2)
def flip(im):
    return im

def post_list_info(id_user):
    address, data = list_info(id_user)
    df = pd.DataFrame(data)

    # Đổi tên cột
    df = df.rename(columns={'HoTenNguoiNhan': 'Họ tên người nhận', 'SDT': 'SĐT'})

    # Đổi thứ tự cột để "Họ tên người nhận" ở vị trí đầu tiên
    df = df[['Họ tên người nhận', 'SĐT']]
    return address, df
with gr.Blocks() as demo:
    gr.Markdown("""
    # Camera phát hiện đám cháy
    """)
    with gr.Tab("📸Camera"):
        with gr.Row():
            inp = gr.Image(sources=["webcam"], label="Input Image", show_label=True, type="numpy", width = 384, height=216, scale=1)
            out = gr.Image(label="Flipped Image", show_label=True, scale=2)
        inp.stream(fn=flip, inputs=inp, outputs=out)
    with gr.Tab('📂Lưu trữ'):
        li  = gr.Textbox()
    with gr.Tab('⚙️Tùy chỉnh'):
        gr.Markdown("# Xem tất cả thông tin")
        gr.Button("Xem thông tin").click(fn=post_list_info,
                          inputs=gr.Textbox(value = id_now, visible=False),
                          outputs=[gr.Textbox(label="Địa chỉ camera", show_label=True),
                                   gr.DataFrame(label="Thông tin người nhận thông báo cháy", show_label=True)])

        gr.Markdown("# Thêm thông tin người nhận thông báo cháy")
        with gr.Row():
            ho_ten_nguoi_nhan = gr.Textbox(label="Họ tên người nhận mới", show_label=True, placeholder="Nhập họ tên người nhận mới", scale=1)
            sdt = gr.Textbox(label="Số điện thoại người nhận", show_label=True, placeholder="Nhâp số điện thoại",scale=1)
        gr.Button("Thêm người nhận thông báo").click(fn=add_info,
                                                     inputs=[gr.Textbox(value = id_now, visible=False), ho_ten_nguoi_nhan, sdt])

demo.launch(auth = authentication, auth_message= "Đăng nhập")