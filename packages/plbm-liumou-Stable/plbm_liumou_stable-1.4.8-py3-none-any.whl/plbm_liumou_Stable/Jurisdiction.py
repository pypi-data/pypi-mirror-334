#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   Jurisdiction.py
@Time    :   2022/04/25 16:54:45
@Author  :   村长
@Version :   1.0
@Contact :   liumou.site@qq.com
@Desc    :   权限验证模块
"""

from os import system
from subprocess import getoutput

from .logger import ColorLogger
from .OsInfo import OsInfo


class Jurisdiction:
	def __init__(self, passwd, logs=False, log_file=None):
		"""
		初始化函数，用于设置主机密码、日志配置以及操作系统类型。

		:param passwd: str，设置主机密码，用于权限验证。
		:param logs: bool，可选参数，默认为False。指示是否启用文本日志功能。
		:param log_file: str，可选参数，默认为None。指定日志文件的路径，仅在logs为True时生效。
		:return: None
		"""
		# 初始化日志文件和日志开关
		self.log_file = log_file
		self.logs = logs

		# 配置日志记录器，根据是否启用日志决定日志记录器的行为
		self.loggers = ColorLogger(class_name=self.__class__.__name__)
		if self.logs:
			self.loggers = ColorLogger(class_name=self.__class__.__name__,
									   txt=self.logs, file=self.log_file)

		# 设置主机密码和超级权限标志
		self.passwd = passwd
		self.super_permissions = False

		# 获取当前操作系统的类型
		self.os_type = OsInfo().os_type


	def reset_pd(self):
		"""
		重置密码的函数。

		该函数会尝试两次检查状态，如果状态检查通过则返回True；否则提示用户输入密码并再次检查。
		如果两次尝试均失败，则记录错误日志并返回False。

		:return:
			- True: 如果状态检查通过。
			- False: 如果两次尝试后状态检查仍未通过。
		"""
		# 获取当前系统用户名
		username = getoutput('echo $USER')

		# 循环两次尝试检查状态
		for i in range(2):
			status = self._check()  # 调用内部方法检查状态
			if status:
				return True  # 如果状态检查通过，直接返回True
			else:
				# 如果状态检查未通过，提示用户输入密码
				self.passwd = input("请输入用户[ %s ]登录密码:\n" % username)

		# 如果两次尝试均失败，记录错误日志并返回False
		self.loggers.error("重试次数超过程序设置值")
		return False


	def _check(self):
		"""
		检查密码是否正确。

		该函数通过尝试使用密码执行sudo命令来验证密码的正确性。
		具体步骤包括创建一个临时文件并立即删除它，以测试sudo权限和密码的有效性。

		:return: 如果密码正确且用户具有sudo权限，返回True；否则返回False。
		:rtype: bool
		"""
		# 构造用于测试sudo权限的命令，尝试创建一个临时文件
		c = "echo %s | sudo -S touch /d" % self.passwd

		# 构造用于清理的命令，删除临时文件
		d = "echo %s | sudo -S rm -f /d" % self.passwd

		# 执行创建临时文件的命令，并获取返回值
		res = system(c)

		# 检查命令执行结果，返回值为0表示成功
		if str(res) == '0':
			# 如果命令成功执行，删除临时文件并记录日志
			system(d)
			self.loggers.info("密码正确")
			return True

		# 如果命令执行失败，记录错误日志
		self.loggers.error('密码错误或者当前用户无sudo权限')
		return False


	def verification(self, name, reset=False):
		"""
		检测sudo权限是否能够获取并设置正确的密码, 最终密码可以通过实例变量获取(self.passwd)
		:param name: 调用的任务名称
		:param reset: 是否使用对话模式设置正确密码(默认False)
		:return: 是否取得sudo权限(True取得/False未取得)
		"""
		# 获取当前用户名和UID
		username = getoutput('echo $USER')
		uid = getoutput("echo $UID")

		# 如果当前用户是root或UID为0，则认为已经具有sudo权限
		if str(username).lower() == 'root' or str(uid) == '0':
			if self.logs:
				self.loggers.info('已处于root权限')
			return True

		# 针对UOS操作系统特别处理，尝试获取开发者权限
		if self.os_type.lower() == 'uos'.lower():
			self.developer()
		else:
			# 对于其他操作系统，直接尝试获取sudo权限
			self.super_permissions = True

		# 已具有sudo权限，根据reset参数决定是否重置密码
		if self.super_permissions:
			if reset:
				return self.reset_pd()
			else:
				return self._check()

		# 如果以上条件都不满足，返回False表示未取得sudo权限
		return False

	def developer(self):
		"""
		检查是否开启开发者模式
		Returns:
			bool: 是否开启开发者模式
		"""
		# 读取第一个开发者模式文件的内容
		dev_file = "/var/lib/deepin/developer-install_modes/enabled"
		dev1 = str(getoutput(cmd="cat %s") % dev_file).replace(" ", '').replace('\n', '')

		# 读取第二个开发者模式文件的内容
		dev_file2 = "/var/lib/deepin/developer-install_mode/enabled"
		dev2 = str(getoutput(cmd="cat %s") % dev_file2).replace(" ", '').replace('\n', '')

		# 读取第三个开发者模式文件的内容
		dev_file3 = "cat /var/lib/deepin/developer-mode/enabled"
		dev3 = str(getoutput(cmd=dev_file3)).replace(" ", '').replace('\n', '')

		# 初始化终端模式标志为False
		terminal_mode = False

		# 如果任意一个开发者模式文件中包含"1"，则认为开发者模式已开启
		if dev1 == "1" or dev2 == "1" or dev3 == "1":
			terminal_mode = True
		# 如果当前用户ID不是0且用户名为"root"，或用户ID为0，也认为开发者模式已开启
		elif str(getoutput('echo $UID')) != '0' and str(getoutput('echo $USER')) == "root" or str(
				getoutput('echo $UID')) == '0':
			terminal_mode = True

		# 设置当前实例的超级权限标志为终端模式标志
		self.super_permissions = terminal_mode

		# 如果超级权限标志为True，则记录日志并返回True
		if self.super_permissions:
			self.loggers.info('已开启开发者模式')
			return True
		# 否则，记录警告日志并返回False
		else:
			self.loggers.warning('开发者模式未开启')
			return False


# 主程序入口
if __name__ == "__main__":
	# 创建Jurisdiction类的实例，传入密码参数
	ju = Jurisdiction(passwd='1')
	# 调用verification方法进行密码验证
	if ju.verification(name='Demo'):
		# 如果验证成功，打印提示信息
		print('密码验证正确')
	else:
		# 如果验证失败，打印提示信息
		print('密码验证失败')
