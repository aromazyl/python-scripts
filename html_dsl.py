#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 zhangyule <zyl2336709@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

def HTMLFrameWork(name):
    return lambda body: """
<html>

<head>
<meta http-equiv=Content-Type content=\"text/html; charset=gb2312\">
<style>
.table_head{
    color:white;
    font-size:9.0pt;
    font-weight:300;
    font-style:bold;
    text-decoration:bold;
    font-family:\"Arial Unicode MS\", sans-serif;
    text-align:center;
    vertical-align:middle;
    border:.5pt solid windowtext;
    background:#2060A0;
    white-space:nowrap;
    }
.table_plain{
    color:black;
    font-size:10.0pt;
    font-weight:400;
    font-style:normal;
    text-decoration:none;
    font-family:\"Arial Unicode MS\", sans-serif;
    text-align:center;
    vertical-align:middle;
    border:.5pt solid windowtext;
    white-space:nowrap;
    }
.table_red{
    color:red;
    font-size:10.0pt;
    font-weight:400;
    font-style:normal;
    text-decoration:none;
    font-family:\"Arial Unicode MS\", sans-serif;
    text-align:center;
    vertical-align:middle;
    border:.5pt solid windowtext;
    white-space:nowrap;
    }
.table_green{
    color:green;
    font-size:10.0pt;
    font-weight:400;
    font-style:normal;
    text-decoration:none;
    font-family:\"Arial Unicode MS\", sans-serif;
    text-align:center;
    vertical-align:middle;
    border:.5pt solid windowtext;
    white-space:nowrap;
    }
#table_list p{
    /*line-height:2px;*/
    font-size:14px;
    margin-bottom: 5px;
    margin-top: 0px;
}
</style>
</head>

<body>
<div id=\"table_list\">
    <h4>%s</h4>
</div>
%s
</body>

</html>
""" % (name, body)

# leads客户监控邮件

def HTMLBody():
    return lambda (names, tables): '\n'.join(map(lambda (name, table) : \
"""
<h4>%s</h4>
<div id="">
%s
</div>
""" % (name, table), zip(names, tables)))
# 表 1.targetid 媒体表
# 表 2. 单元媒体表

def ReportTable():
    return lambda (reportheader, reportinfos) : \
"""
<table border=1 cellpadding=0 cellspacing=0 style='border-collapse:collapse;/* table-layout:fixed; */width:100%'>
""" + \
        reportheader + '\n' + \
        '\n'.join(reportinfos) + \
"""
</table>
"""

def ReportHeaderCase():
    return lambda (casename, casewidth) : \
        """<th rowspan=\"1\" class=table_head width=400 style=\'height:15.0pt;width:"""+str(casewidth)+"""%\'>""" + casename +"""</th>"""

def ReportHeader():
    def function(report_cases):
        head = '<tr height=20 style=\'height:15.0pt\'>'
        tail = '</tr>'
        body = '\n'.join(report_cases)
        return '\n'.join([head, body, tail])
    return function

def ReportInfoCase():
    return lambda casename: \
"""<td class=table_plain style='height:15.0pt;border-top:none'>%s</td>""" % casename

def ReportInfo():
    def function(report_info_cases):
        head = '<tr height=20 style=\'height:15.0pt\'>'
        tail = '</tr>'
        body = '\n'.join(report_info_cases)
        return '\n'.join([head, body, tail])
    return function

def makeHTMLTable(field_names, field_widths, field_value_lists):
    return ReportTable()( \
                         (ReportHeader()( \
                                        map(lambda (name, width): \
                                            ReportHeaderCase()((name, width)), zip(field_names, field_widths)) \
                                        ) \
                         , \
                         map(lambda x: ReportInfo()(map(ReportInfoCase(), x)), field_value_lists)) \
                         )

def importDataFromFile(filename):
    res = []
    for lines in open(filename, 'r'):
        res.append(lines.strip().split('::'))

if __name__ == '__main__':
    # field_names = ['a', 'b']
    # field_widths = [12, 13]
    # field_values_lists = [[1,2], [3, 4], [5, 6]]
    # table1 = makeHTMLTable(field_names, field_widths, field_values_lists)
    # table2 = makeHTMLTable(field_names, field_widths, field_values_lists)
    # table3 = makeHTMLTable(field_names, field_widths, field_values_lists)
    # print HTMLFrameWork('test')((HTMLBody()((['table1', 'table2', 'table3'], [table1, table2, table3]))))
    # print ReportHeaderCase()(('aa', 11))
    # print ReportHeader()( \
    #                      map(lambda (name, width): \
    #                          ReportHeaderCase()((name, width)), zip(field_names, field_widths)) \
    #                      )
    # print ReportInfo()(map(ReportInfoCase(), ([1,2])))
    # print makeHTMLTable(field_names, field_widths, field_values_lists)
    pass
