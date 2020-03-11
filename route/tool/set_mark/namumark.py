from . import tool

import datetime
import html
import re

def link_fix(main_link):
    if re.search('^:', main_link):
        main_link = re.sub('^:', '', main_link)

    main_link = re.sub('^사용자:', 'user:', main_link)
    main_link = re.sub('^파일:', 'file:', main_link)
    main_link = re.sub('^분류:', 'category:', main_link)

    other_link = re.search('[^\\\\]?(#[^#]+)$', main_link)
    if other_link:
        other_link = other_link.groups()[0]

        main_link = re.sub('(#[^#]+)$', '', main_link)
    else:
        other_link = ''

    main_link = re.sub('\\\\#', '%23', main_link)

    return [main_link, other_link]

def table_parser(data, cel_data, cel_num, start_data, num = 0, cel_color = {}):
    table_class = 'class="'
    div_style = 'style="'
    all_table = 'style="'
    cel_style = 'style="'
    row_style = 'style="'
    row = ''
    cel = 'colspan="' + str(round(len(start_data) / 2)) + '"'

    if not cel_num in cel_color:
        cel_color[cel_num] = ''

    cel_style += cel_color[cel_num]

    if num == 0:
        if re.search('^ ', cel_data) and re.search(' $', cel_data):
            cel_style += 'text-align: center;'
        elif re.search('^ ', cel_data):
            cel_style += 'text-align: right;'
        elif re.search(' $', cel_data):
            cel_style += 'text-align: left;'

    table_state = re.findall('&lt;((?:(?!&gt;).)+)&gt;', data)
    for in_state in table_state:
        if re.search("^table ?width=([^=]+)$", in_state):
            table_data = re.sub('^table ?width=', '', in_state)
            div_style += 'width: ' + ((table_data + 'px') if re.search('^[0-9]+$', table_data) else table_data) + ';'
            all_table += 'width: 100%;'
        elif re.search("^table ?height=([^=]+)$", in_state):
            table_data = re.sub('^table ?height=', '', in_state)
            div_style += 'height: ' + ((table_data + 'px') if re.search('^[0-9]+$', table_data) else table_data) + ';'
        elif re.search("^table ?align=([^=]+)$", in_state):
            table_data = re.sub('^table ?align=', '', in_state)
            if table_data == 'right':
                div_style += 'float: right;'
            elif table_data == 'center':
                all_table += 'margin: auto;'
        elif re.search("^table ?textalign=([^=]+)$", in_state):
            num = 1
            table_data = re.sub('^table ?textalign=', '', in_state)
            if table_data == 'right':
                all_table += 'text-align: right;'
            elif table_data == 'center':
                all_table += 'text-align: center;'
        elif re.search("^row ?textalign=([^=]+)$", in_state):
            table_data = re.sub('^row ?textalign=', '', in_state)
            if table_data == 'right':
                row_style += 'text-align: right;'
            elif table_data == 'center':
                row_style += 'text-align: center;'
            else:
                row_style += 'text-align: left;'
        elif re.search('^-([0-9]+)$', in_state):
            cel = 'colspan="' + re.sub('^-', '', in_state) + '"'
        elif re.search("^(\^|v)?\|([^|]+)$", in_state):
            if re.search('^\^', in_state):
                cel_style += 'vertical-align: top;'
            elif re.search('^v', in_state):
                cel_style += 'vertical-align: bottom;'

            row = 'rowspan="' + re.sub('^(\^|v)?\|', '', in_state) + '"'
        elif re.search("^row ?bgcolor=([^=]+)$", in_state):
            table_data = re.sub('^row ?bgcolor=', '', in_state)
            row_style += 'background: ' + (re.sub(',([^,]*)', '', table_data) if re.search(',', table_data) else table_data) + ';'
        elif re.search("^row ?color=([^=]+)$", in_state):
            table_data = re.sub('^row ?color=', '', in_state)
            row_style += 'color: ' + (re.sub(',([^,]*)', '', table_data) if re.search(',', table_data) else table_data) + ';'
        elif re.search("^table ?bordercolor=([^=]+)$", in_state):
            table_data = re.sub('^table ?bordercolor=', '', in_state)
            all_table += 'border: ' + (re.sub(',([^,]*)', '', table_data) if re.search(',', table_data) else table_data) + ' 2px solid;'
        elif re.search("^table ?bgcolor=([^=]+)$", in_state):
            table_data = re.sub('^table ?bgcolor=', '', in_state)
            all_table += 'background: ' + (re.sub(',([^,]*)', '', table_data) if re.search(',', table_data) else table_data) + ';'
        elif re.search("^table ?color=([^=]+)$", in_state):
            table_data = re.sub('^table ?color=', '', in_state)
            all_table += 'color: ' + (re.sub(',([^,]*)', '', table_data) if re.search(',', table_data) else table_data) + ';'
        elif re.search("^col ?bgcolor=([^=]+)$", in_state):
            table_data = re.sub('^col ?bgcolor=', '', in_state)
            table_data = (re.sub(',([^,]*)', '', table_data) if re.search(',', table_data) else table_data)
            cel_color[cel_num] += 'background: ' + table_data + ';'
            cel_style += 'background: ' + table_data + ';'
        elif re.search("^col ?color=([^=]+)$", in_state):
            table_data = re.sub('^col ?color=', '', in_state)
            table_data = (re.sub(',([^,]*)', '', table_data) if re.search(',', table_data) else table_data)
            cel_color[cel_num] += 'color: ' + table_data + ';'
            cel_style += 'color: ' + table_data + ';'
        elif re.search("^(bgcolor=([^=]+)|#(?:[0-9a-f-A-F]{3}){1,2}|\w+)$", in_state):
            table_data = re.sub('^bgcolor=', '', in_state)
            cel_style += 'background: ' + (re.sub(',([^,]*)', '', table_data) if re.search(',', table_data) else table_data) + ';'
        elif re.search("^color=([^=]+)$", in_state):
            table_data = re.sub('^color=', '', in_state)
            cel_style += 'color: ' + (re.sub(',([^,]*)', '', table_data) if re.search(',', table_data) else table_data) + ';'
        elif re.search("^width=([^=]+)$", in_state):
            table_data = re.sub('^width=', '', in_state)
            cel_style += 'width: ' + ((table_data + 'px') if re.search('^[0-9]+$', table_data) else table_data) + ';'
        elif re.search("^height=([^=]+)$", in_state):
            table_data = re.sub('^height=', '', in_state)
            cel_style += 'height: ' + ((table_data + 'px') if re.search('^[0-9]+$', table_data) else table_data) + ';'
        elif re.search('^\(|:|\)$', in_state):
            if in_state == '(':
                cel_style += 'text-align: right;'
            elif in_state == ':':
                cel_style += 'text-align: center;'
            else:
                cel_style += 'text-align: left;'
        elif re.search("^table ?class=([^=]+)$", in_state):
            table_class += re.sub("^table ?class=", '', in_state)

    div_style += '"'
    all_table += '"'
    cel_style += '"'
    row_style += '"'
    table_class += '"'

    return [all_table, row_style, cel_style, row, cel, table_class, num, div_style, cel_color]

