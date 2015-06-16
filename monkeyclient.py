# -*- coding:utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : monkeyclient
# 
# Creation      : 2015年4月22日
# Author        : gancj@ucweb.com
###########################################################################

import util
import os
import sys
import time
import shutil
import datetime
from excelutil import insertdata
import mailutil

ru = util.RunUtil()


class MonkeyTestClient():

    def __init__(self, workout, workdir, workoutpath, workresult):
        self.workout = workout
        self.workoutpath = workoutpath
        self.workresult = workresult
        self.workdir = workdir

    def setup(self):
        pass

    def teardown(self):
        #删除测试结果的文件夹
        shutil.rmtree(self.workout)
        shutil.rmtree(self.workresult)
        os.remove(os.path.join(self.workdir, 'result.xlsx'))
        os.remove(os.path.join(self.workdir, 'result.zip'))

    def initalizeEnvironment(self):
        pass

    def isDeviceConnected(self):
        if ru.getDevID():
            self.uuid = ru.getDevID()
            return 1
        else:
            self.uuid = ""
            return 0

    def waitingForStop(self):
        """

        :return:
        1:  成功运行sec*cycle 分钟
        －1：开始就没有正常启动instrumentss
        0:  中途挂了
        缺陷：只能检查出monkey挂掉的情况，并不能检查出回到主界面的情况，或者monkey卡住的情况
        """
        sec = float(ru.anaysisIniFile('./config.ini', 'time_args', 'sleep_sec'))
        cycle = int(ru.anaysisIniFile('./config.ini', 'time_args', 'cycle'))
        print '开始检查，{0}轮，每轮{1}秒，跑完这么多轮后停止'.format(cycle, sec)
        minutesCount = 0
        while self.isInstrumentsRunning():
            time.sleep(sec)
            minutesCount = minutesCount + 1
            if minutesCount > cycle:
                break
        if minutesCount == 0:
            return -1
        elif minutesCount>cycle:
            return 1
        else:
            return 0

    def isInstrumentsRunning(self):
        """
        :return:
            1: 正在运行
            0: 没有在运行
        """
        instrumentsCount = os.popen('ps -ef | grep /instruments | grep -v grep | wc -l').readlines()[0].replace("\n", "")
        if int(instrumentsCount):
            return 1
        else:
            return 0

    def creatDir(self):
        workdir = os.path.dirname(os.path.realpath(sys.argv[0]))
        workout = os.path.join(workdir, 'out')
        if not os.path.exists(workout):
            os.mkdir(workout)
        workoutpath = os.path.join(workout, util.RunUtil().getCurTime())
        if not os.path.exists(workoutpath):
            os.mkdir(workoutpath)
        self.workoutpath = workoutpath
        return self.workoutpath

    def runJsScripts(self):
        """ 运行js脚本测试
            注释规范
            Args:

            Returns:

            Raises:
            IOError: An error occurred accessing the bigtable.Table object.
        """
        template = ru.anaysisIniFile('./config.ini', 'instruments_options', 'template')
        devicename = ru.anaysisIniFile('./config.ini', 'instruments_options', 'devicename')
        UIASCRIPT = ru.anaysisIniFile('./config.ini', 'instruments_options', 'UIASCRIPT')
        document = os.path.join(self.workoutpath, ru.anaysisIniFile('./config.ini', 'instruments_options', 'document'))
        application = ru.anaysisIniFile('./config.ini', 'instruments_options', 'application')
        outputfilename = os.path.join(self.workoutpath, ru.anaysisIniFile('./config.ini', 'instruments_options' \
                                                                          , 'outputfilename'))
        cmd = "instruments -w {0} -D {1} -t {2} {3} -e UIASCRIPT {4} -e UIARESULTSPATH {5}  -v > {6}  2>&1" \
            .format(devicename, document, template, application, UIASCRIPT, self.workoutpath, outputfilename)
        util.RunUtil().execCMD(cmd)

    def start(self):
        test_times = ru.anaysisIniFile('./config.ini', 'run_args', 'test_times')
        result = [['id', 'result', 'path', 'start_time', 'end_time', 'run_time(/s)']]
        for i in xrange(1, int(test_times) + 1):
                print '启动第' + str(i) + '次测试'
                dir = self.creatDir()
                print dir
                start_time = datetime.datetime.now()
                self.runJsScripts()
                print '开始等待执行waitingForStop方法'
                test_result_id = self.waitingForStop()
                print test_result_id
                if test_result_id == 1:
                    test_result = 'success'
                elif test_result_id == 0:
                    test_result = 'crash'
                elif test_result_id == -1:
                    #注意锁屏及退回桌面等异常情况处理
                    test_result = 'start error'
                print str(i) + ':' + test_result
                end_time = datetime.datetime.now()
                diff_time = (end_time - start_time).total_seconds()
                ru.killProcess("/bin/instruments")
                zipresultpath = os.path.join(self.workresult, '{1}_{0}_result.zip'. \
                                             format(''.join(self.workoutpath.split('/')[-2:]), 'the_' + str(i) + '_test_log'))
                print 'zipresultpath:' + zipresultpath
                ru.zip_dirorfile(self.workoutpath, zipresultpath)
                result_item = [i, test_result, ''.join(self.workoutpath.split('/')[-2:]), start_time.strftime("%Y-%m-%d %H:%M:%S"), end_time.strftime("%Y-%m-%d %H:%M:%S"), diff_time]
                result.append(result_item)
        insertdata('result.xlsx', 'result', result)
        return result
