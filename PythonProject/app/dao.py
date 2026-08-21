import hashlib
from sqlite3 import IntegrityError

from wtforms.validators import ValidationError

from app.model import User, UserRole
from app import db
import re

def add_user(name, username, password, avatar, email, phone, user_role):
    username = username.strip()

    # Kiểm tra username
    if len(username) < 5 or len(username) > 20:
        raise ValidationError("Username phải từ 5 đến 20 ký tự!")

    # \s thay vì chỉ để [ ] là để thay cho cả khoảng trắng, các dấu tab xuống dòng
    if re.search(r'\s', username):
        raise ValidationError("Username không được chứa khoảng trắng!")

    if not re.match(r'^[a-zA-Z0-9]+$', username):
        raise  ValidationError("Username không được chứa ký tự đặc biệt")

    # Kiểm tra password
    if len(password) < 8:
        raise ValidationError('Password phải ít nhất 8 ký tự')
    if not re.search(r'[0-9]', password):
        raise ValidationError('Password phải chứa số')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password phải chứa ký tự hoa')
    if not re.search(r'[a-z]', password):
        raise ValidationError('Password phải chứa ký tự')
    #Kiểm tra email
    email_regrex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regrex, email):
        raise ValidationError("Email không đúng định dạng!")

    #Kiểm tra name
    if not name or not name.strip():
        raise ValidationError("Vui lòng nhập tên!")
    if len(name) > 255:
        raise ValidationError("Tên không được quá 255 ký tự!")

    #Kiểm tra user_role
    if user_role is None:
        raise ValidationError("Vai trò không được để trống!")

    if user_role not in [UserRole.EMPLOYER, UserRole.CANDIDATE]:
        raise ValidationError("Vai trò không hợp lệ")

    #Kiểm tra sdt
    if phone is None:
        raise ValidationError("Bắt buộc nhập số điện thoại!")

    if len(phone) > 15:
        raise ValidationError("Số điện thoại chỉ được nhập tối đa 15 ký tự")

    if not re.match(r'^[0-9]+$', phone):
        raise ValidationError("Số điện thoại không hợp lệ!")

    #Kiểm tra phía dưới db username
    if User.query.filter(User.username.__eq__(username)).first():
        raise ValidationError(f'Username {username} đã tồn tại')

    # Kiểm tra phía dưới db email
    if User.query.filter(User.email.__eq__(email)).first():
        raise ValidationError(f'Email {email} đã tồn tại')

    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name = name.strip(), username=username.strip(), password=password, email=email, phone=phone, user_role=user_role)

    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise Exception("Không thể thêm user!")
    return u


def auth_user(username, password):
    if not username:
        raise ValidationError("Vui lòng nhập username!")
    if not password:
        raise ValidationError("Vui lòng nhập mật khẩu!")
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u = User.query.filter(User.username == username).first()
    if not u:
        raise ValidationError("Sai tên đăng nhập hoặc sai mật khẩu!")
    if password != u.password:
        raise ValidationError("Sai tên đăng nhập hoặc sai mật khẩu!")
    if not u.active:
        raise ValidationError("Tài khoản người dùng không tồn tại!")
    return u
