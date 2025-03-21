#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import shlex
from os import path
from . import NewCommand, NewApt
from .logger import ColorLogger
from subprocess import getoutput


class Source:
	def __init__(self, passwd, debug=False, mirrors="mirrors.cloud.tencent.com"):
		"""
		初始化类实例的方法。

		参数:
		- passwd: 用于执行命令的密码。
		- debug: 是否启用调试模式，默认为False。
		- mirrors: APT源的镜像地址，默认为"mirrors.cloud.tencent.com"。

		该方法主要负责初始化类的一些基本属性和对象，包括镜像地址、源文件路径、命令执行对象、操作系统类型、APT管理对象和日志记录对象。
		"""
		self.mirrors = mirrors  # 设置APT源的镜像地址
		self.source = '/etc/apt/sources.list'  # APT源文件路径
		self.source_bak = '/etc/apt/sources.list.bak'  # APT源文件备份路径
		self.cmd = NewCommand(password=passwd)  # 创建一个新的命令执行对象
		# 获取操作系统类型，并转换为小写
		self.release = getoutput("cat /etc/os-release  | grep ^ID=").split("=")[1].lower()
		self.apt = NewApt(password=passwd)  # 创建一个新的APT管理对象
		self.logger = ColorLogger(txt=debug)  # 创建一个彩色日志对象，根据debug参数决定是否启用调试模式

	def bak(self):
		"""
		备份源文件到指定备份路径。

		此方法检查备份文件是否已存在，如果不存在且源文件存在，则通过sudo命令执行文件复制操作。
		这用于在修改源文件之前保留一份备份，确保可以恢复原始状态。
		"""
		if not path.isfile(self.source_bak) and path.isfile(self.source):
			# 当备份文件不存在且源文件存在时，执行备份操作
			self.cmd.sudo(cmd="cp -rf %s %s" % (self.source, self.source_bak), name='Bak Sources')


	def process_url(self, cmd, name_prefix):
		"""
		处理 URL 并执行 sed 替换命令。
		:param cmd: 获取 URL 的命令
		:param name_prefix: 日志前缀
		"""
		try:
			# 执行命令并获取输出
			info = str(getoutput(cmd=cmd))
			if len(info) < 5:
				self.logger.info(f"No valid URL found for {name_prefix}. Skipping.")
				return

			# 解析 URL
			url = info.split(" ")[1]
			http_ = url.split(":")[0]
			host_ = url.split("//")[1].split("/")[0]

			# 构造 sed 命令并转义
			http_cmd = "sed -i 's@{0}@https@g' {1}".format(shlex.quote(http_), shlex.quote(self.source))
			host_cmd = "sed -i 's@{0}@{1}@g' {2}".format(shlex.quote(host_), shlex.quote(self.mirrors), shlex.quote(self.source))

			# 执行命令
			self.cmd.sudo(cmd=http_cmd, name=f'{name_prefix}-Http')
			self.cmd.sudo(cmd=host_cmd, name=f'{name_prefix}-Host')

		except IndexError as e:
			self.logger.error(f"IndexError in processing {name_prefix}: {e}")
		except ValueError as e:
			self.logger.error(f"ValueError in processing {name_prefix}: {e}")
		except Exception as e:
			self.logger.error(f"Unexpected error in processing {name_prefix}: {e}")

	def get(self):
		# 处理非 security URL
		cmd = "cat /etc/apt/sources.list | grep ^deb | grep http | sed -n 1p"
		self.process_url(cmd, "non-security")

		# 处理 security URL
		cmd = "cat /etc/apt/sources.list | grep ^deb | grep http | grep security | sed -n 1p"
		self.process_url(cmd, "security")


	def start(self):
		"""
		开始执行主要流程。

		本函数按顺序执行以下操作：
		1. 调用self.bak()进行备份操作。
		2. 调用self.get()获取必要数据或资源。
		3. 调用self.apt.update_index()更新索引。

		这些操作的确切目的和功能依赖于具体实现和上下文。
		"""
		# 首先进行备份操作，确保在后续操作中可以恢复到先前状态
		self.bak()

		# 获取必要的数据或资源，这是执行后续步骤的前提
		self.get()

		# 更新索引，以确保所有数据或资源是最新的并且已正确索引
		self.apt.update_index()

# 主程序入口
if __name__ == "__main__":
	# 创建Source实例，传入密码和调试模式参数
	# 参数passwd用于指定密码，此处简单设为'1'
	# 参数debug指定是否开启调试模式，此处设为True
	s = Source(passwd='1', debug=True)

	# 启动Source实例
	# 此处的start方法负责开始执行与Source相关的操作或任务
	s.start()
