from flask import Blueprint, jsonify
from flask import request

from web.dao.ip_dao import IPDao

blue = Blueprint('IpApi', __name__)

dao = IPDao()


@blue.route('/')
def index():
    return '<h2>Welcome to My Proxy Pool</h2>'


# 获取当前速度最快的代理
@blue.route('/ip/', methods=('GET',))
def proxy_ip():
    anonymity = request.args.get('anonymity', 1)
    protocol = request.args.get('protocol', 'http')
    count = request.args.get('count', 1)

    result = dao.query(**{
        'protocol': protocol,
        'anonymity': anonymity,
        'count': count
    })
    return jsonify(result)


# 保存代理信息或者更新代理信息的接口
@blue.route('/ip/', methods=('POST', 'PUT'))
def save_ip():
    # 表单参数： protocol 代理类型 ip_port ip+端口 isanonymous 是否匿名 livetime 存活时间 testtime 验证时间
    protocol = request.form.get('protocol')
    ip = request.form.get('ip')
    port = request.form.get('port')
    anonymity = request.form.get('anonymity')
    score = request.form.get('score')
    msg = ''
    if request.method == 'POST':
        dao.insert(**{
            'ip': ip,
            'port': port,
            'protocol': protocol,
            'anonymity': anonymity,
            'score': score
        })
        msg = '添加数据成功'
    elif request.method == 'PUT':
        dao.update(**{
            'ip': ip,
            'port': port,
            'protocol': protocol,
            'anonymity': anonymity,
            'score': score
        })
        msg = '更新数据成功'
    return jsonify({'code': 200, 'msg': msg})


# 查询所有ip信息的接口
@blue.route('/ip/all/', methods=('GET',))
def query():
    result = dao.query_all()
    return jsonify(result)


# 删除代理信息的接口
@blue.route('/ip/<string:ip>/', methods=('DELETE',))
def delete(ip):
    dao.delete(ip)
    return jsonify({
        'code': 300,
        'msg': '删除成功'
    })
