from fire_detection_on_gradio.web_fire_database.database import SessionLocal
from fire_detection_on_gradio.web_fire_database import models

db = SessionLocal()

def authentication(account, password):
    try:

        user = db.query(models.Users).filter(models.Users.TaiKhoan == account, models.Users.MatKhau == password).first()
        if user is not None:
            user = user.__dict__
            id_user = user['IDUser']
            return (True, id_user)
        else:
            return (False, None)
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

def all_people(id_user):
    try:
        all_users = db.query(models.Infomations).filter(models.Infomations.IDUser == id_user).all()
        if all_users is not None:
            all_users = list(map(clean_data,all_users))
            return all_users
        else:
            return None
    except Exception as e:
        print(f"error : {e}")

