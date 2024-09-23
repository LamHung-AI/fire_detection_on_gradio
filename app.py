import gradio as gr
import sys
import os
# sys.path.append(os.getcwd())
from utils.authentication import authentication


def flip(im):
    return im

with gr.Blocks() as demo:
    gr.Markdown("Nhóm 1 (65TTNT)")

    with gr.Row():
        inp = gr.Image(sources=["webcam"], label="Input Image", type="numpy", width = 384, height=216, scale=1)
        out = gr.Image(label="Flipped Image", scale=2)

    inp.stream(fn=flip, inputs=inp, outputs=out)

demo.launch(auth = authentication, auth_message= "Enter your username and password that you received in on Slack")