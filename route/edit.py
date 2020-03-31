from .tool.func import *

def edit_2(conn, name):
    curs = conn.cursor()

    ip = ip_check()
    section = flask.request.args.get('section', None)

    curs.execute(db_change("select data from data where title = ?"), [name])
    old = curs.fetchall()

    if acl_check(name) == 1:
        return redirect('/edit_req/' + url_pas(name))
    
    if flask.request.method == 'POST':
        if captcha_post(flask.request.form.get('g-recaptcha-response', flask.request.form.get('g-recaptcha', ''))) == 1:
            return re_error('/error/13')
        else:
            captcha_post('', 0)

        if slow_edit_check() == 1:
            return re_error('/error/24')

        today = get_time()
        content = flask.request.form.get('content', '')

        if flask.request.form.get('otent', '') == content:
            return redirect('/w/' + url_pas(name))
        
        if edit_filter_do(content) == 1:
            return re_error('/error/21')
            
        curs.execute(db_change('select data from other where name = "copyright_checkbox_text"'))
        copyright_checkbox_text_d = curs.fetchall()
        if copyright_checkbox_text_d and copyright_checkbox_text_d[0][0] != '' and flask.request.form.get('copyright_agreement', '') != 'yes':
            return re_error('/error/29')

        content = savemark(content)
        
        if old:
            leng = leng_check(len(flask.request.form.get('otent', '')), len(content))
            
            if section:
                content = old[0][0].replace('\r\n', '\n').replace(
                    flask.request.form.get('otent', '').replace('\r\n', '\n'), 
                    content.replace('\r\n', '\n')
                )
        else:
            leng = '+' + str(len(content))

        if old:
            curs.execute(db_change("update data set data = ? where title = ?"), [content, name])
        else:
            curs.execute(db_change("insert into data (title, data) values (?, ?)"), [name, content])

            curs.execute(db_change('select data from other where name = "count_all_title"'))
            curs.execute(db_change("update other set data = ? where name = 'count_all_title'"), [str(int(curs.fetchall()[0][0]) + 1)])

        curs.execute(db_change("select user from scan where title = ?"), [name])
        for scan_user in curs.fetchall():
            curs.execute(db_change("insert into alarm (name, data, date) values (?, ?, ?)"), [
                scan_user[0],
                ip + ' | <a href="/w/' + url_pas(name) + '">' + name + '</a> | Edit', 
                today
            ])
                
        history_plus(
            name,
            content,
            today,
            ip,
            flask.request.form.get('send', ''),
            leng
        )
        
        curs.execute(db_change("delete from back where link = ?"), [name])
        curs.execute(db_change("delete from back where title = ? and type = 'no'"), [name])
        
        render_set(
            title = name,
            data = content,
            num = 1
        )
        
        conn.commit()
        
        return redirect('/w/' + url_pas(name))
    else:            
        if old:
            if section:
                data = re.sub(
                    '\n(?P<in>={1,6})', 
                    '<br>\g<in>', 
                    html.escape('\n' + old[0][0].replace('\r\n', '\n') + '\n')
                )
                i = 0

                while 1:
                    g_data = re.search('((?:<br>)(?:(?:(?!\n|<br>).)+)(?:\n*(?:(?:(?!<br>).)+\n*)+)?)', data)
                    if g_data:
                        if int(section) - 1 == i:
                            data = html.unescape(re.sub('<br>(?P<in>={1,6})', '\n\g<in>', g_data.groups()[0]))
                            
                            break
                        else:
                            data = re.sub('((?:<br>)(?:(?:(?!\n|<br>).)+)(?:\n*(?:(?:(?!<br>).)+\n*)+)?)', '\n', data, 1)

                        i += 1
                    else:
                        break
            else:
                data = old[0][0].replace('\r\n', '\n')
        else:
            data = ''
            
        data_old = data
        get_name = ''

        if not section:
            get_name = '''
                <a href="/manager/15?plus=''' + url_pas(name) + '">(' + load_lang('load') + ')</a> <a href="/edit_filter">(' + load_lang('edit_filter_rule') + ''')</a>
                <hr class=\"main_hr\">
            '''
            
        if flask.request.args.get('plus', None):
            curs.execute(db_change("select data from data where title = ?"), [flask.request.args.get('plus', 'test')])
            get_data = curs.fetchall()
            if get_data:
                data = get_data[0][0]

        save_button = load_lang('save')
        menu_plus = [
            ['delete/' + url_pas(name), load_lang('delete')], 
            ['move/' + url_pas(name), load_lang('move')], 
            ['upload', load_lang('upload')]
        ]
        sub = load_lang('edit')

        curs.execute(db_change('select data from other where name = "edit_bottom_text"'))
        sql_d = curs.fetchall()
        if sql_d and sql_d[0][0] != '':
            b_text = '<hr class=\"main_hr\">' + sql_d[0][0]
        else:
            b_text = ''
        
        cccb_text = ''
        curs.execute(db_change('select data from other where name = "copyright_checkbox_text"'))
        sql_d = curs.fetchall()
        if sql_d and sql_d[0][0] != '':
            cccb_text = '<hr class=\"wmain_hr\"><input type="checkbox" name="copyright_agreement" value="yes">' + sql_d[0][0] + '<hr class=\"main_hr\">'

        curs.execute(db_change('select data from other where name = "edit_help"'))
        sql_d = curs.fetchall()
        if sql_d and sql_d[0][0] != '':
            p_text = sql_d[0][0]
        else:
            p_text = load_lang('defalut_edit_help')

        return easy_minify(flask.render_template(skin_check(), 
            imp = [name, wiki_set(), custom(), other2([' (' + sub + ')', 0])],
            data =  get_name + '''
                <form method="post">
                    <script>do_stop_exit();</script>
                    ''' + edit_button() + '''
                    <textarea rows="25" id="content" placeholder="''' + p_text + '''" name="content">''' + html.escape(re.sub('\n$', '', data)) + '''</textarea>
                    <textarea id="origin" name="otent">''' + html.escape(re.sub('\n$', '', data_old)) + '''</textarea>
                    <hr class=\"main_hr\">
                    <input placeholder="''' + load_lang('why') + '''" name="send" type="text">
                    <hr class=\"main_hr\">
                    ''' + captcha_get() + ip_warring() + cccb_text + '''
                    <button id="save" type="submit" onclick="go_save_zone = 1;">''' + save_button + '''</button>
                    <button id="preview" type="button" onclick="load_preview(\'''' + url_pas(name) + '\')">' + load_lang('preview') + '''</button>
                </form>
                ''' + b_text + '''
                <hr class=\"main_hr\">
                <div id="see_preview"></div>
            ''',
            menu = [['w/' + url_pas(name), load_lang('return')]] + menu_plus
        ))