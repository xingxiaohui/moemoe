from qiniu import Auth, put_stream, put_data
import os
from moemoe import app

# 需要填写你的 Access Key 和 Secret Key
access_key = app.config['QINIU_ACCESS_KEY']
secret_key = app.config['QINIU_SECRET_KEY']
# 构建鉴权对象
q = Auth(access_key, secret_key)
# 要上传的空间
bucket_name = app.config['QINIU_BUCKET_NAME']
domain_prefix = app.config['QINIU_DOMAIN']


def qiniu_upload_file(source_file, save_file_name):
    q = Auth(access_key, secret_key)
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, save_file_name)
    ret, info = put_data(token, save_file_name, data=source_file.read())

    if info.status_code == 200:
        return domain_prefix + save_file_name
    return None
