import sys
import redis
import pymysql
import subprocess
from flask_cors import CORS
from flask import render_template,redirect
from flask import Flask,request,Response,jsonify

app = Flask(__name__)
CORS(app, resources=r'/*')


redisCli = redis.Redis(host=redisDb, port=6039, decode_responses=True, db=0)  


@app.route('/applyupload')
def Upload():
    FIN = request.args.get("FIN")
    time = request.args.get("time")
    expiredTime = request.args.get("expired")
    nameSpace = request.args.get("nameSpace")
    fileName = request.args.get("fileName")
    # 接下来先检查是否存在FIN, 没有则将文件信息写入数据库[Mysql]
    # 返回准许上传的临时Url
    result = subprocess.check_output("mc share upload minio/test/", shell=True)


@app.route('/applydownload')
def Download():
    pass

@app.before_request
def redirect():
    token = request.headers['token']
    ipaddr = request.headers['ipaddress']
    ip = request.remote_addr
    if ip != ipaddr or token == None or token == '':
        return {"statusCode":"404", 
                "body": json.dumps('Forbiden Request.')}
    else:
        if redisCli.get(token):
            pass



