import random, hashlib
from flask import render_template, redirect, request, flash, get_flashed_messages
from sqlalchemy import and_

from moemoe import app, db
from moemoe.models import Image, User, Comment
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
def index():
    images = Image.query.order_by(db.desc(Image.id)).limit(10).all()
    return render_template('index.html', images=images)


@app.route('/image/<int:image_id>')
def image(image_id):
    image = Image.query.get(image_id)
    if image is None:
        return redirect('/')
    return render_template('pageDetail.html', image=image)


@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if image is None:
        redirect('/')
    return render_template('profile.html', user=user)


@app.route('/login.html')
def login_page():
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['login']):
        msg = msg + m
    return render_template('login.html', msg=msg, next=request.values.get('next'))


@app.route('/reg/', methods={'post'})
def reg():
    # request.args
    # request.form
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    # 来源页
    next = request.values.get('next').strip()

    if username == '' or password == '':
        return redirect_with_msg('/login.html', u'用户名或密码为空！', category='login')

    user = User.query.filter_by(username=username).first()
    if user is not None:
        return redirect_with_msg('/login.html', u'用户名已存在！', category='login')

    # 随机生成字符串给密码加盐
    # salt = '.'.join(random.sample('abcdefghijklmn1234567890'))
    # 使用用户名作为盐
    salt = '.'.join(username)
    md5 = hashlib.md5()
    md5.update((password+salt).encode("utf8"))
    new_password = md5.hexdigest()
    # 持久化到本地数据库
    user = User(username, new_password, get_image_url())
    db.session.add(user)
    db.session.commit()
    # 登陆用户
    login_user(user)
    if next is not None and next.startswith('/'):
        return redirect(next)
    return redirect('/')


@app.route('/login/', methods={'post'})
def login():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    # 来源页
    next = request.values.get('next').strip()

    if username == '' or password == '':
        return redirect_with_msg('/login.html', u'用户名或密码为空！', category='login')

    salt = '.'.join(username)
    md5 = hashlib.md5()
    md5.update((password + salt).encode('utf8'))
    new_password = md5.hexdigest()
    user = User.query.filter(and_(User.username == username, User.password == new_password)).first()
    if user is None:
        return redirect_with_msg('/login.html', u'用户名或密码错误！', category='login')
    login_user(user)
    if next is not None and next.startswith('/'):
        return redirect(next)
    return redirect('/')


@app.route('/logout/', methods={'post', 'get'})
def logout():
    logout_user()
    return redirect('/')


# 随机生成用户头像地址
def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'


# 带有flash信息的跳转
def redirect_with_msg(target, msg, category):
    if msg is not None:
        flash(msg, category=category)
    return redirect(target)