from moemoe import app, db
from flask_script import Manager

from moemoe.models import User, Image, Comment
manager = Manager(app)


@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(0,10):
        # 创建十个用户并提交
        db.session.add(User('user'+str(i), 'password'))
        db.session.commit()
        # 为每个用户创建一个作品并提交
        db.session.add(Image('aaaa', i + 1))
        db.session.commit()
        # 为每个用户创建一个作品并提交
        db.session.add(Comment(i + 1, i + 1, '评论'))
        db.session.commit()


if __name__ == '__main__':
    manager.run()