"""
工具模块
"""
import random
import string
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from PIL import Image, ImageFont, ImageDraw, ImageFilter


def rnd_color():
    # 随机颜色
    return random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)


def gene_text():
    # 生成4位验证码
    return ''.join(random.sample(string.ascii_letters + string.digits, 4))


def draw_lines(draw, num, width, height):
    # 划线
    for num in range(num):
        x1 = random.randint(0, width / 2)
        y1 = random.randint(0, height / 2)
        x2 = random.randint(0, width)
        y2 = random.randint(height / 2, height)
        draw.line(((x1, y1), (x2, y2)), fill='black', width=1)


def get_verify_code():
    # 生成验证码图形
    code = gene_text()
    # 图片大小120×50
    width, height = 120, 50
    # 新图片对象
    im = Image.new('RGB', (width, height), 'white')
    # 字体
    font = ImageFont.truetype('static/fonts/Arial.ttf', 40)
    # draw对象
    draw = ImageDraw.Draw(im)
    # 绘制字符串
    for item in range(4):
        draw.text((5 + random.randint(-3, 3) + 23 * item, 5 + random.randint(-3, 3)),
                  text=code[item], fill=rnd_color(), font=font)
    # 划线
    draw_lines(draw, 2, width, height)
    # 高斯模糊
    im = im.filter(ImageFilter.GaussianBlur(radius=1.5))
    return im, code


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_email():
    from_addr = 'moe_noreply@163.com'
    password = 'moemoe961753'
    to_addr = '1559237979@qq.com'
    smtp_server = 'smtp.163.com'

    msg = MIMEText('<html><body>' +
                   '<p>尊敬的用户,您好！</p>' +
                   '<p>&emsp;&emsp;感谢您注册萌图网账号。</p>' +
                   '<p>&emsp;&emsp;请点击以下链接进行邮箱验证，以便开始使用您的萌图网账户：</p>' +
                   '<p>&emsp;&emsp;<a href="https://portal.qiniu.com/api/gaea/email/confirm?' +
                   'd=MTU1OTIzNzk3OUBxcS5jb20%3D&m=A5ne-VAoKVEsdMag0IqcBkYjeZk%3D">点击验证</a></p>' +
                   '<p>&emsp;&emsp;如果您无法点击以上链接，请复制以下网址到浏览器里直接打开：</p>' +
                   '<p>&emsp;&emsp;https://portal.qiniu.com/api/gaea/email/confirm?d=MTU1OTIzNzk3OUBxcS5jb20%3D&m=A5ne-VAoKVEsdMag0IqcBkYjeZk%3D</p>' +
                   '<img src="https://www.uxahz.com//skin/default/images/cent.png" width="1140" height="120" border="0">' +
                   '</body></html>', 'html', 'utf-8')

    # msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
    msg['From'] = _format_addr('萌图网<%s>' % from_addr)
    msg['To'] = _format_addr('<%s>' % to_addr)
    msg['Subject'] = Header('萌图网邮箱验证', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


if __name__ == '__main__':
    send_email()