def table_start(data):
    cel_num = 0
    table_num = 0
    table_end = ''
    while 1:
        table = re.search('\n((?:(?:(?:(?:\|\||\|[^|]+\|)+(?:(?:(?!\|\|).\n*)*))+)\|\|(?:\n)?)+)', data)
        if table:
            table = '\n' + table.groups()[0]
            table_cel = re.findall('(\n(?:(?:\|\|)+)|\|\|\n(?:(?:\|\|)+)|(?:(?:\|\|)+))((?:(?:(?!\n|\|\|).)+\n*)+)', table)
            for i in table_cel:
                cel_plus = re.search('^((?:&lt;(?:(?:(?!&gt;).)*)&gt;)+)', i[1])
                cel_plus = cel_plus.groups()[0] if cel_plus else ''
                cel_data = re.sub('^((?:&lt;(?:(?:(?!&gt;).)*)&gt;)+)', '', i[1])

                if re.search('^\n', i[0]):
                    cel_num = 1

                    cel_plus = table_parser(
                        cel_plus, 
                        cel_data,
                        cel_num,
                        re.sub('^\n', '', i[0])
                    )
                    cel_color = cel_plus[8]
                    table_num = cel_plus[6]

                    table_end += '' + \
                        '<div class="table_safe" ' + cel_plus[7] + '>' + \
                            '<table ' + cel_plus[5] + ' ' + cel_plus[0] + '>' + \
                                '<tr ' + cel_plus[1] + '>' + \
                                    '<td ' + cel_plus[2] + ' ' + cel_plus[3] + ' ' + cel_plus[4] + '>' + \
                                        cel_data
                                        
                elif re.search('\n', i[0]):
                    cel_num = 1

                    cel_plus = table_parser(
                        cel_plus, 
                        cel_data,
                        cel_num,
                        re.sub('^\|\|\n', '', i[0]),
                        table_num,
                        cel_color
                    )
                    cel_color = cel_plus[8]

                    table_end += '' + \
                            '</td>' + \
                        '</tr>' + \
                        '<tr ' + cel_plus[1] + '>' + \
                            '<td ' + cel_plus[2] + ' ' + cel_plus[3] + ' ' + cel_plus[4] + '>' + \
                                cel_data
                else:
                    cel_num += 1

                    cel_plus = table_parser(
                        cel_plus, 
                        cel_data,
                        cel_num,
                        re.sub('^\|\|\n', '', i[0]),
                        table_num,
                        cel_color
                    )
                    cel_color = cel_plus[8]

                    table_end += '' + \
                        '</td>' + \
                        '<td ' + cel_plus[2] + ' ' + cel_plus[3] + ' ' + cel_plus[4] + '>' + \
                            cel_data

            table_end += '</td></tr></table>'

            data = re.sub('\n((?:(?:(?:(?:\|\||\|[^|]+\|)+(?:(?:(?!\|\|).\n*)*))+)\|\|(?:\n)?)+)', table_end, data, 1)
        else:
            break

    return data

