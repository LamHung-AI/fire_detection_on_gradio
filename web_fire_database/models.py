from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Users(Base):
    __tablename__ = "USERS"
    IDUser = Column(Integer, primary_key=True, autoincrement=True)
    HoTenUser = Column(String, nullable=False)
    TaiKhoan = Column(String, nullable=False, unique=True)
    MatKhau = Column(String, nullable=False)
    NgaySinh = Column(DateTime)
    SDT = Column(String,nullable=False)
    Email = Column(String,nullable=False)
    DcChiTiet = Column(String)
    Phuong_Xa_Thon = Column(String,nullable=False)
    Quan_Huyen = Column(String,nullable=False)
    Tinh_Tp = Column(String,nullable=False)

    # Liên kết với các bảng khác
    infomations = relationship('Infomations', back_populates='user')
    cameras = relationship('Camera', back_populates='user')
    videos = relationship('VideoStore', back_populates='user')

class Infomations(Base):
    __tablename__ = 'INFOMATIONS'
    IDInfo = Column(Integer, primary_key=True, autoincrement=True)
    IDUser = Column(Integer, ForeignKey('USERS.IDUser'), nullable=False)
    HoTenNguoiNhan = Column(String, nullable=False)
    SDT = Column(String, nullable=False)

    # Liên kết trở lại với bảng users
    user = relationship('Users', back_populates='infomations')

class Camera(Base):
    __tablename__ = "CAMERA"
    IDCamera = Column(Integer, primary_key=True, autoincrement=True)
    IDUser = Column(Integer, ForeignKey('USERS.IDUser'), nullable=False)
    DcChiTiet = Column(String)
    Phuong_Xa_Thon = Column(String,nullable=False)
    Quan_Huyen = Column(String,nullable=False)
    Tinh_Tp = Column(String,nullable=False)

    user = relationship('Users', back_populates='cameras')

class VideoStore(Base):
    __tablename__ = "VIDEOSTORE"
    IDVideo = Column(Integer, primary_key=True, autoincrement=True)
    IDCamera = Column(Integer, ForeignKey('CAMERA.IDCamera'), nullable=False)
    IDUser = Column(Integer, ForeignKey('USERS.IDUser'), nullable=False)
    TenVideo = Column(String)
    Thoigian = Column(String)
    DuongDan = Column(String)

    user = relationship('Users', back_populates='videos')
    camera = relationship('Camera')