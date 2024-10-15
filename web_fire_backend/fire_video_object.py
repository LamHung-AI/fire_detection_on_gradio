import os
import cv2
import gc
import gradio as gr

from datetime import datetime
from fire_detection_on_gradio.web_fire_backend.utils import get_id_camera


class FireVideo:
    def __init__(self, user_id):
        self.user_id = user_id
        self.save_video = False
        self.images = []
        self.time = datetime.now()

    def __get_id_camera(self):
        return get_id_camera(self.user_id)

    def add_image(self, img):
        self.images.append(img)

    def __get_video_folder_path(self):
        fix_path = f"../web_fire_database/fire_video_storage/{self.user_id}/{self.__get_id_camera()}/"
        return fix_path

    def write_video(self):
        video_folder_path = self.__get_video_folder_path()
        os.makedirs(video_folder_path, exist_ok=True)
        fps = 2

        # Giả định tất cả ảnh đều có cùng kích thước, lấy kích thước từ ảnh đầu tiên
        print(len(self.images))
        height, width, layers = self.images[0].shape
        output_video_path = video_folder_path + str(self.time)+f'__id_camera_{get_id_camera(self.user_id)}' + ".mp4"


        # Định nghĩa codec và khởi tạo VideoWriter để lưu video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec 'mp4v' cho định dạng .mp4
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
        gr.Info('Video cháy đã được lưu lại thành công🎉️🎉', duration=3)