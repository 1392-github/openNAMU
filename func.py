﻿from bottle import request, app
from bottle.ext import beaker
import json
import sqlite3

json_data = open('set.json').read()
set_data = json.loads(json_data)

conn = sqlite3.connect(set_data['db'] + '.db')
curs = conn.cursor()
    
session_opts = {
    'session.type': 'file',
    'session.data_dir': './app_session/',
    'session.auto': 1
}

app = beaker.middleware.SessionMiddleware(app(), session_opts)

from mark import *

def other2(d):
    g = 0
    session = request.environ.get('beaker.session')
    if(session.get('View_List')):
        m = re.findall('(?:(?:([^\n]+)\n))', session.get('View_List'))
        if(m):
            g = ''
            for z in m[-6:-1]:
                g += '<a href="/w/' + url_pas(z) + '">' + z + '</a> / '
            g = re.sub(' / $', '', g)
            
    r = d + [g]
    return(r)

def wiki_set(num):
    if(num == 1):
        r = []

        curs.execute('select data from other where name = ?', ['name'])
        d = curs.fetchall()
        if(d):
            r += [d[0][0]]
        else:
            r += ['무명위키']

        curs.execute('select data from other where name = "license"')
        d = curs.fetchall()
        if(d):
            r += [d[0][0]]
        else:
            r += ['CC 0']

        return(r)

    if(num == 2):
        d = '위키:대문'
        curs.execute('select data from other where name = "frontpage"')
    elif(num == 3):
        d = '2'
        curs.execute('select data from other where name = "upload"')
    
    r = curs.fetchall()
    if(r):
        return(r[0][0])
    else:
        return(d)

def diff(seqm, num):
    output= []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if(opcode == 'equal' and num == 1):
            output.append(seqm.a[a0:a1])
        elif(opcode == 'insert' and num == 0):
            output.append("<span style='background:#CFC;'>" + seqm.b[b0:b1] + "</span>")
        elif(opcode == 'delete' and num == 1):
            output.append("<span style='background:#FDD;'>" + seqm.a[a0:a1] + "</span>")
        elif(opcode == 'replace'):
            if(num == 1):
                output.append("<span style='background:#FDD;'>" + seqm.a[a0:a1] + "</span>")
            else:
                output.append("<span style='background:#CFC;'>" + seqm.b[b0:b1] + "</span>")
        elif(num == 0):
            output.append(seqm.b[b0:b1])
            
    return(''.join(output))
           
def admin_check(num, what):
    ip = ip_check() 
    curs.execute("select acl from user where id = ?", [ip])
    user = curs.fetchall()
    if(user):
        reset = 0
        while(1):
            if(num == 1 and reset == 0):
                check = 'ban'
            elif(num == 2 and reset == 0):
                check = 'mdel'
            elif(num == 3 and reset == 0):
                check = 'toron'
            elif(num == 4 and reset == 0):
                check = 'check'
            elif(num == 5 and reset == 0):
                check = 'acl'
            elif(num == 6 and reset == 0):
                check = 'hidel'
            else:
                check = 'owner'

            curs.execute('select name from alist where name = ? and acl = ?', [user[0][0], check])
            acl_data = curs.fetchall()
            if(acl_data):
                if(what):
                    curs.execute("insert into re_admin (who, what, time) values (?, ?, ?)", [ip, what, get_time()])
                    conn.commit()

                return(1)
            else:
                if(reset == 0):
                    reset = 1
                else:
                    break

def ip_pas(raw_ip):
    if(re.search("(\.|:)", raw_ip)):
        ip = raw_ip
    else:
        curs.execute("select title from data where title = ?", ['사용자:' + raw_ip])
        data = curs.fetchall()
        if(data):
            ip = '<a href="/w/' + url_pas('사용자:' + raw_ip) + '">' + raw_ip + '</a>'
        else:
            ip = '<a class="not_thing" href="/w/' + url_pas('사용자:' + raw_ip) + '">' + raw_ip + '</a>'
            
    ip += ' <a href="/record/' + url_pas(raw_ip) + '">(기록)</a>'

    return(ip)

def custom():
    session = request.environ.get('beaker.session')
    try:
        d1 = format(session['Daydream'])
    except:
        d1 = ''

    try:
        d2 = format(session['AQUARIUM'])
    except:
        d2 = ''

    if(session.get('Now') == 1):
        curs.execute('select name from alarm limit 1')
        if(curs.fetchall()):
            d3 = 2
        else:
            d3 = 1
    else:
        d3 = 0

    return([d1, d2, d3])

