import hashlib
from datetime import datetime, timedelta

from flask_login import UserMixin
from sqlalchemy import Column, String, Enum, Float, Text, DateTime, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app import db, app
from enum import Enum as UserEnum
class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    active = db.Column(db.Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now)
    updated_date = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class UserRole(UserEnum):
    ADMIN = 1
    EMPLOYER = 2
    CANDIDATE = 3

class AppStatus(UserEnum):
    SUBMITTED = 1
    INTERVIEW = 2
    ACCEPTED = 3
    REJECTED = 4

class User(BaseModel, UserMixin):
    name = Column(String(255), nullable=False)
    #Thái hà sửa lại thuộc tính default cua avatar, đổi default thành none, để ai không up ảnh ava lên thì nó không đụng vào link,
    #còn up ảnh thì nó ghi đè link res cloudinary lên
    # avatar = Column(String(255),
    #                 default='https://res-console.cloudinary.com/dqrfckaek/thumbnails/transform/v1/image/upload/Y19maWxsLGhfMjAwLHdfMjAw/v1/bWFpbi1zYW1wbGVfZnB6Y3Vt/template_primary')
    avatar = Column(String(255),
                    default=None)

    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    user_role = Column(Enum(UserRole), nullable=False)
    phone = Column(String(15), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()

        # 1. Khởi tạo bảng
        db.create_all()


        # 3. Thêm Người dùng (User)
        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())

        admin = User(name="Quản trị viên", username="admin", password=password,
                     user_role=UserRole.ADMIN, phone="0123456789", email="admin@gmail.com")

        # Công ty chuyên CNTT, Thiết kế và Ngôn ngữ
        emp1 = User(name='Tập đoàn Công nghệ & Sáng tạo ABC', username='employer1', password=password,
                    user_role=UserRole.EMPLOYER, phone="0988123456", email="employer1@gmail.com")

        # Công ty chuyên Marketing và Thương mại điện tử
        emp2 = User(name='Agency Truyền thông Media XYZ', username='employer2', password=password,
                    user_role=UserRole.EMPLOYER, phone="0977123456", email="employer2@gmail.com")

        # Công ty chuyên Logistics và Kế toán (Dịch vụ doanh nghiệp)
        emp3 = User(name='Tổng công ty Vận tải & Tài chính Toàn Cầu', username='employer3', password=password,
                    user_role=UserRole.EMPLOYER, phone="0966123456", email="employer3@gmail.com")

        cand1 = User(name='Ứng viên 1', username='candidate1', password=password,
                     user_role=UserRole.CANDIDATE, phone="0123456789", email="candidate1@gmail.com")

        #Tạo thêm candidate cand2
        cand2 = User(name='Ứng viên 2', username='candidate2', password=password,
                     user_role=UserRole.CANDIDATE, phone="0223456789", email="candidate2@gmail.com")

        db.session.add_all([admin, emp1, emp2, emp3, cand1, cand2])
        db.session.flush()
        db.session.commit()