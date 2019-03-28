#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 zhangyule <zyl2336709@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

import os

class SystemOp(object):
    def __init__(self, cmd):
        self.cmd = cmd

    def show(self):
        print self.cmd
        return self

    def mand(self, op):
        return AndOp(self, op)

    def mor(self, op):
        return OrOp(self, op)

    def mifthenelse(self, opcond, op):
        return IfThenElseOp(opcond, self, op)

    def mappend(self, op):
        return AppendOp(self, op)

    def sys_apply(self):
        return IO(lambda: os.system(self.cmd))

    def popen_apply(self):
        return IO(lambda: os.popen(self.cmd))

class IO(object):
    def __init__(self, exec_cmd):
        self.exec_cmd = exec_cmd

    def run(self):
        return self.exec_cmd()

class HadoopOp(SystemOp):
    def __init__(self, cmd, hadoop_home):
        self.hadoop_home = hadoop_home
        super(HadoopOp, self).__init__(hadoop_home + "/bin/hadoop " + cmd)

class AndOp(SystemOp):
    def __init__(self, opa, opb):
        super(AndOp, self).__init__(opa.cmd + " && " + opb.cmd)

class OrOp(SystemOp):
    def __init__(self, opa, opb):
        super(OrOpo, self).__init__(opa.cmd + "; " + opb.cmd)

class IfThenElseOp(SystemOp):
    def __init__(self, opcond, opa, opb):
        super(IfThenElseOp, self).__init__("""
        %s
        if [ $? -ne 0 ]; then
          %s
        else
          %s
        fi
        """ % (opcond.cmd, opa.cmd, opb.cmd))

class AppendOp(SystemOp):
    def __init__(self, op, append):
        super(AppendOp, self).__init__(op.cmd + append.cmd)

class FormalHdfsOps(object):
    def __init__(self, hadoop_home):
        self.hadoop_home = hadoop_home

    def mkdir(self, path):
        return HadoopOp("fs -mkdir %s" % path, self.hadoop_home)

    def rmr(self, path):
        return HadoopOp("fs -rmr %s" % path, self.hadoop_home)

    def cat(self, path):
        return HadoopOp("fs -cat %s" % path, self.hadoop_home)

    def test(self, path):
        return HadoopOp("fs -test -e %s" % path, self.hadoop_home)

    def touchz(self, path):
        return HadoopOp("fs -touchz %s" % path, self.hadoop_home)

    def ls(self, path):
        return HadoopOp("fs -ls %s" % path, self.hadoop_home)

    def put(self, fpath, tpath):
        return HadoopOp("fs -put %s %s" % (fpath, tpath), self.hadoop_home)

    def get(self, fpath, tpath):
        return HadoopOp("fs -get %s %s" % (fpath, tpath), self.hadoop_home)

if __name__ == '__main__':
    hadoop_home = os.environment('HADOOP_HOME')
    ops_gen = FormalHdfsOps(hadoop_home)
    ops_gen.put("./hadoop_dsl.py", '{your hadoop path}').show().sys_apply().run()