def acl_check(name):
    ip = ip_check()
    band = re.search("^([0-9]{1,3}\.[0-9]{1,3})", ip)
    if(band):
        band_it = band.groups()
    else:
        band_it = ['Not']

    curs.execute("select block from ban where block = ? and band = 'O'", [band_it[0]])
    band_d = curs.fetchall()

    curs.execute("select block from ban where block = ?", [ip])
    ban_d = curs.fetchall()
    if(band_d or ban_d):
        return(1)

    acl_c = re.search("^사용자:([^/]*)", name)
    if(acl_c):
        acl_n = acl_c.groups()

        if(admin_check(5, None) == 1):
            return(0)

        curs.execute("select acl from data where title = ?", ['사용자:' + acl_n[0]])
        acl_d = curs.fetchall()
        if(acl_d):
            if(acl_d[0][0] == 'all'):
                return(0)

            if(acl_d[0][0] == 'user' and not re.search("(\.|:)", ip)):
                return(0)

            if(not ip == acl_n[0] or re.search("(\.|:)", ip)):
                return(1)
        
        if(ip == acl_n[0] and not re.search("(\.|:)", ip) and not re.search("(\.|:)", acl_n[0])):
            return(0)
        else:
            return(1)

    file_c = re.search("^파일:(.*)", name)
    if(file_c and admin_check(5, 'edit (' + name + ')') != 1):
        return(1)

    curs.execute("select acl from data where title = ?", [name])
    acl_d = curs.fetchall()
    if(not acl_d):
        return(0)

    curs.execute("select acl from user where id = ?", [ip])
    user_d = curs.fetchall()

    curs.execute('select data from other where name = "edit"')
    set_d = curs.fetchall()
    if(acl_d[0][0] == 'user'):
        if(not user_d):
            return(1)

    if(acl_d[0][0] == 'admin'):
        if(not user_d):
            return(1)

        if(not admin_check(5, 'edit (' + name + ')') == 1):
            return(1)

    if(set_d):
        if(set_d[0][0] == 'user'):
            if(not user_d):
                return(1)

        if(set_d[0][0] == 'admin'):
            if(not user_d):
                return(1)

            if(not admin_check(5, None) == 1):
                return(1)

    return(0)

def ban_check():
    ip = ip_check()
    band = re.search("^([0-9]{1,3}\.[0-9]{1,3})", ip)
    if(band):
        band_it = band.groups()
    else:
        band_it = ['Not']
        
    curs.execute("select block from ban where block = ? and band = 'O'", [band_it[0]])
    band_d = curs.fetchall()

    curs.execute("select block from ban where block = ?", [ip])
    ban_d = curs.fetchall()
    if(band_d or ban_d):
        return(1)
    
    return(0)
        
def topic_check(name, sub):
    ip = ip_check()
    band = re.search("^([0-9]{1,3}\.[0-9]{1,3})", ip)
    if(band):
        band_it = band.groups()
    else:
        band_it = ['Not']
        
    curs.execute("select block from ban where block = ? and band = 'O'", [band_it[0]])
    band_d = curs.fetchall()

    curs.execute("select block from ban where block = ?", [ip])
    ban_d = curs.fetchall()
    if(band_d or ban_d):
        return(1)

    curs.execute("select title from stop where title = ? and sub = ?", [name, sub])
    topic_s = curs.fetchall()
    if(topic_s):
        return(1)

    return(0)

def rd_plus(title, sub, date):
    curs.execute("select title from rd where title = ? and sub = ?", [title, sub])
    rd = curs.fetchall()
    if(rd):
        curs.execute("update rd set date = ? where title = ? and sub = ?", [date, title, sub])
    else:
        curs.execute("insert into rd (title, sub, date) values (?, ?, ?)", [title, sub, date])
    conn.commit()
    
def rb_plus(block, end, today, blocker, why):
    curs.execute("insert into rb (block, end, today, blocker, why) values (?, ?, ?, ?, ?)", [block, end, today, blocker, why])
    conn.commit()

def history_plus(title, data, date, ip, send, leng):
    curs.execute("select id from history where title = ? order by id+0 desc limit 1", [title])
    rows = curs.fetchall()
    if(rows):
        curs.execute("insert into history (id, title, data, date, ip, send, leng) values (?, ?, ?, ?, ?, ?, ?)", [str(int(rows[0][0]) + 1), title, data, date, ip, send, leng])
    else:
        curs.execute("insert into history (id, title, data, date, ip, send, leng) values ('1', ?, ?, ?, ?, ?, ?)", [title, data, date, ip, send + ' (새 문서)', leng])
    conn.commit()

def leng_check(a, b):
    if(a < b):
        c = b - a
        c = '+' + str(c)
    elif(b < a):
        c = a - b
        c = '-' + str(c)
    else:
        c = '0'
        
    return(c)
