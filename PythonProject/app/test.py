import hashlib

import pytest
from wtforms.validators import ValidationError

from app.dao import auth_user, add_user
from app.model import UserRole
from app import db

from datetime import datetime, timedelta

import pytest
import hashlib
from cloudinary import uploader
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['PAGE_SIZE'] = 2
    app.config['TESTING'] = True
    app.secret_key = "nnasidhfona@@()s*(&^&%&^%i103498"

    db.init_app(app)

    return app

@pytest.fixture
def test_app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def test_client(test_app):
    return test_app.test_client()

@pytest.fixture
def test_session(test_app):
    yield db.session
    db.session.rollback()

def test_success(test_session):
    add_user(name='Võ Thị Bích Như', username='a' * 5, password='4aA' * 3, avatar=None, email='abc@gmail.com',
             phone='0123456789', user_role=UserRole.CANDIDATE)
    a = auth_user(username='a' * 5, password="4aA" * 3)
    assert a is not None
    assert a.username == 'a' * 5
    assert a.password == str(hashlib.md5(('4aA' * 3).encode('utf-8')).hexdigest())

def test_empty_username(test_session):
    with pytest.raises(ValidationError, match="Vui lòng nhập username!"):
        a = auth_user(username='', password="4aA" * 3)

def test_empty_password(test_session):
    with pytest.raises(ValidationError, match="Vui lòng nhập mật khẩu!"):
        a = auth_user(username='a' * 5, password='')


def test_invalid_username(test_session):
    add_user(name='Võ Thị Bích Như', username='a' * 5, password='4aA' * 3, avatar=None, email='abc@gmail.com',
             phone='0123456789', user_role=UserRole.CANDIDATE)
    with pytest.raises(ValidationError, match="Sai tên đăng nhập hoặc sai mật khẩu!"):
        auth_user(username='a' * 6, password="4aA" * 3)


def test_invalid_password(test_session):
    add_user(name='Võ Thị Bích Như', username='a' * 5, password='4aA' * 3, avatar=None, email='abc@gmail.com',
             phone='0123456789', user_role=UserRole.CANDIDATE)
    with pytest.raises(ValidationError, match="Sai tên đăng nhập hoặc sai mật khẩu!"):
        auth_user(username='a' * 5, password="4aA" * 4)


def test_not_exist_user(test_session):
    with pytest.raises(ValidationError, match="Sai tên đăng nhập hoặc sai mật khẩu!"):
        auth_user(username='a' * 5, password="4aA" * 4)




