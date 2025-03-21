#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   Rename.py
@Time    :   2022-08-10 11:12
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   Linux系统文件重命名工具
"""
from argparse import ArgumentParser
from os import path, getcwd, walk
from subprocess import getstatusoutput
from sys import exit


class FileRename:
	def __init__(self, path, log, debug=False):
		"""
		文件重命名工具
		:param path: 需要操作的文件/文件夹路径
		"""
		self.path = path
		self.log = log
		self.debug = debug
		self.success_list = []
		self.fail_list = []
		self.skip_list = []
		self.exists_list = []
		self.file_list = []

	def writer(self, filename, data):
		"""
		写入文件
		:param filename: 文件名称
		:param data: 数据列表
		:return:
		"""
		try:
			w = open(file=filename, mode='w+', encoding='utf8')
			for info in data:
				ws = str("%s\n" % info)
				print(info)
				w.write(ws)
			w.close()
		except Exception as e:
			print(e)

	def info(self):
		"""
		打印最终结果
		:return:
		"""
		Summary_file = path.join(self.log, 'Summary.txt')
		i = ["重命名成功的数量: %s" % len(self.success_list),
		     "重命名失败的数量: %s" % len(self.fail_list),
		     "跳过重命名的数量: %s " % len(self.skip_list),
		     "文件不存在的数量: %s" % len(self.exists_list)]
		self.writer(filename=Summary_file, data=i)
		success = path.join(self.log, 'success.txt')
		self.writer(filename=success, data=self.success_list)

		fail = path.join(self.log, 'fail.txt')
		self.writer(filename=fail, data=self.fail_list)
		skip = path.join(self.log, 'skip.txt')
		self.writer(filename=skip, data=self.skip_list)

		exists = path.join(self.log, 'exists.txt')
		self.writer(filename=exists, data=self.exists_list)

	def replace(self, filename, old_str, new_str=''):
		"""
		文件名字符串替换工具
		:param filename: 需要替换文件名的文件/文件夹的绝对路径
		:param old_str: 需要替换的旧字符串
		:param new_str: 需要使用的新字符串
		:return:
		"""
		if path.exists(filename):
			new_file = str(filename).replace(old_str, new_str)
			if path.exists(new_file):
				print("新文件已存在,跳过替换: ", new_file)
				self.skip_list.append(filename)
			else:
				cmd = "mv %s %s" % (filename, new_file)
				if self.debug:
					print(cmd)
				if getstatusoutput(cmd)[0] == 0:
					print("重命名成功: [ %s -> %s ]" % (filename, new_file))
					self.success_list.append(filename)
				else:
					print("重命名失败: [ %s -> %s ]" % (filename, new_file))
					self.fail_list.append(filename)
		else:
			print("文件不存在,无需重命名: ", filename)
			self.exists_list.append(filename)

	def file_sub(self, dir_path=None):
		"""
		获取文件夹下所有子文件
		:param dir_path: 文件夹路径
		:return:
		"""
		if dir_path is None:
			dir_path = self.path
		for dirpath, dirnames, filenames in walk(dir_path):
			for filename in filenames:
				self.file_list.append(path.join(dirpath, filename))

	def ccc(self):
		"""
		野王的去换行符
		:return:
		"""
		self.file_sub()
		for file in self.file_list:
			self.replace(filename=file, old_str='\r', new_str='')
		self.info()


if __name__ == "__main__":
	py_ver = "2022.8.10.1754"
	pwd = getcwd()
	arg = ArgumentParser(description='当前脚本版本: %s' % py_ver, prog="XC在线检查")
	arg.add_argument('-p', '--path', type=str,
	                 help='设置需要重命名的文件夹路径', required=True)
	arg.add_argument('-d', '--debug', type=int, default=0,
	                 help='是否开启调试, 默认: 0', required=False)
	arg.add_argument('-l', '--log', type=str, default=pwd,
	                 help='设置日志记录文件夹路径, 默认: %s' % pwd,
	                 required=False)
	args = arg.parse_args()
	path_ = args.path
	d_ = args.debug
	log_ = args.log
	debug = False
	if int(d_) == 1:
		debug = True
	up = FileRename(path=path_, debug=debug, log=log_)
	up.ccc()
