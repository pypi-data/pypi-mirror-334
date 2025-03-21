#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   install.py
@Time    :   2022-10-25 10:51
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   安装模块
"""
from os import system, getcwd, path


class Install:
	def __init__(self):
		self.pwd = getcwd()
		self.w = './PythonLinuxBasicModule'
		self.dir = path.join(self.w, 'src/plbm_liumou_Stable')

	def cmd(self, cmd, name):
		"""

		:param cmd:
		:param name:
		:return:
		"""
		res = system(cmd)
		if int(res) == 0:
			print("%s 成功" % name)
			return True
		else:
			print("%s 失败" % name)
		return False

	def check(self):
		"""
		检查
		:return:
		"""
		if path.isdir(self.dir):
			cmd = "cp -rf %s ." % self.dir
			return self.cmd(cmd=cmd, name='Copy')
		else:
			print('路径不存在: %s' % self.dir)
		return False

	def delete(self):
		cmd = "rm -rf %s" % self.w
		self.cmd(cmd=cmd, name='Delete')

	def start(self):
		"""

		:return:
		"""
		if self.check():
			self.delete()


if __name__ == "__main__":
	install = Install()
	install.start()
