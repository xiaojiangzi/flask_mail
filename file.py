# -*- coding: UTF-8 -*-
from flask import Flask,render_template,request
from flask_mail import Mail,Message
import os

import os
classes_path = os.path.expanduser('./email.txt')
with open(classes_path,'r',encoding = 'UTF-8') as f:
    class_names = f.readlines()
class_names = [c.strip() for c in class_names]
print(class_names)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './file/'
# 文件位置
app.config.update(
    DEBUG = True,
    MAIL_SERVER = 'smtp.163.com',
    MAIL_PORT = 25,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = '',
    MAIL_PASSWORD = '',
    MAIL_DEBUG = True
)
# 邮箱地址
mail = Mail(app)

@app.route('/')
def upload_file():
    return render_template('file.html')
# 路由

@app.route("/",methods=["POST","GET"])
def file():
    if request.method == "POST":
        print("POST请求")
        f = request.files['file']
        if f == None:
            print("文件为空")
        else:
            print(f)
            title = ""
            # 标题
            msg = Message(title, sender='邮箱',recipients=class_names)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            msg.body = "以下是本次总结"
            # 正文
            with app.open_resource("./file/"+f.filename) as fp:
                msg.attach(f.filename, "file/", fp.read())
                    # 获取附件类型和附件位置
                    #上传附件
            mail.send(msg)
            # 发送邮件
            return "邮件发送成功"
            # 邮件分发
    else:
        print("GET请求")
        return render_template("file.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80)