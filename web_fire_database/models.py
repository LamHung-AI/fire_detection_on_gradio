from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Users(Base):
    __tablename__ = "USERS"
    IDUser = Column(Integer, primary_key=True, autoincrement=True)
    HoTenUser = Column(String, nullable=False)
    TaiKhoan = Column(String, nullable=False, unique=True)
    MatKhau = Column(String, nullable=False)
    DiaChiCamera = Column(String)

    # Liên kết với bảng infomation
    infomations = relationship('Infomations', back_populates='user')

class Infomations(Base):
    __tablename__ = 'INFOMATIONS'
    IDInfo = Column(Integer, primary_key=True, autoincrement=True)
    IDUser = Column(Integer, ForeignKey('USERS.IDUser'), nullable=False)
    HoTenNguoiNhan = Column(String, nullable=False)
    SDT = Column(String, nullable=False)

    # Liên kết trở lại với bảng users
    user = relationship('Users', back_populates='infomations')