def main():
    ru = util.RunUtil()
    workdir = os.path.dirname(os.path.realpath(sys.argv[0]))
    workout = os.path.join(workdir, 'out')
    workresult = os.path.join(workdir, 'result')
    #1.检查是否有out这个文件夹，此文件夹用于讲log输出保存d的子文件夹
    if not os.path.exists(workout):
        os.mkdir(workout)
    if not os.path.exists(workresult):
        os.mkdir(workresult)
    #2.在out文件下面新建测试文件夹
    workoutpath = os.path.join(workout, util.RunUtil().getCurTime())
    if not os.path.exists(workoutpath):
        os.mkdir(workoutpath)
    mtc = MonkeyTestClient(workout, workdir, workoutpath, workresult)
    mtc.start()

    resultzip = os.path.join(workdir, 'result.zip')
    ru.zip_dirorfile(workresult, resultzip)
    resultxlsx = os.path.join(workdir, 'result.xlsx')
    attachs = [resultxlsx, resultzip]
    print attachs
    summary = 'to do'
    sendmailadd = ru.anaysisIniFile('./config.ini', 'mail', 'address')
    mailutil.sendemailto(sendmailadd, attachs, summary)
    mtc.teardown()
'''
if __name__ == "__main__":
    workdir = os.path.dirname(os.path.realpath(sys.argv[0]))
    workout = os.path.join(workdir, 'out')
    workresult = os.path.join(workdir, 'result')
    #1.检查是否有out这个文件夹，此文件夹用于讲log输出保存d的子文件夹
    if not os.path.exists(workout):
        os.mkdir(workout)
    if not os.path.exists(workresult):
        os.mkdir(workresult)
    #2.在out文件下面新建测试文件夹
    workoutpath = os.path.join(workout, util.RunUtil().getCurTime())
    if not os.path.exists(workoutpath):
        os.mkdir(workoutpath)
    mtc = MonkeyTestClient(workdir, workoutpath, workresult)
    mtc.start()

    resultzip = os.path.join(workdir, 'result.zip')
    ru.zip_dirorfile(workresult, resultzip)
    resultxlsx = os.path.join(workdir, 'result.xlsx')
    attachs = [resultxlsx, resultzip]
    print attachs
    summary = 'to do'
    sendmailadd = ru.anaysisIniFile('./config.ini', 'mail', 'address')
    mailutil.sendemailto(sendmailadd, attachs, summary)
    mtc.teardown()
'''