def middle_parser(data, include_num):
    global end_data
    global plus_data

    middle_stack = 0
    middle_list = []
    middle_num = 0

    html_num = 0
    syntax_num = 0
    folding_num = 0

    middle_re = re.compile('(?:{{{((?:(?:(?! |{{{|}}}|&lt;).)*) ?)|(}}}))')
    middle_all_data = middle_re.findall(data)
    for middle_data in middle_all_data:
        if not middle_data[1]:
            if middle_stack > 0:
                middle_stack += 1

                data = re.sub('(?:{{{((?:(?! |{{{|}}}|&lt;).)*)(?P<in> ?)|(}}}))', '&#123;&#123;&#123;' + middle_data[0] + '\g<in>', data, 1)
            else:
                if re.search('^(#|@|\+|\-)', middle_data[0]) and not re.search('^(#|@|\+|\-){2}|(#|@|\+|\-)\\\\', middle_data[0]):
                    if re.search('^(#(?:[0-9a-f-A-F]{3}){1,2})', middle_data[0]):
                        middle_search = re.search('^(#(?:[0-9a-f-A-F]{3}){1,2})', middle_data[0])
                        middle_list += ['span']

                        data = middle_re.sub('<span style="color: ' + middle_search.groups()[0] + ';">', data, 1)
                    elif re.search('^(?:#(\w+))', middle_data[0]):
                        middle_search = re.search('^(?:#(\w+))', middle_data[0])
                        middle_list += ['span']

                        data = middle_re.sub('<span style="color: ' + middle_search.groups()[0] + ';">', data, 1)
                    elif re.search('^(?:@((?:[0-9a-f-A-F]{3}){1,2}))', middle_data[0]):
                        middle_search = re.search('^(?:@((?:[0-9a-f-A-F]{3}){1,2}))', middle_data[0])
                        middle_list += ['span']

                        data = middle_re.sub('<span style="background: #' + middle_search.groups()[0] + ';">', data, 1)
                    elif re.search('^(?:@(\w+))', middle_data[0]):
                        middle_search = re.search('^(?:@(\w+))', middle_data[0])
                        middle_list += ['span']

                        data = middle_re.sub('<span style="background: ' + middle_search.groups()[0] + ';">', data, 1)
                    elif re.search('^(\+|-)([1-5])', middle_data[0]):
                        middle_search = re.search('^(\+|-)([1-5])', middle_data[0])
                        middle_search = middle_search.groups()
                        if middle_search[0] == '+':
                            font_size = str(int(middle_search[1]) * 20 + 100)
                        else:
                            font_size = str(100 - int(middle_search[1]) * 10)

                        middle_list += ['span']

                        data = middle_re.sub('<span style="font-size: ' + font_size + '%;">', data, 1)
                    elif re.search('^#!wiki', middle_data[0]):
                        middle_data_2 = re.search('{{{#!wiki(?: style=(?:&quot;|&#x27;)((?:(?!&quot;|&#x27;).)*)(?:&quot;|&#x27;))?(?: *)\n?', data)
                        if middle_data_2:
                            middle_data_2 = middle_data_2.groups()
                        else:
                            middle_data_2 = ['']

                        middle_list += ['div_1']

                        data = re.sub(
                            '{{{#!wiki(?: style=(?:&quot;|&#x27;)((?:(?!&quot;|&#x27;).)*)(?:&quot;|&#x27;))?(?: *)\n?',
                            '<div id="wiki_div" style="' + str(middle_data_2[0] if middle_data_2[0] else '') + '">',
                            data,
                            1
                        )
                    elif re.search('^#!syntax', middle_data[0]):
                        middle_data_2 = re.search('{{{#!syntax ((?:(?!\n).)+)\n?', data)
                        if middle_data_2:
                            middle_data_2 = middle_data_2.groups()
                        else:
                            middle_data_2 = ['python']

                        if syntax_num == 0:
                            plus_data += 'hljs.initHighlightingOnLoad();\n'

                            syntax_num = 1

                        middle_list += ['pre']

                        data = re.sub(
                            '{{{#!syntax ?((?:(?!\n).)*)\n?',
                            '<pre id="syntax"><code class="' + middle_data_2[0] + '">',
                            data,
                            1
                        )
                    elif re.search('^#!folding', middle_data[0]):
                        middle_list += ['2div']

                        folding_data = re.search('{{{#!folding ?((?:(?!\n).)*)\n?', data)
                        if folding_data:
                            folding_data = folding_data.groups()
                        else:
                            folding_data = ['Test']

                        data = re.sub(
                            '{{{#!folding ?((?:(?!\n).)*)\n?', '' + \
                            '<div>' + \
                                str(folding_data[0]) + ' ' + \
                                '<div style="display: inline-block;">' + \
                                    '<a href="javascript:void(0);" onclick="do_open_folding(\'' + include_num + 'folding_' + str(folding_num) + '\', this);">' + \
                                        '[+]' + \
                                    '</a>' + \
                                '</div_2>' + \
                                '<div id="' + include_num + 'folding_' + str(folding_num) + '" style="display: none;">' + \
                                    '<div id="wiki_div" style="">',
                            data,
                            1
                        )

                        folding_num += 1
                    elif re.search('^#!html', middle_data[0]):
                        middle_list += ['span']

                        html_num += 1

                        data = middle_re.sub('<span id="' + include_num + 'render_contect_' + str(html_num) + '">', data, 1)
                    else:
                        middle_list += ['span']

                        data = middle_re.sub('<span>', data, 1)
                else:
                    middle_list += ['code']

                    middle_stack += 1

                    data = middle_re.sub('<code>' + middle_data[0].replace('\\', '\\\\'), data, 1)

                middle_num += 1
        else:
            if middle_list == []:
                data = middle_re.sub('&#125;&#125;&#125;', data, 1)
            else:
                if middle_stack > 0:
                    middle_stack -= 1

                if middle_stack > 0:
                    data = middle_re.sub('&#125;&#125;&#125;', data, 1)
                else:
                    if middle_num > 0:
                        middle_num -= 1

                    if middle_list[middle_num] == '2div':
                        data = middle_re.sub('</div_1></div_2></div_2>', data, 1)
                    elif middle_list[middle_num] == 'pre':
                        data = middle_re.sub('</code></pre>', data, 1)
                    else:
                        data = middle_re.sub('</' + middle_list[middle_num] + '>', data, 1)

                    del(middle_list[middle_num])

    while 1:
        if middle_stack == 0:
            break
        else:
            if middle_list == []:
                data += '&#125;&#125;&#125;'
            else:
                if middle_stack > 0:
                    middle_stack -= 1

                if middle_stack > 0:
                    data += '&#125;&#125;&#125;'
                else:
                    if middle_num > 0:
                        middle_num -= 1

                    if middle_list[middle_num] == '2div':
                        data += '</div_1></div_2></div_2>'
                    elif middle_list[middle_num] == 'pre':
                        data += '</code></pre>'
                    else:
                        data += '</' + middle_list[middle_num] + '>'

                    del(middle_list[middle_num])

    num = 0
    while 1:
        nowiki_data = re.search('<code>((?:(?:(?!<\/code>).)*\n*)*)<\/code>', data)
        if nowiki_data:
            nowiki_data = nowiki_data.groups()

            num += 1
            end_data['nowiki_' + str(num)] = [nowiki_data[0], 'code']

            data = re.sub(
                '<code>((?:(?:(?!<\/code>).)*\n*)*)<\/code>',
                '<span id="nowiki_' + str(num) + '"></span>',
                data,
                1
            )
        else:
            break

    num = 0
    while 1:
        syntax_data = re.search('<code class="((?:(?!"|>|<).)+)">((?:\n*(?:(?:(?!<\/code>|<span id="syntax_).)+)\n*)+)<\/code>', data)
        if syntax_data:
            syntax_data = syntax_data.groups()

            num += 1

            end_data['syntax_' + str(num)] = [syntax_data[1], 'normal']

            data = re.sub(
                '<code class="((?:(?!"|>|<).)+)">((?:\n*(?:(?:(?!<\/code>|<span id="syntax_).)+)\n*)+)<\/code>',
                '<code class="' + syntax_data[0] + '"><span id="syntax_' + str(num) + '"></span></code>',
                data,
                1
            )
        else:
            break

    return data

