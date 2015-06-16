# -*- coding:utf-8 -*-

import subprocess, signal
import os

# p = subprocess.Popen("ps -A | grep  /bin/instruments | grep -v grep", stdout=subprocess.PIPE, shell = True)
# out, err = p.communicate()
# for line in out.splitlines():
#     print line
#     pid = int(line.split(None, 1)[0])
#     print pid
#     os.system('kill {0}'.format(pid))
i = 10
while i>1:
    i = i - 1
    print i
    if i < 5:
        break
print 'end'