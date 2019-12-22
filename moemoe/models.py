from datetime import datetime
from moemoe import db, login_manager


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_date = db.Column(db.DateTime)
    comments = db.relationship('Comment')

    def __init__(self, url, user_id):
        self.url = url
        self.user_id = user_id
        self.create_date = datetime.now()

    def __repr__(self):
        return '<Image %d %s %d >' % (self.id, self.url, self.user_id)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1024))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Integer)  # 0 正常 1 删除
    user = db.relationship('User')

    def __init__(self, user_id, image_id, content):
        self.user_id = user_id
        self.image_id = image_id
        self.content = content
        self.status = 0

    def __repr__(self):
        return '<Comment %d %s %d >' % (self.id, self.content, self.image_id)


class User(db.Model):
    # __tablename__ = 'tablename'  可自定义表名，不定义则为实体类名小写
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32))
    head_url = db.Column(db.String(80))
    images = db.relationship('Image', backref='user', lazy='dynamic')

    def __init__(self, username, password, head_url):
        self.username = username
        self.password = password
        self.head_url = head_url

    def __repr__(self):
        return '<User %d %s>' % (self.id, self.username)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)