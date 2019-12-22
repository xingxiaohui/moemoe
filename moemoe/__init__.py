from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# 初始化 Flask 框架
app = Flask(__name__)
# 读取配置信息
app.config.from_pyfile('app.conf')
# 增加 jinja 语法拓展
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
# 初始化 Flash-Massage 使用的密钥
app.secret_key = 'moe-moe-2019-12-22-15-38-06-v-0-0-1'
# 初始化 SQLAlchemy
db = SQLAlchemy(app)
# 初始化 Flask-Login
login_manager = LoginManager(app)
# 配置无权限用户的登录入口
login_manager.login_view = '/login.html'


from moemoe import models, views