def namumark(conn, data, title, main_num, include_num):
    curs = conn.cursor()

    global plus_data
    global end_data

    data = '\n' + data + '\n'
    include_num = include_num + '_' if include_num else ''
    plus_data = 'get_link_state("' + include_num + '");\nget_file_state("' + include_num + '");\n'

    backlink = []
    end_data = {}

    data = re.sub('<math>(?P<in>(?:(?!<\/math>).)+)<\/math>', '[math(\g<in>)]', data)

    data = html.escape(data)
    data = re.sub('\r\n', '\n', data)

    first = 0
    math_re = re.compile('\[math\(((?:(?!\)\]).)+)\)\]', re.I)
    while 1:
        math = math_re.search(data)
        if math:
            math = math.groups()[0]

            first += 1

            data = math_re.sub('<span id="math_' + str(first) + '"></span>', data, 1)

            plus_data += '''
                try {
                    katex.render(
                        "''' + html.unescape(math).replace('\\', '\\\\').replace('"', '\\"') + '''",
                        document.getElementById("math_''' + str(first) + '''")
                    );
                } catch {
                    document.getElementById("math_''' + str(first) + '''").innerHTML = '<span style="color: red;">''' + math.replace('\\', '\\\\') + '''</span>';
                }\n
            '''
        else:
            break

    data = re.sub('\\\\{', '<break_middle>', data)
    data = middle_parser(data, include_num)
    data = re.sub('<break_middle>', '\\{', data)

    num = 0
    while 1:
        one_nowiki = re.search('(?:\\\\)(.)', data)
        if one_nowiki:
            one_nowiki = one_nowiki.groups()

            num += 1

            end_data['one_nowiki_' + str(num)] = [one_nowiki[0], 'normal']

            data = re.sub('(?:\\\\)(.)', '<span id="one_nowiki_' + str(num) + '"></span>', data, 1)
        else:
            break

    include_re = re.compile('\[include\(((?:(?!\)\]).)+)\)\]', re.I)
    i = 0
    while 1:
        i += 1

        include = include_re.search(data)
        if include:
            include = include.groups()[0]

            include_data = re.search('^((?:(?!,).)+)', include)
            if include_data:
                include_data = include_data.groups()[0]
            else:
                include_data = 'Test'

            include_link = include_data
            backlink += [[title, include_link, 'include']]

            data = include_re.sub('' + \
                '<a id="include_link" class="include_' + str(i) + '" href="/w/' + tool.url_pas(include_link) + '">[' + include_link + ']</a>' + \
                '<div id="include_' + str(i) + '"></div>' + \
            '', data, 1)

            include_plus_data = []
            while 1:
                include_plus = re.search(', ?((?:(?!=).)+)=((?:(?!,).)+)', include)
                if include_plus:
                    include_plus = include_plus.groups()

                    include_data_set = include_plus[1]
                    find_data = re.findall('<span id="(one_nowiki_[0-9]+)">', include_data_set)
                    for j in find_data:
                        include_data_set = include_data_set.replace('<span id="' + j + '"></span>', end_data[j][0])

                    include_plus_data += [[include_plus[0], include_data_set]]

                    include = re.sub(', ?((?:(?!=).)+)=((?:(?!,).)+)', '', include, 1)
                else:
                    break

            plus_data += 'load_include("' + include_link + '", "include_' + str(i) + '", ' + str(include_plus_data) + ');\n'
        else:
            break

    data = re.sub('\r\n', '\n', data)
    data = re.sub('&amp;', '&', data)

    data = re.sub('\n( +)\|\|', '\n||', data)
    data = re.sub('\|\|( +)\n', '||\n', data)

    data = re.sub('\n##(((?!\n).)+)', '', data)
    data = re.sub('<div id="wiki_div" style="">\n', '<div id="wiki_div" style="">', data)

    while 1:
        wiki_table_data = re.search('<div id="wiki_div" ((?:(?!>).)+)>((?:(?!<div id="wiki_div"|<\/div_1>).\n*)+)<\/div_1>', data)
        if wiki_table_data:
            wiki_table_data = wiki_table_data.groups()
            if re.search('\|\|', wiki_table_data[1]):
                end_parser = re.sub('\n$', '', re.sub('^\n', '', table_start('\n' + wiki_table_data[1] + '\n')))
            else:
                end_parser = wiki_table_data[1]

            data = re.sub('<div id="wiki_div" ((?:(?!>).)+)>((?:(?!<div id="wiki_div"|<\/div_1>).\n*)+)<\/div_1>', '<div ' + wiki_table_data[0] + '>' + end_parser + '</div_2>', data, 1)
        else:
            break

    data = re.sub('<\/div_2>', '</div>', data)
    data = re.sub('<\/td>', '</td_1>', data)

    data += '\n'
    data = data.replace('\\', '&#92;')

    redirect_re = re.compile('\n#(?:redirect|넘겨주기) ((?:(?!\n).)+)\n', re.I)
    redirect = redirect_re.search(data)
    if redirect:
        redirect = redirect.groups()[0]

        return_link = link_fix(redirect)
        main_link = return_link[0]
        other_link = return_link[1]

        backlink += [[title, main_link + other_link, 'redirect']]

        data = redirect_re.sub(
            '\n' + \
                '<ul>' + \
                    '<li>' + \
                        '<a href="' + tool.url_pas(main_link) + other_link + '">' + main_link + other_link + '</a>' + \
                    '</li>' + \
                '</ul>' + \
            '\n',
            data,
            1
        )

    no_toc_re = re.compile('\[(?:목차|toc)\((?:no)\)\]\n', re.I)
    toc_re = re.compile('\[(?:목차|toc)\]', re.I)
    if not no_toc_re.search(data):
        if not toc_re.search(data):
            data = re.sub('\n(?P<in>={1,6}) ?(?P<out>(?:(?!=).)+) ?={1,6}\n', '\n[toc]\n\g<in> \g<out> \g<in>\n', data, 1)
    else:
        data = no_toc_re.sub('', data)

    data = '<div class="all_in_data" id="in_data_0">' + data

    toc_full = 0
    toc_top_stack = 6
    toc_stack = [0, 0, 0, 0, 0, 0]
    edit_number = 0
    toc_data = '<div id="toc"><span id="toc_title">TOC</span>\n\n'
    while 1:
        toc = re.search('\n(={1,6}) ?((?:(?!\n).)+) ?(?:={1,6})\n', data)
        if toc:
            toc = toc.groups()

            toc_number = len(toc[0])
            edit_number += 1

            if toc_full > toc_number:
                for i in range(toc_number, 6):
                    toc_stack[i] = 0

            if toc_top_stack > toc_number:
                toc_top_stack = toc_number

            toc_full = toc_number
            toc_stack[toc_number - 1] += 1
            toc_number = str(toc_number)
            all_stack = ''

            for i in range(0, 6):
                all_stack += str(toc_stack[i]) + '.'

            while 1:
                if re.search('[^0-9]0\.', all_stack):
                    all_stack = re.sub('[^0-9]0\.', '.', all_stack)
                else:
                    break

            all_stack = re.sub('^0\.', '', all_stack)
            all_stack = re.sub('\.$', '', all_stack)

            new_toc_data = re.sub('=*$', '', toc[1])
            new_toc_data = re.sub(' +$', '', new_toc_data)
            if re.search('^# ?(?P<in>[^#]+) ?#$', new_toc_data):
                fol_head = '+'

                new_toc_data = re.sub('^# ?(?P<in>[^#]+) ?#$', '\g<in>', new_toc_data)
            else:
                fol_head = '-'

            data = re.sub(
                '\n(={1,6}) ?((?:(?!\n).)+) ?\n',
                '\n' + \
                '</div>'
                '<h' + toc_number + ' id="s-' + all_stack + '">' + \
                    '<a href="#toc">' + all_stack + '.</a> ' + new_toc_data + ' ' + \
                    '<span style="font-size: 12px">' + \
                        '<a href="/edit/' + tool.url_pas(title) + '?section=' + str(edit_number) + '">(Edit)</a>' + \
                        ' ' + \
                        '<a href="javascript:void(0);" onclick="do_open_folding(\'in_data_' + all_stack + '\', this);">' + \
                            '[' + fol_head + ']' + \
                        '</a>' + \
                    '</span>' + \
                '</h' + toc_number + '>' + \
                '<div class="all_in_data"' + (' style="display: none;"' if fol_head == '+' else '') + ' id="in_data_' + all_stack + '">' + \
                    '\n',
                data,
                1
            )

            toc_main_data = new_toc_data
            toc_main_data = re.sub('\[\*((?:(?! |\]).)*)(?: ((?:(?!(\[\*(?:(?:(?!\]).)+)\]|\])).)+))?\]', '', toc_main_data)
            toc_main_data = re.sub('<span id="math_[0-9]"><\/span>', '(Math)', toc_main_data)

            toc_data += '' + \
                '<span style="margin-left: ' + str((toc_full - toc_top_stack) * 10) + 'px;">' + \
                    '<a href="#s-' + all_stack + '">' + all_stack + '.</a> ' + toc_main_data + \
                '</span>' + \
                '\n' + \
            ''
        else:
            break

    toc_data += '</div>'
    data = toc_re.sub(toc_data, data)

    data = tool.savemark(data)

    data = re.sub("\[anchor\((?P<in>(?:(?!\)\]).)+)\)\]", '<span id="\g<in>"></span>', data, flags = re.I)

    ruby_all = re.findall("\[ruby\(((?:(?:(?!\)\]).)+))\)\]", data, flags = re.I)
    for i in ruby_all:
        ruby_code = re.search('^([^,]+)', i)
        if ruby_code:
            ruby_code = ruby_code.groups()[0]
        else:
            ruby_code = 'Test'

        ruby_top = re.search('ruby=([^,]+)', i, flags = re.I)
        if ruby_top:
            ruby_top = ruby_top.groups()[0]
        else:
            ruby_top = 'Test'

        ruby_color = re.search('color=([^,]+)', i, flags = re.I)
        if ruby_color:
            ruby_color = 'color: ' + ruby_color.groups()[0] + ';'
        else:
            ruby_color = ''

        ruby_data = '' + \
            '<ruby>' + \
                ruby_code \
                + '<rp>(</rp>' + \
                '<rt style="' + ruby_color + '">' + ruby_top + '</rt>' + \
                '<rp>)</rp>' + \
            '</ruby>' + \
        ''

        data = re.sub("\[ruby\(((?:(?:(?!\)\]).)+))\)\]", ruby_data, data, 1, flags = re.I)

    curs.execute(tool.db_change('select data from other where name = "count_all_title"'))
    all_title = curs.fetchall()
    data = re.sub('\[pagecount\]', all_title[0][0], data, flags = re.I)

    now_time = tool.get_time()
    data = re.sub('\[date\]', now_time, data, flags = re.I)

    time_data = re.search('^([0-9]{4}-[0-9]{2}-[0-9]{2})', now_time)
    time = time_data.groups()

    age_re = re.compile('\[age\(([0-9]{4}-[0-9]{2}-[0-9]{2})\)\]', re.I)
    while 1:
        age_data = age_re.search(data)
        if age_data:
            age = age_data.groups()[0]

            try:
                old = datetime.datetime.strptime(time[0], '%Y-%m-%d')
                will = datetime.datetime.strptime(age, '%Y-%m-%d')

                e_data = old - will

                data = age_re.sub(str(int(e_data.days / 365)), data, 1)
            except:
                data = age_re.sub('age-error', data, 1)
        else:
            break

    dday_re = re.compile('\[dday\(([0-9]{4}-[0-9]{2}-[0-9]{2})\)\]', re.I)
    while 1:
        dday_data = dday_re.search(data)
        if dday_data:
            dday = dday_data.groups()[0]

            try:
                old = datetime.datetime.strptime(time[0], '%Y-%m-%d')
                will = datetime.datetime.strptime(dday, '%Y-%m-%d')

                e_data = old - will

                if re.search('^-', str(e_data.days)):
                    e_day = str(e_data.days)
                else:
                    e_day = '+' + str(e_data.days)

                data = dday_re.sub(e_day, data, 1)
            except:
                data = dday_re.sub('dday-error', data, 1)
        else:
            break

    video_re = re.compile('\[(youtube|kakaotv|nicovideo)\(((?:(?!\)\]).)+)\)\]', re.I)
    youtube_re = re.compile('youtube', re.I)
    kakaotv_re = re.compile('kakaotv', re.I)
    while 1:
        video = video_re.search(data)
        if video:
            video = video.groups()

            width = re.search(', ?width=((?:(?!,).)+)', video[1])
            if width:
                video_width = width.groups()[0]
                if re.search('^[0-9]+$', video_width):
                    video_width += 'px'
            else:
                video_width = '560px'

            height = re.search(', ?height=((?:(?!,).)+)', video[1])
            if height:
                video_height = height.groups()[0]
                if re.search('^[0-9]+$', video_height):
                    video_height += 'px'
            else:
                video_height = '315px'

            code = re.search('^((?:(?!,).)+)', video[1])
            if code:
                video_code = code.groups()[0]
            else:
                video_code = ''

            video_start = ''

            if youtube_re.search(video[0]):
                start = re.search(', ?(start=(?:(?!,).)+)', video[1])
                if start:
                    video_start = '?' + start.groups()[0]

                video_code = re.sub('^https:\/\/www\.youtube\.com\/watch\?v=', '', video_code)
                video_code = re.sub('^https:\/\/youtu\.be\/', '', video_code)

                video_src = 'https://www.youtube.com/embed/' + video_code
            elif kakaotv_re.search(video[0]):
                video_code = re.sub('^https:\/\/tv\.kakao\.com\/channel\/9262\/cliplink\/', '', video_code)
                video_code = re.sub('^http:\/\/tv\.kakao\.com\/v\/', '', video_code)

                video_src = 'https://tv.kakao.com/embed/player/cliplink/' + video_code +'?service=kakao_tv'
            else:
                video_src = 'https://embed.nicovideo.jp/watch/' + video_code

            data = video_re.sub(
                '<iframe style="width: ' + video_width + '; height: ' + video_height + ';" src="' + video_src + video_start + '" allowfullscreen></iframe>', 
                data, 
                1
            )
        else:
            break

    while 1:
        block = re.search('(\n(?:&gt; ?(?:(?:(?!\n).)+)?\n)+)', data)
        if block:
            block = block.groups()[0]

            block = re.sub('^\n&gt; ?', '', block)
            block = re.sub('\n&gt; ?', '\n', block)
            block = re.sub('\n$', '', block)

            data = re.sub('(\n(?:&gt; ?(?:(?:(?!\n).)+)?\n)+)', '\n<blockquote>' + block + '</blockquote>\n', data, 1)
        else:
            break

    while 1:
        hr = re.search('\n-{4,9}\n', data)
        if hr:
            data = re.sub('\n-{4,9}\n', '\n<hr>\n', data, 1)
        else:
            break

    data = re.sub('(?P<in>\n +\* ?(?:(?:(?!\|\|).)+))\|\|', '\g<in>\n ||', data)
    data = re.sub('(?P<in><div id="folding_(?:[0-9]+)" style="display: none;"><div style="">|<blockquote>)(?P<out> )?\* ', '\g<in>\n\g<out>* ', data)

    while 1:
        li = re.search('(\n(?:(?: *)\* ?(?:(?:(?!\n).)+)\n)+)', data)
        if li:
            li = li.groups()[0]
            while 1:
                sub_li = re.search('\n(?:( *)\* ?((?:(?!\n).)+))', li)
                if sub_li:
                    sub_li = sub_li.groups()

                    if len(sub_li[0]) == 0:
                        margin = 20
                    else:
                        margin = len(sub_li[0]) * 20

                    li = re.sub('\n(?:( *)\* ?((?:(?!\n).)+))', '<li style="margin-left: ' + str(margin) + 'px;">' + sub_li[1] + '</li>', li, 1)
                else:
                    break

            data = re.sub('(\n(?:(?: *)\* ?(?:(?:(?!\n).)+)\n)+)', '\n\n<ul>' + li + '</ul>\n', data, 1)
        else:
            break

    data = re.sub('<\/ul>\n \|\|', '</ul>||', data)

    while 1:
        indent = re.search('\n( +)', data)
        if indent:
            indent = len(indent.groups()[0])

            margin = '<span style="margin-left: 20px;"></span>' * indent

            data = re.sub('\n( +)', '\n' + margin, data, 1)
        else:
            break

    data = table_start(data)

    category = ''
    category_re = re.compile('^(?:category|분류):', re.I)
    while 1:
        link = re.search('\[\[((?:(?!\[\[|\]\]).)+)\]\]', data)
        if link:
            link = link.groups()[0]

            link_split = re.search('((?:(?!\|).)+)(?:\|((?:(?!\|).)+))', link)
            if link_split:
                link_split = link_split.groups()

                main_link = link_split[0]
                see_link = link_split[1]
            else:
                main_link = link
                see_link = link

            if re.search('^((?:file|파일)|(?:out|외부)):', main_link):
                file_style = ''

                file_width = re.search('width=((?:(?!&).)+)', see_link)
                if file_width:
                    file_width = file_width.groups()[0]
                    if re.search('px$', file_width):
                        file_style += 'width: ' + file_width + ';'
                    else:
                        file_style += 'width: ' + file_width + 'px;'

                file_height = re.search('height=((?:(?!&).)+)', see_link)
                if file_height:
                    file_height = file_height.groups()[0]
                    if re.search('px$', file_height):
                        file_style += 'height: ' + file_height + ';'
                    else:
                        file_style += 'height: ' + file_height + 'px;'

                file_align = re.search('align=((?:(?!&).)+)', see_link)
                if file_align:
                    file_align = file_align.groups()[0]
                    if file_align == 'center':
                        file_align = 'display: block; text-align: center;'
                    else:
                        file_align = 'float: ' + file_align + ';'
                else:
                    file_align = ''

                file_color = re.search('bgcolor=((?:(?!&).)+)', see_link)
                if file_color:
                    file_color = 'background: ' + file_color.groups()[0] + '; display: inline-block;'
                else:
                    file_color = ''

                if re.search('^(?:out|외부):', main_link):
                    file_src = re.sub('^(?:out|외부):', '', main_link)

                    file_alt = main_link
                    exist = 'Yes'
                else:
                    file_data = re.search('^(?:file|파일):((?:(?!\.).)+)\.(.+)$', main_link)
                    if file_data:
                        file_data = file_data.groups()
                        file_name = file_data[0]
                        file_end = file_data[1]

                        if main_link != title:
                            backlink += [[title, main_link, 'file']]
                    else:
                        file_name = 'TEST'
                        file_end = 'jpg'

                    file_src = '/image/' + tool.sha224_replace(file_name) + '.' + file_end
                    file_alt = 'file:' + file_name + '.' + file_end
                    exist = None

                if exist:
                    data = re.sub(
                        '\[\[((?:(?!\[\[|\]\]).)+)\]\]',
                        '<span style="' + file_align + '">' + \
                            '<span style="' + file_color + '">' + \
                                '<img style="' + file_style + '" alt="' + file_alt + '" src="' + file_src + '">' + \
                            '</span>' + \
                        '</span>',
                        data,
                        1
                    )
                else:
                    data = re.sub(
                        '\[\[((?:(?!\[\[|\]\]).)+)\]\]',
                        '<span style="' + file_align + '">' + \
                            '<span style="' + file_color + '">' + \
                                '<img class="' + include_num + 'file_finder_1" style="' + file_style + '" alt="' + file_alt + '" src="' + file_src + '">' + \
                                '<a class="' + include_num + 'file_finder_2" id="not_thing" href="/upload?name=' + tool.url_pas(file_name) + '">' + file_alt + '</a>' + \
                            '</span>' + \
                        '</span>',
                        data,
                        1
                    )
            elif category_re.search(main_link):
                if category == '':
                    category += '<div id="cate_all"><hr><div id="cate">Category : '

                main_link = category_re.sub('category:', main_link)

                curs.execute(tool.db_change("select title from data where title = ?"), [main_link])
                if re.search('#blur', main_link):
                    see_link = 'Hidden'
                    link_id = 'id="inside"'

                    main_link = re.sub('#blur', '', main_link)

                backlink += [[title, main_link, 'cat']]
                category += '<a class="' + include_num + 'link_finder" href="/w/' + tool.url_pas(main_link) + '">' + category_re.sub('', see_link) + '</a> | '

                data = re.sub('\[\[((?:(?!\[\[|\]\]).)+)\]\]', '', data, 1)
            elif re.search('^wiki:', main_link):
                data = re.sub(
                    '\[\[((?:(?!\[\[|\]\]).)+)\]\]',
                    '<a id="inside" href="/' + tool.url_pas(re.sub('^wiki:', '', main_link)) + '">' + see_link + '</a>',
                    data,
                    1
                )
            elif re.search('^inter:((?:(?!:).)+):', main_link):
                inter_data = re.search('^inter:((?:(?!:).)+):((?:(?!\]\]|\|).)+)', main_link)
                inter_data = inter_data.groups()

                curs.execute(tool.db_change('select link, icon from inter where title = ?'), [inter_data[0]])
                inter = curs.fetchall()
                if inter:
                    if inter[0][1] != '':
                        inter_view = inter[0][1]
                    else:
                        inter_view = inter_data[0] + ':'

                    if see_link != main_link:
                        data = re.sub(
                            '\[\[((?:(?!\[\[|\]\]).)+)\]\]',
                            '<a id="inside" href="' + inter[0][0] + inter_data[1] + '">' + inter_view + see_link + '</a>',
                            data,
                            1
                        )
                    else:
                        data = re.sub(
                            '\[\[((?:(?!\[\[|\]\]).)+)\]\]',
                            '<a id="inside" href="' + inter[0][0] + inter_data[1] + '">' + inter_view + inter_data[1] + '</a>',
                            data,
                            1
                        )
                else:
                    data = re.sub('\[\[((?:(?!\[\[|\]\]).)+)\]\]', 'Not exist', data, 1)
            elif re.search('^(\/(?:.+))$', main_link):
                under_title = re.search('^(\/(?:.+))$', main_link)
                under_title = under_title.groups()[0]

                if see_link != main_link:
                    data = re.sub('\[\[((?:(?!\[\[|\]\]).)+)\]\]', '[[' + title + under_title + '|' + see_link + ']]', data, 1)
                else:
                    data = re.sub('\[\[((?:(?!\[\[|\]\]).)+)\]\]', '[[' + title + under_title + ']]', data, 1)
            elif re.search('^http(s)?:\/\/', main_link):
                data = re.sub('\[\[((?:(?!\[\[|\]\]).)+)\]\]', '<a id="out_link" rel="nofollow" href="' + main_link + '">' + see_link + '</a>', data, 1)
            else:
                return_link = link_fix(main_link)
                main_link = html.unescape(return_link[0])
                other_link = return_link[1]

                if re.search('^\/', main_link):
                    main_link = re.sub('^\/', title + '/', main_link)
                elif re.search('\.\.\/\/', main_link):
                    main_link = re.sub('\.\.\/\/', '/', main_link)
                elif re.search('^\.\.\/', main_link):
                    main_link = re.sub('^\.\.\/', re.sub('(?P<in>.+)\/.*$', '\g<in>', title), main_link)

                if not re.search('^\|', main_link):
                    if main_link != title:
                        if main_link != '':
                            backlink += [[title, main_link, '']]

                            curs.execute(tool.db_change("select title from data where title = ?"), [main_link])
                            if not curs.fetchall():
                                backlink += [[title, main_link, 'no']]

                            data = re.sub(
                                '\[\[((?:(?!\[\[|\]\]).)+)\]\]',
                                '<a class="' + include_num + 'link_finder" ' + \
                                    'title="' + main_link + other_link + '" ' + \
                                    'href="/w/' + tool.url_pas(main_link) + other_link + '"' + \
                                '>' + see_link + '</a>',
                                data,
                                1
                            )
                        else:
                            data = re.sub(
                                '\[\[((?:(?!\[\[|\]\]).)+)\]\]',
                                '<a title="' + other_link + '" href="' + other_link + '">' + see_link + '</a>',
                                data,
                                1
                            )
                    else:
                        if re.search('^#', other_link):
                            data = re.sub(
                                '\[\[((?:(?!\[\[|\]\]).)+)\]\]',
                                '<a title="' + other_link + '" href="' + other_link + '">' + other_link + '</a>',
                                data,
                                1
                            )
                        else:
                            data = re.sub('\[\[((?:(?!\[\[|\]\]).)+)\]\]', '<b>' + see_link + '</b>', data, 1)
                else:
                    data = re.sub('\[\[((?:(?!\[\[|\]\]).)+)\]\]', '&#91;&#91;' + link + '&#93;&#93;', data, 1)
        else:
            break

    br_re = re.compile('\[br\]', re.I)
    data = br_re.sub('<br>', data)

    footnote_number = 0

    footnote_all = []
    footnote_dict = {}
    footnote_re = {}

    footdata_all = '<hr><ul id="footnote_data">'

    re_footnote = re.compile('(?:\[\*((?:(?! |\]).)*)(?: ((?:(?!(?:\[\*|\])).)+))?\]|(\[(?:각주|footnote)\]))')
    while 1:
        footnote = re_footnote.search(data)
        if footnote:
            footnote_data = footnote.groups()
            if footnote_data[2]:
                footnote_all.sort()

                for footdata in footnote_all:
                    if footdata[2] == 0:
                        footdata_in = ''
                    else:
                        footdata_in = footdata[2]

                    footdata_all += '' + \
                        '<li>' + \
                            '<a href="#' + include_num + 'rfn-' + str(footdata[0]) + '" ' + \
                                'id="' + include_num + 'cfn-' + str(footdata[0]) + '" ' + \
                                'onclick="do_open_foot(\'' + include_num + 'fn-' + str(footdata[0]) + '\', 1);">' + \
                                '(' + footdata[1] + ')' + \
                            '</a> <span id="' + include_num + 'fn-' + str(footdata[0]) + '">' + footdata_in + '</span>' + \
                        '</li>' + \
                    ''

                data = re_footnote.sub(footdata_all + '</ul>', data, 1)

                footnote_all = []
                footdata_all = '<hr><ul id="footnote_data">'
            else:
                footnote = footnote_data[1]
                footnote_name = footnote_data[0]
                if footnote_name and not footnote:
                    if footnote_name in footnote_dict:
                        footnote_re[footnote_name] += 1

                        foot_plus_num = str(footnote_re[footnote_name])
                        footshort = footnote_dict[footnote_name] + '.' + foot_plus_num

                        footnote_all += [[float(footshort), footshort, 0]]

                        data = re_footnote.sub('' + \
                            '<sup>' + \
                                '<a href="#' + include_num + 'fn-' + footshort + '" ' + \
                                    'id="' + include_num + 'rfn-' + footshort + '" ' + \
                                    'onclick="do_open_foot(\'' + include_num + 'fn-' + footshort + '\');">' + \
                                    '(' + footnote_name + ')' + \
                                '</a>' + \
                            '</sup>' + \
                        '', data, 1)
                    else:
                        data = re_footnote.sub('<sup><a href="javascript:void(0);">(' + footnote_name + ')</a></sup>', data, 1)
                else:
                    footnote_number += 1

                    if not footnote_name:
                        footnote_name = str(footnote_number)

                    footnote_dict.update({ footnote_name : str(footnote_number) })

                    if not footnote_name in footnote_re:
                        footnote_re.update({ footnote_name : 0 })
                    else:
                        footnote_re[footnote_name] += 1

                    footnote_all += [[footnote_number, footnote_name, footnote]]

                    data = re_footnote.sub('' + \
                        '<sup>' + \
                            '<a href="#' + include_num + 'fn-' + str(footnote_number) + '" ' + \
                                'id="' + include_num + 'rfn-' + str(footnote_number) + '" ' + \
                                'onclick="do_open_foot(\'' + include_num + 'fn-' + str(footnote_number) + '\');">' + \
                                '(' + footnote_name + ')' + \
                            '</a>' + \
                        '</sup>' + \
                    '', data, 1)
        else:
            break

    data = re.sub('\n+$', '', data)

    footnote_all.sort()

    for footdata in footnote_all:
        if footdata[2] == 0:
            footdata_in = ''
        else:
            footdata_in = str(footdata[2])

        footdata_all += '' + \
            '<li>' + \
                '<a href="#' + include_num + 'rfn-' + str(footdata[0]) + '" ' + \
                    'id="' + include_num + 'cfn-' + str(footdata[0]) + '" ' + \
                    'onclick="do_open_foot(\'' + include_num + 'fn-' + str(footdata[0]) + '\', 1);">' + \
                    '(' + str(footdata[1]) + ')' + \
                '</a> <span id="' + include_num + 'fn-' + str(footdata[0]) + '">' + footdata_in + '</span>' + \
            '</li>' + \
        ''

    footdata_all += '</ul>'
    footdata_all = '</div>' + footdata_all
    if footdata_all == '</div><hr><ul id="footnote_data"></ul>':
        footdata_all = '</div>'

    data = re.sub('\n$', footdata_all, data + '\n', 1)

    data = re.sub('&#x27;&#x27;&#x27;(?P<in>((?!&#x27;&#x27;&#x27;).)+)&#x27;&#x27;&#x27;', '<b>\g<in></b>', data)
    data = re.sub('&#x27;&#x27;(?P<in>((?!&#x27;&#x27;).)+)&#x27;&#x27;', '<i>\g<in></i>', data)
    data = re.sub('~~(?P<in>(?:(?!~~).)+)~~', '<s>\g<in></s>', data)
    data = re.sub('--(?P<in>(?:(?!--).)+)--', '<s>\g<in></s>', data)
    data = re.sub('__(?P<in>(?:(?!__).)+)__', '<u>\g<in></u>', data)
    data = re.sub('\^\^(?P<in>(?:(?!\^\^).)+)\^\^', '<sup>\g<in></sup>', data)
    data = re.sub(',,(?P<in>(?:(?!,,).)+),,', '<sub>\g<in></sub>', data)

    if category != '':
        category = re.sub(' \| $', '', category) + '</div></div>'

    data += category

    for i in end_data:
        if end_data[i][1] == 'normal':
            data = data.replace('<span id="' + i + '"></span>', end_data[i][0])
            data = data.replace(tool.url_pas('<span id="' + i + '"></span>'), tool.url_pas(end_data[i][0]))
        else:
            if re.search('\n', end_data[i][0]):
                data = data.replace('<span id="' + i + '"></span>', '\n<pre>' + re.sub('^\n', '', end_data[i][0]) + '</pre>')
            else:
                data = data.replace('<span id="' + i + '"></span>', '<code>' + end_data[i][0] + '</code>')

    if main_num == 1:
        i = 0
        while 1:
            try:
                _ = backlink[i][0]
            except:
                break

            find_data = re.findall('<span id="(one_nowiki_[0-9]+)">', backlink[i][1])
            for j in find_data:
                if backlink[i][2] != 'redirect':
                    backlink[i][1] = backlink[i][1].replace('<span id="' + j + '"></span>', end_data[j][0])
                else:
                    backlink[i][1] = backlink[i][1].replace('<span id="' + j + '"></span>', '\\' + end_data[j][0])

            i += 1

    data = re.sub('<\/td_1>', '</td>', data)
    data = re.sub('<\/ul>\n?', '</ul>', data)
    data = re.sub('<\/pre>\n?', '</pre>', data)
    data = re.sub('(?P<in><div class="all_in_data"(?:(?:(?!id=).)+)? id="in_data_([^"]+)">)(\n)+', '\g<in>', data)
    data = re.sub('\n\n<ul>', '\n<ul>', data)
    data = re.sub('<\/ul>\n\n', '</ul>', data)
    data = re.sub('^(\n)+', '', data)
    data = re.sub('(\n)+<hr><ul id="footnote_data">', '<hr><ul id="footnote_data">', data)
    data = re.sub('(?P<in><td(((?!>).)*)>)\n', '\g<in>', data)
    data = re.sub('(\n)?<hr>(\n)?', '<hr>', data)
    data = re.sub('<\/ul>\n\n<ul>', '</ul>\n<ul>', data)
    data = re.sub('<\/ul>\n<ul>', '</ul><ul>', data)
    data = re.sub('\n<\/ul>', '</ul>', data)
    data = re.sub('\n', '<br>', data)

    plus_data = 'render_html("' + include_num + 'render_contect");\n' + plus_data

    return [data, plus_data, backlink]
