import random
from sqlalchemy import or_, and_

from moemoe import app, db
from flask_script import Manager

from moemoe.models import User, Image, Comment
manager = Manager(app)


def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'


@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(0, 10):
        # 创建十个用户并提交
        db.session.add(User('user'+str(i), 'password', get_image_url()))
        db.session.commit()
        # 为每个用户创建一个作品并提交
        db.session.add(Image('/static/images/res/cat.jpg', i + 1))
        db.session.commit()
        # 为每个用户创建一个作品并提交
        db.session.add(Comment(i + 1, i + 1, '评论' + str(i+1)))
        db.session.commit()

    """  对数据库的一些基本操作
    # 查询全部
    print(1, User.query.all())
    user_id = 1
    print(1, User.query.get(user_id))
    # 带条件的查询
    print(2, User.query.filter_by(id=5).first())
    # 带有order by 的查询
    print(3, User.query.order_by(User.id.desc()).offset(1).limit(2).all())
    # 以某个标志结尾的查询 类似于SQL 的like查询
    print(4, User.query.filter(User.username.endswith('1')).limit(1).all())
    # 条件查询的 or 查询
    print(5, User.query.filter(or_(User.id == 1, User.id == 2)).all())
    # 条件查询的 and 查询
    print(6, User.query.filter(and_(User.id > 2, User.id < 5)).all())
    # 条件查询的 and 查询 返回第一个或者404错误
    print(7, User.query.filter(and_(User.id > 10, User.id < 15)).first_or_404())
    # 带有分页条件的查询
    print(8, User.query.order_by(User.id.desc()).paginate(page=1, per_page=5).items)

    # 修改信息
    user1 = User.query.filter_by(id=1).first()
    user1.username = '修改用户名1'
    db.session.commit()
    print(9, User.query.filter_by(id=1).first())

    # 删除数据
    comment = Comment.query.filter_by(id=1).first()
    db.session.delete(comment)
    db.session.commit()
    """


if __name__ == '__main__':
    manager.run()