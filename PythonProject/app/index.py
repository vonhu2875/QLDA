import hashlib

from flask import render_template
from wtforms.validators import ValidationError
from app.model import User
import math
from datetime import datetime
from app import app, login
from flask import render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_user, logout_user, login_required, current_user
from unicodedata import category



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


@app.route('/login')
def login_view():
    return render_template('login.html')

@app.route('/login', methods=['post'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        user = auth_user(username=username, password=password)
        if user:
            login_user(user=user)
        next = request.args.get('next')
        return redirect(next if next else '/')
    except ValidationError as val:
        return render_template('login.html', err_msg=str(val))
    except ValidationError as dup:
        return render_template('login.html', err_msg=str(dup))
    except Exception as ex:
        return render_template('login.html', err_msg=str(ex))

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True)