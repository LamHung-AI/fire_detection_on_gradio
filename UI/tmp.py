import gradio as gr

# Tạo hàm phát lại âm thanh
def play_audio():
    return "../storage_project/fire_warning.mp3"  # Trả về đường dẫn file âm thanh

# Tạo giao diện Gradio
audio_player = gr.Audio(value=play_audio, autoplay=True, label="Audio Player")

# Khởi tạo Gradio Interface và chạy chương trình
demo = gr.Interface(
    fn=play_audio,  # Hàm phát lại âm thanh
    inputs=None,    # Không cần input từ người dùng
    outputs=audio_player  # Hiển thị thành phần phát âm thanh
)

if __name__ == "__main__":
    demo.launch()
