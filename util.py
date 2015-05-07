# -*- coding:utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : util
# Description   : 工具类
# Creation      : 2015年4月22日
# Author        : gancj@ucweb.com
###########################################################################

import subprocess
import ConfigParser
import os, sys
import time
import zipfile

class RunUtil():
    def __init__(self):
        return

    def killProcess(self, process_name):
        '''结束进程.
        Args:
            process_name：需结束的进程名称
        Returns:无
        '''
        p = subprocess.Popen("ps -A | grep {0} | grep -v grep".format(process_name), stdout=subprocess.PIPE, shell = True)
        out, err = p.communicate()
        for line in out.splitlines():
            print line
            pid = int(line.split(None, 1)[0])
            print pid
            os.system('kill {0}'.format(pid))


    def killInstruments(self):
        '''结束进程.
        Args:无
        Returns:无
        '''
        processList = os.system("ps -ef | grep \"/Instruments\" | grep -v grep | awk {'print $2'}")
        print str(processList) + 'processlist'
        if processList != "":
            os.system("kill -9 $(ps -ef | grep \"/AutomationInstrument.bundle\" | head -n 1 | grep -v grep | awk {'print $2'})")

    def execCMD(self, cmd):
        handle = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return handle

    def anaysisIniFile(self, filepath, section, key):
        cf = ConfigParser.ConfigParser()
        cf.read(filepath)
        return cf.get(section, key)

    def getDevID(self):
        '''获取真机设备udid.
        Args:无
        Returns:无
        '''
        all_devid = os.popen('system_profiler SPUSBDataType | grep "Serial Number:.*" | sed s#".*Serial Number: "##').readlines()
        devid = ''
        i = 0
        while (i < len(all_devid)):
            if len(all_devid[i]) >= 40:
                devid = all_devid[i].replace("\n", '')
                break
            i += 1
        return devid

    def getCurTime(self):
        return time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))

    def zip_dirorfile(self, dirname, zipfilename):
        filelist = []
        if os.path.isfile(dirname):
            filelist.append(dirname)
        else:
            for root, dirs, files in os.walk(dirname):
                for name in files:
                    filelist.append(os.path.join(root, name))

        zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
        for tar in filelist:
            arcname = tar[len(dirname):]
            #print arcname
            zf.write(tar, arcname)
        zf.close()


    def unzip_file(self, zipfilename, unziptodir):
        if not os.path.exists(unziptodir): os.mkdir(unziptodir, 0777)
        zfobj = zipfile.ZipFile(zipfilename)
        for name in zfobj.namelist():
            name = name.replace('\\','/')

            if name.endswith('/'):
                os.mkdir(os.path.join(unziptodir, name))
            else:
                ext_filename = os.path.join(unziptodir, name)
                ext_dir= os.path.dirname(ext_filename)
                if not os.path.exists(ext_dir) : os.mkdir(ext_dir, 0777)
                outfile = open(ext_filename, 'wb')
                outfile.write(zfobj.read(name))
                outfile.close()

if __name__ == "__main__":
    ru = RunUtil()
    workdir = os.path.dirname(os.path.realpath(sys.argv[0]))
    workout = os.path.join(workdir, 'out')
    workresult = os.path.join(workdir, 'result')
    ru.zip_dirorfile(workresult, os.path.join(workdir, 'result.zip'))