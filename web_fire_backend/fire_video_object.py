import os
import cv2
import gc
import gradio as gr

from datetime import datetime
from fire_detection_on_gradio.web_fire_backend.utils import get_id_camera, write_infor_video


class FireVideo:
    def __init__(self, user_id):
        self.user_id = user_id
        self.save_video = False
        self.images = []
        self.time = datetime.now().strftime("%H-%M-%S__%d-%m-%Y")
        self.fire_video_paths = []

    def __get_id_camera(self):
        return get_id_camera(self.user_id)

    def add_image(self, img):
        self.images.append(img)

    def get_video_folder_path(self):
        fix_path = f"../web_fire_database/fire_video_storage/{self.user_id}/{self.__get_id_camera()}/"
        return fix_path

    def update_fire_videos_paths(self):
        directory = self.get_video_folder_path()
        self.fire_video_paths = [os.path.join(directory, file) for file in os.listdir(directory)
                                 if file.endswith(('.mp4', '.avi', '.mov', '.mkv', 'webm'))]

    def write_video(self):
        video_folder_path = self.get_video_folder_path()
        os.makedirs(video_folder_path, exist_ok=True)
        fps = 2

        # Giả định tất cả ảnh đều có cùng kích thước, lấy kích thước từ ảnh đầu tiên
        print(len(self.images))
        height, width, layers = self.images[0].shape
        ten_video = str(self.time)+f'__id_camera_{get_id_camera(self.user_id)}' + ".webm"
        output_video_path = video_folder_path + ten_video


        # Định nghĩa codec và khởi tạo VideoWriter để lưu video
        fourcc = cv2.VideoWriter_fourcc(*'vp90')
        # fourcc = cv2.VideoWriter_fourcc(*'X264')  # Codec 'H264' cho định dạng .mp4 để hiển thị lên web
        video = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
        print(len(self.images))
        # Thêm từng ảnh (dưới dạng BGR) vào video
        for image in self.images:
            video.write(image)

        # Giải phóng bộ nhớ
        video.release()
        del self.images
        gc.collect()
        self.images = []
        self.save_video = False
        self.update_fire_videos_paths()
        write_infor_video(self.user_id, get_id_camera(self.user_id), ten_video, self.time, output_video_path)
        print("Lưu video thành công")
        gr.Info('Video cháy đã được lưu lại thành công🎉️🎉', duration=3)