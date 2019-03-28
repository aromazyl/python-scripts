#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 zhangyule <zhangyule01@baidu.com>
#
# Distributed under terms of the MIT license.

"""

"""

import sys
import copy
try:
    import prettytable as pt
except:
    pass

from scripts.tools import html_dsl, send_mail
from email.MIMEText import MIMEText
from email.Header import Header
from email.MIMEMultipart import MIMEMultipart

"""
field_names: Include key's names and value's names.
keys: keys record, must be list, e.t.c. [1, 2, 3]
values: values record, must be type List[Tuple], e.t.c. [(1,2,3), (4,5,6)]
"""
class GroupMeta(object):
    def __init__(self, field_names, keys, values):
        self.names = field_names
        self.keys = list(keys)
        self.values = [values]

    def add(self, values):
        self.values.append(values)
        return self

    def sum(self):
        record_result = list(self.values[0])
        for record in self.values[1:]:
            for k in xrange(len(record_result)):
                record_result[k] += record[k]
        return DataFrame(self.keys + record_result, self.names)

class GroupClass(object):
    def __init__(self):
        self.groups = {}

    def reduce_by_sum(self):
        group_result = map(lambda x:x.sum(), self.groups.values())
        df = group_result[0]

        for dd in group_result[1:]:
            df.append(dd)
        return df



"""

"""
class DataFrame(object):
    def __init__(self, values, columns):
        self.columns = columns
        self.index = dict(zip(columns, xrange(10000)))
        if values == None:
            self.collections = []
        else:
            assert len(values) == len(columns), 'Values len must be equal to columns\' length'
            self.collections = [values]

    def get_key(self, key, column_data):
        return copy.deepcopy(column_data[self.index[key]])

    def show(self, tab='\t'):
        def Print(x):
            print str(x) + tab,
        map(Print, self.columns)
        print
        for collect in self.collections:
            map(Print, collect)
            print
        return self

    def show_with_key(self, tab = '\t', out=sys.stdout):
        for collect in self.collections:
            print >> out, '\t'.join(map(lambda x: "%s:%s" % (x[0], x[1]), zip(self.columns, collect)))
        return self

    def resort(self, keys):
        def key_extract(terms):
            return '\t'.join(map(lambda x:str(self.get_key(x, terms)), keys))
        self.collections = sorted(self.collections, key=lambda x:key_extract(x))
        return self

    def add_record(self, value):
        assert len(value) == len(self.columns), 'Values len must be equal to columns\' length'
        self.collections.append(value)
        return self

    """
    data_frame type DataFrame
    @return DataFrame
    """
    def append(self, data_frame):
        self.collections += data_frame.collections
        return self

    """
    keys name and values names
    @return GroupClass
    """
    def groupby(self, keys, values):
        keys = copy.deepcopy(keys)
        values = copy.deepcopy(values)
        group_class = GroupClass()
        for terms in self.collections:
            group_key = tuple(map(lambda x: self.get_key(x, terms), keys))
            group_value = map(lambda x: self.get_key(x, terms), values)
            if group_key not in group_class.groups:
                group_class.groups[group_key] = GroupMeta(keys + values, group_key, group_value)
            else:
                group_class.groups[group_key].add(group_value)
        return group_class

    """
    Select Columns In DataFrame
    @return DataFrame
    """
    def select(self, fields):
        df = DataFrame(None, fields)
        for term in self.collections:
            df.add_record(map(lambda x: self.get_key(x, term), fields))
        return df

    """
    @return DataFrame
    """
    def filter(self, lambda_function):
        df = DataFrame(None, self.columns)
        for collect in self.collections:
            tm = dict(zip(self.columns, collect))
            if lambda_function(tm):
                df.add_record(collect)
        return df

    def create_new_field(self, names, functions):
        df = DataFrame(None, self.columns + names)
        for collect in self.collections:
            tm = dict(zip(self.columns, collect))
            new_fields = map(lambda f: f(tm), functions)
            df.add_record(collect + new_fields)
        return df

    def rename(self, namesA, namesB):
        for name_a, name_b in zip(namesA, namesB):
            self.columns[self.index[name_a]] = name_b
        self.index = dict(zip(self.columns, xrange(100000)))
        return self

    """
    Warning: 1) Call this function after resort by key. 2) Only work on data with expid
    """
    def compare_exp_show(self, tab='\t'):
        if 'expid' not in self.columns:
            print >> sys.stderr, "You should not call this function with expid field!"
            exit(1)
        def Print(x):
            print str(x) + tab,
        map(Print, self.columns)
        print
        for data in self.collections:
            map(Print, data)
            print
            if self.get_key('expid', data).endswith('dz'):
                print 'DIFF'
        return self

    def pretty_show(self):
        table = pt.PrettyTable(self.columns)
        for collection in self.collections:
            table.add_row(collection)
        print table

    def create_html_table(self):
        field_widths = [7 for i in xrange(len(self.columns))]
        return html_dsl.makeHTMLTable(self.columns, field_widths, self.collections)
