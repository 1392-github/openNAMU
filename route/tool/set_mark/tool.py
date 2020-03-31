import urllib.parse
import datetime
import hashlib
import flask
import re

def get_time():
    return str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))

def db_data_get(data):
    global set_data
    set_data = data

def db_change(data):
    if set_data == 'mysql':
        data = data.replace('random()', 'rand()')
        data = data.replace('%', '%%')
        data = data.replace('?', '%s')

    return data

def ip_check(d_type = 0):
    ip = ''
    if d_type == 0 and (flask.session and ('state' and 'id') in flask.session):
        ip = flask.session['id']
    
    if ip == '':
        try:
            ip = flask.request.environ.get('HTTP_X_REAL_IP', flask.request.environ.get('HTTP_X_FORWARDED_FOR', flask.request.remote_addr))
            ip = ip[0] if type(ip) == type([]) else ip

            if ip == '::1' or ip == '127.0.0.1':
                ip = flask.request.environ.get('HTTP_X_FORWARDED_FOR', flask.request.remote_addr)
                ip = ip[0] if type(ip) == type([]) else ip
        except:
            ip = 'error:ip'

    return str(ip)

def savemark(data):
    data = re.sub("\[date\(now\)\]", get_time(), data)

    ip = ip_check()
    name = '[[user:' + ip + '|' + ip + ']]' if not re.search("\.|:", ip) else ip

    data = re.sub("\[name\]", name, data)

    return data

def url_pas(data):
    return urllib.parse.quote(data).replace('/','%2F')

def sha224_replace(data):
    return hashlib.sha224(bytes(data, 'utf-8')).hexdigest()

def md5_replace(data):
    return hashlib.md5(data.encode()).hexdigest()
