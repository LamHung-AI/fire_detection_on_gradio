import gradio as gr
from web_fire_database.utils import *
from web_fire_database import models
from web_fire_database.database import engine
models.Base.metadata.create_all(bind=engine)


def flip(im):
    return im

def get_user_id():
    return id

with gr.Blocks() as demo:
    user_id = gr.State(id)
    gr.Markdown("""
    # Camera phát hiện đám cháy
    """)
    with gr.Tab("📸Camera"):
        with gr.Row():
            inp = gr.Image(sources=["webcam"], label="Input Image", type="numpy", width = 384, height=216, scale=1)
            out = gr.Image(label="Flipped Image", scale=2)
        inp.stream(fn=flip, inputs=inp, outputs=out)
    with gr.Tab('📂Lưu trữ'):
        li  = gr.Textbox()
    with gr.Tab('⚙️Tùy chỉnh'):
        gr.Markdown("# Xem tất cả thông tin")
        gr.Button().click(fn="")


demo.launch(auth = authentication, auth_message= "Đăng nhập")