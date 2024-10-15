import gradio as gr
from ultralytics import YOLO

from fire_detection_on_gradio.web_fire_backend.utils import *
from fire_detection_on_gradio.web_fire_database.database import engine
from fire_detection_on_gradio.web_fire_database import models
from fire_detection_on_gradio.web_fire_backend.fire_video_object import FireVideo

models.Base.metadata.create_all(bind=engine)
fire_detection = YOLO('../storage_project/fire_detection.pt')

video_fire = {}

with gr.Blocks(theme='soft') as demo:
    gr.Markdown("""
    # Camera phát hiện đám cháy
    """)
    current_id_user= gr.State()

    def login(account, password):
        global current_id_user
        is_success , id_now = authentication(account, password)
        current_id_user = id_now
        if is_success:
            gr.Info("Đăng nhập thành công 🎉️🎉", duration=3)
            return [gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), current_id_user]
        else:
            gr.Warning('Tài khoản hoặc mật khẩu không đúng❌', duration=3)
            return [gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), None]

    def get_current_id_user():
        return str(current_id_user)

    tab_camera = gr.Tab('📸Camera', visible=False)
    tab_luu_tru = gr.Tab('📂Lưu trữ', visible=False)
    tab_tuy_chinh = gr.Tab("⚙️Tùy chỉnh", visible=False)
    tab_dang_nhap = gr.Tab("Đăng nhập")

    user_id = gr.Textbox(visible=False)
    user_id.change(fn=get_current_id_user, outputs=user_id)


    def detection(img):
        global video_fire, user_id
        config = 0.57
        results = fire_detection.predict(source=img, conf=config)
        annotated_img = results[0].plot()

        prob = results[0].boxes.conf.cpu().numpy()
        print(prob)
        if len(prob) == 0:
            prob = [0]

        if user_id not in video_fire:
            video_fire[user_id] = FireVideo(get_current_id_user())

        if max(prob) > config:
            time_now = datetime.now().strftime("%H-%M-%S__%d-%m-%Y")
            video_fire[user_id].save_video = True
            video_fire[user_id].time = time_now

        if video_fire[user_id].save_video is True:
            video_fire[user_id].add_image(annotated_img)
            print(len(video_fire[user_id].images))

        time_now = datetime.now().strftime("%H-%M-%S__%d-%m-%Y")
        if (calculate_time_difference(video_fire[user_id].time, time_now) > 20) and (video_fire[user_id].save_video is True):
            video_fire[user_id].write_video()

        annotated_img_rgb = annotated_img[..., ::-1]
        return annotated_img_rgb

    with tab_dang_nhap:
        username = gr.Textbox(label="Tên đăng nhập", placeholder="Nhập tên đăng nhập", show_label=True)
        passwd = gr.Textbox(label="Mật khẩu", type="password", placeholder="Nhập mật khẩu tại đây", show_label=True)
        login_button = gr.Button("Đăng nhập")
        login_button.click(fn = login, inputs=[username, passwd], outputs=[tab_camera, tab_luu_tru, tab_tuy_chinh, user_id])

    with tab_camera:
        with gr.Row():
            inp = gr.Image(sources=["webcam"], label="Camera thường", show_label=True, type="pil", width = 384, height=216, scale=1)
            out = gr.Image(label="Camera phát hiện đám cháy", show_label=True, scale=2)
        inp.stream(fn=detection, inputs=inp, outputs=out)

    with tab_luu_tru:
        out_id = gr.Textbox()
        # gr.Button().click(fn=get_current_id_user, outputs=[out_id])

    with tab_tuy_chinh:
        gr.Markdown("# Xem tất cả thông tin ")
        gr.Button("Xem thông tin").click(fn=post_list_info,
                                        inputs=user_id,
                                        outputs=[gr.DataFrame(label="Thông tin người nhận thông báo cháy", show_label=True)]
                                         )

        gr.Markdown("# Thêm thông tin người nhận thông báo cháy")
        with gr.Row():
            ho_ten_nguoi_nhan = gr.Textbox(label="Họ tên người nhận mới", show_label=True, placeholder="Nhập họ tên người nhận mới", scale=1)
            sdt = gr.Textbox(label="Số điện thoại người nhận", show_label=True, placeholder="Nhâp số điện thoại",scale=1)
        gr.Button("Thêm người nhận thông báo").click(fn=add_info,
                                                     inputs=[user_id, ho_ten_nguoi_nhan, sdt])
        gr.Markdown("# Xóa thông tin người nhận báo cháy")
        delete_sdt = gr.Textbox(label="Số điện thoại người nhận cần xóa", show_label=True, placeholder="Nhâp số điện thoại người")
        gr.Button('Xóa người nhận thông báo này').click(fn=delete_info,
                                                        inputs=[user_id, delete_sdt]
                                                        )

        gr.Markdown("# Đổi mật khẩu")
        password1 = gr.Textbox(label="Mật khẩu mới", show_label=True,
                             placeholder="Nhâp mật khẩu mới", type="password")
        password2 = gr.Textbox(label="Nhập lại mật khẩu mới", show_label=True,
                               placeholder="Nhâp lại mật khẩu mới", type="password")
        gr.Button('Đổi mật khẩu').click(fn=change_password,
                                        inputs=[user_id, password1, password2]
                                        )
demo.launch()
