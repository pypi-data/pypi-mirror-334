# -*- encoding: utf-8 -*-
"""
@File    :   DemoModule.py
@Time    :   2022-10-25 20:17
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
import platform
from os import getenv, environ
from subprocess import getoutput

os_type = 'Windows'
os_arch = platform.machine()
os_ver = platform.release()
home_dir = ''
os_release = platform.release()
username = getenv("USER")
uid = 1
if platform.system().lower() == 'linux':
	home_dir = environ["HOME"]
	os_type = getoutput("""grep ^ID /etc/os-release | sed 's/ID=//' | sed -n 1p | sed 's#\"##g'""")
	os_ver = getoutput(cmd="""grep ^Min /etc/os-version | awk -F '=' '{print $2}'""")
	if str(os_type).lower() == 'kylin'.lower():
		os_ver = getoutput(cmd="""cat /etc/kylin-build | sed -n 2p | awk '{print $2}'""")
	uid = getoutput('echo $UID')
else:
	home_dir = environ["USERPROFILE"]
	username = environ["USERNAME"]
