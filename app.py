import gradio as gr


# sys.path.append(os.getcwd())
def authentication(a, p):
    return True


from fire_detection_on_gradio.web_fire_database import models
from fire_detection_on_gradio.web_fire_database import engine
models.Base.metadata.create_all(bind=engine)


def flip(im):
    return im

with gr.Blocks() as demo:
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
    with gr.Tab('⚙️Cài đặt'):
        k = gr.Textbox()

demo.launch(auth = authentication, auth_message= "Enter your username and password that you received in on Slack")