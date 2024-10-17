import pandas as pd
import gradio as gr
import os
from datetime import datetime

from fire_detection_on_gradio.web_fire_database.database import SessionLocal
from fire_detection_on_gradio.web_fire_database import models

db = SessionLocal()

def get_id_camera(user_id):
    id_camera = db.query(models.Camera).filter(models.Camera.IDUser == user_id).first()
    id_camera = id_camera.__dict__
    return id_camera['IDCamera']
def calculate_time_difference(time1, time2):
    # Định dạng thời gian
    time_format = "%H-%M-%S__%d-%m-%Y"

    # Chuyển đổi chuỗi thời gian thành đối tượng datetime
    t1 = datetime.strptime(time1, time_format)
    t2 = datetime.strptime(time2, time_format)

    difference = int(abs((t1 - t2).total_seconds()))

    return difference

def info_user(user_id):
    try:
        infor = db.query(models.Users).filter(models.Users.IDUser==user_id).first()
        infor = infor.__dict__
        HoTenUser = infor["HoTenUser"]
        NgaySinh = infor['NgaySinh']
        SDT = infor['SDT']
        Email = infor['Email']
        address = infor['DcChiTiet'] +" "+ infor['Phuong_Xa_Thon'] +" "+ infor['Quan_Huyen'] +" " + infor['Tinh_Tp']

        return HoTenUser, NgaySinh, SDT, Email, address
    except Exception as e:
        print(e)
        db.close()

def post_list_info(id_user):
    try:
        data = list_info(id_user)
        df = pd.DataFrame(data)

        # Đổi tên cột
        df = df.rename(columns={'HoTenNguoiNhan': 'Họ tên người nhận', 'SDT': 'SĐT'})

        # Đổi thứ tự cột để "Họ tên người nhận" ở vị trí đầu tiên
        df = df[['Họ tên người nhận', 'SĐT']]
        return df
    except Exception as e:
        print(e)
        raise gr.Error(f"Đã có lỗi xảy ra. Quý khách vui lòng thử lại sau 💥!", duration=3)
        db.close()

def authentication(account, password):
    try:

        user = db.query(models.Users).filter(models.Users.TaiKhoan == account, models.Users.MatKhau == password).first()
        if user is not None:
            user = user.__dict__
            return True, user["IDUser"]
        else:
            return False, None
    except:
        raise gr.Error(f"Đã có lỗi xảy ra. Quý khách vui lòng thử lại sau 💥!", duration=3)
        db.close()

def add_info(id_user, hotennguoinhan, sdt):
    if (not sdt.isdigit()) or (len(sdt) != 10):
        gr.Warning("Số điện thoại không hợp lệ📵. Xin vui lòng nhập lại số điện thoại khác❗", duration=3)
    else:
        people_info = {
            "IDUser" : id_user,
            "HoTenNguoiNhan" : hotennguoinhan,
            "SDT" : sdt
        }
        try:
            sdt_exist = db.query(models.Infomations).filter(models.Infomations.IDUser == id_user, models.Infomations.SDT == sdt).first()
            if sdt_exist is None:
                new_people_info = models.Infomations(**people_info)
                db.add(new_people_info)
                db.commit()
                gr.Info("Thêm người nhận thông báo mới thành công 🎉️🎉️", duration=3)
            else:
                gr.Warning(f"Đã có người nhận vói số điện thoại {sdt}📵. Quý khách vui lòng nhập số điện thoại khác❗", duration=3)
        except Exception:
            raise gr.Error(f"Đã có lỗi xảy ra. Quý khách vui lòng thử lại sau 💥!", duration=3)
            db.close()


def delete_info(id_user, sdt):
    if (not (sdt.isdigit())) or (len(sdt) != 10):
        gr.Warning("Số điện thoại không hợp lệ📵. Xin vui lòng nhập lại số điện thoại khác❗", duration=3)
        return
    try:
        # Truy vấn thông tin người nhận theo id_nguoi_nhan
        info = db.query(models.Infomations).filter(models.Infomations.IDUser==id_user, models.Infomations.SDT == sdt).first()
        if info is not None:
            # Xóa thông tin người nhận nếu tìm thấy
            db.delete(info)
            db.commit()
            gr.Info(f"Đã xóa người nhận với sdt {sdt} thành công🎉️🎉️🎉")
        else:
            gr.Warning(f"Không tìm thấy người nhận với sdt {sdt}❗")
    except :
        raise gr.Error(f"Đã có lỗi xảy ra. Quý khách vui lòng thử lại sau 💥!", duration=3)
        db.close()

def write_infor_video(user_id, camera_id, ten_video, thoi_gian, duong_dan):
    try:
        new_info_video = {
            "IDUser" : user_id,
            "IDCamera": camera_id,
            "TenVideo": ten_video,
            "Thoigian": thoi_gian,
            "DuongDan": duong_dan
        }

        write = models.VideoStore(**new_info_video)
        db.add(write)
        db.commit()
    except Exception as e:
        print(e)
        db.close()

def clean_data(people):
    people = people.__dict__
    people.pop('_sa_instance_state')
    people.pop('IDInfo')
    people.pop('IDUser')
    return people

def list_info(id_user):
    try:
        user = db.query(models.Users).filter(models.Users.IDUser == id_user).first()
        if user is None:
            gr.Warning("Không có người dùng này❗")
            return
        all_people = db.query(models.Infomations).filter(models.Infomations.IDUser == id_user).all()
        all_people = list(map(clean_data,all_people))
        return all_people
    except Exception as e:
        print(f"error : {e}")
        db.close()


def change_password(id_user, old_password, new_password1, new_password2):
    try:
        check_old_password = db.query(models.Users).filter(models.Users.MatKhau ==  old_password).first()
        if check_old_password is None:
            gr.Warning('Mật khẩu cũ không đúng❌❌')
            return
        if new_password1 != new_password2:
            gr.Warning("Mật khẩu mới và xác nhận mật khẩu phải giống nhau ❗", duration=3)
        else:
            user = db.query(models.Users).filter(models.Users.IDUser==id_user)
            if user.first() is None:
                gr.Warning("Không có người dùng này❗")
                return
            user.update({"MatKhau": new_password1}, synchronize_session=False)
            db.commit()
            gr.Info("Cập nhật mật khẩu mới thành công!🎉️🎉", duration=3)
    except:
        raise gr.Error(f"Đã có lỗi xảy ra. Quý khách vui lòng thử lại sau 💥!", duration=3)
    db.close()