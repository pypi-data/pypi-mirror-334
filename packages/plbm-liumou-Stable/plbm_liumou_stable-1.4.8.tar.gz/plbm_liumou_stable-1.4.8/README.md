# PythonLinuxBasicModule

由于工作中需要编写大量的Linux平台管理脚本、而其中大部分代码都是重复的，所以为了更好的开发效率，我决定将日常Linux管理脚本中用到的基础功能集合起来并使用开源都方式共享，同时也希望有更多人能够一起完善。

## 简介

[PythonLinuxBasicModule Gitee项目](https://gitee.com/liumou_site/plbm)（Python Linux基础模块: `plbm`）是使用Python3进行编写的一个开源系统管理工具，
通过封装Linux系统都软件包管理、磁盘管理、文件管理、网络管理、安全管理、服务管理等内容从而实现快速开发的效果。


## 特色

* 使用全中文注释，即使小白也能轻松上手
* 完全使用内置模块进行开发，拿来即用
* 使用Python基础语法进行编写，兼容新旧版本Python3，告别语法冲突(例如3.5及以下版本无法使用f"{}"语法)
* 完全开源、永久免费


# 更新内容

## `1.4.6`

* 修正新模块异常


# 使用方法

## 安装

具体可以访问Pypi项目地址[https://pypi.org/project/plbm-liumou-Stable/](https://pypi.org/project/plbm-liumou-Stable/)

### 安装-作为系统/用户模块

```shell
pip3 install --upgrade plbm_liumou_Stable ColorInfo -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 安装-作为项目模块

直接进入你的项目根目录,然后执行下面的命令即可

```shell
git clone https://gitee.com/liumou_site/PythonLinuxBasicModule.git
cd PythonLinuxBasicModule
python3 install.py
```


# Demo

## 包管理

```shell
root@l:~/data/git/PythonLinuxBasicModule/demo# cat package.py 
# -*- encoding: utf-8 -*-
"""
@File    :   demo.py
@Time    :   2022-10-24 22:45
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
from plbm_liumou_Stable import NewPackageManagement
from ColorInfo import ColorLogger



class ServiceManager:
	def __init__(self, pac, password):
		self.package = pac
		self.pac = NewPackageManagement(password=password, package="vsftpd")
		self.logger = ColorLogger(class_name=self.__class__.__name__)

	def remove(self):
		if self.pac.installed():
			self.logger.info(f"已安装: {self.package}")
			if self.pac.uninstall():
				self.logger.info(f"卸载成功: {self.package}")
			else:
				self.logger.error(f"卸载失败: {self.package}")

		else:
			self.logger.warning(f"未安装: {self.package}")


if __name__ == "__main__":
	demo = ServiceManager(pac="vsftpd", password="demo")
	demo.remove()
root@l:~/data/git/PythonLinuxBasicModule/demo# python3 package.py 
/usr/lib/python3/dist-packages/requests/__init__.py:91: RequestsDependencyWarning: urllib3 (1.26.12) or chardet (3.0.4) doesn't match a supported version!
  RequestsDependencyWarning)
2023-01-06 22:42:31 Jurisdiction.py  line: 79 - Class: Jurisdiction Function: verification - INFO : 已处于root权限
2023-01-06 22:42:31 Cmd.py  line: 188 - Class: ComMand Function: getout - DEBUG : dpkg -s vsftpd
2023-01-06 22:42:31 Package.py  line: 141 - Class: NewPackageManagement Function: installed - INFO : 已安装: vsftpd
2023-01-06 22:42:31 package.py  line: 23 - Class: ServiceManager Function: remove - INFO : 已安装: vsftpd
2023-01-06 22:42:31 Dpkg.py  line: 113 Function: uninstall - INFO : UnInstalling UnInstall vsftpd ...
(Reading database ... 92009 files and directories currently installed.)
Removing vsftpd (3.0.3-12) ...
Purging configuration files for vsftpd (3.0.3-12) ...
locale: Cannot set LC_MESSAGES to default locale: No such file or directory
locale: Cannot set LC_ALL to default locale: No such file or directory
Processing triggers for man-db (2.8.5-2) ...
Processing triggers for systemd (241-7~deb10u8) ...
[ UnInstall vsftpd ] 执行成功
2023-01-06 22:42:36 package.py  line: 25 - Class: ServiceManager Function: remove - INFO : 卸载成功: vsftpd

```

## 服务管理-Demo

```shell
root@l:~/data/git/PythonLinuxBasicModule# cat demo.py 
# -*- encoding: utf-8 -*-
"""
@File    :   demo.py
@Time    :   2022-10-24 22:45
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
from plbm_liumou_Stable import NewServiceManagement
from ColorInfo import ColorLogger


class ServiceManager:
	def __init__(self, services, password):
		self.services = services
		self.manager = NewServiceManagement(service=services, password=password)
		self.logger = ColorLogger(class_name=self.__class__.__name__)

	def restart(self):
		if self.manager.restart(reload=True):
			self.logger.info("服务重启成功")
		else:
			self.logger.warning("服务重启失败")


if __name__ == "__main__":
	demo = ServiceManager(services="vsftpd", password="demo")
	demo.restart()
root@l:~/data/git/PythonLinuxBasicModule# python3 demo.py 
/usr/lib/python3/dist-packages/requests/__init__.py:91: RequestsDependencyWarning: urllib3 (1.26.12) or chardet (3.0.4) doesn't match a supported version!
  RequestsDependencyWarning)
[ 重载服务配置 ] 执行成功
[ Restart vsftpd ] 执行成功
2023-01-06 22:36:41 Service.py  line: 141 - Class: NewServiceManagement Function: restart - INFO : 重启成功: vsftpd
2023-01-06 22:36:41 demo.py  line: 23 - Class: ServiceManager Function: restart - INFO : 服务重启成功
root@l:~/data/git/PythonLinuxBasicModule# 
```
