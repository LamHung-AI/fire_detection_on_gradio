from fire_detection_on_gradio.web_fire_database.database import SessionLocal
from fire_detection_on_gradio.web_fire_database import models

db = SessionLocal()
class NoUser(Exception):
    pass

def authentication(account, password):
    try:

        user = db.query(models.Users).filter(models.Users.TaiKhoan == account, models.Users.MatKhau == password).first()
        if user is not None:
            user = user.__dict__
            id_user = user['IDUser']
            return (True)
        else:
            return (False)
    except Exception as e:
        print(f"error : {e}")

def add_info(id_user, hotennguoinhan, sdt):
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
            print('Đã thêm người dùng thành công!')
        else:
            print(f"Đã có nguoi dung voi sdt: {sdt}")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")


def delete_info(id_user, sdt):
    try:
        # Truy vấn thông tin người nhận theo id_nguoi_nhan
        info = db.query(models.Infomations).filter(models.Infomations.SDT == sdt).first()
        if info is not None:
            # Xóa thông tin người nhận nếu tìm thấy
            db.delete(info)
            db.commit()
            print(f"Đã xóa người nhận với sdt {sdt} thành công.")
        else:
            print(f"Không tìm thấy người nhận với sdt {sdt}.")
    except Exception as e:
        print(f"Lỗi khi xóa người nhận: {e}")
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
            raise NoUser("Không có người dùng này")
        user = user.__dict__
        all_people = db.query(models.Infomations).filter(models.Infomations.IDUser == id_user).all()
        all_people = list(map(clean_data,all_people))
        return (user['DiaChiCamera'], all_people)
    except Exception as e:
        print(f"error : {e}")

def change_password(id_user, new_password1, new_password2):
    try:
        if (new_password1 != new_password2):
            print("Mật khẩu mới và xác nhận mật khẩu phải giống nhau")
        else:
            user = db.query(models.Users).filter(models.Users.IDUser==id_user)
            if user.first() is None:
                raise NoUser("Không có người dùng này")
            user.update({"MatKhau": new_password1}, synchronize_session=False)
            db.commit()
            print("Cập nhật mật khẩu mới thành công!")
    except NoUser as e:
        print(f"Lỗi: {e}")
    except Exception as e:
        print(f"Lỗi : {e}")
print(list_info(2))