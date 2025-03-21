# -*- encoding: utf-8 -*-
"""
@File    :   CMD.py
@Time    :   2022-09-06 16:16
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   执行系统命令
"""
import platform
from os import system, chdir, path, getcwd, getenv
from subprocess import getstatusoutput, getoutput

from .logger import ColorLogger


class NewCommand:
	def __init__(self, password, cmd=None, terminal=False, logs=False, work=getcwd()):
		"""
		初始化类实例，用于执行系统指令。

		:param terminal: 是否使用图形终端执行命令，默认为False。此参数为全局默认值，子功能可自定义。
		:param password: 主机密码，类型为字符串(string)。
		:param cmd: 需要执行的命令，类型为字符串(string)，默认为None。
		:param logs: 是否启用日志打印信息，默认为False。
		:param work: 工作目录，类型为字符串(string)，默认为当前工作目录。
		:return: 无返回值。
		"""
		# 保存当前工作目录
		self.pwd = getcwd()
		# 设置日志打印标志
		self.logs = logs
		# 切换到指定的工作目录
		chdir(work)
		# 是否使用终端执行命令
		self.terminal = terminal
		# 设置主机密码
		self.password = password
		# 传入初始命令
		self.cmd = cmd
		# 初始化最终命令为空字符串
		self.cmd_ = ''
		# 初始化执行结果标志为False
		self.ok = False
		# 初始化退出状态码为0
		self.code = 0

		# 检查是否有可用终端
		self.use_terminal = False
		# 初始化终端类型为空字符串
		self.terminal_type = ''
		# 初始化终端参数为空字符串
		self.terminal_arg = ''
		# 获取用户主目录路径
		self.home = getenv('HOME')
		# 定义临时脚本文件路径
		self.sh = path.join(self.home, 'run_tmp.sh')
		# 获取当前用户名
		self.user = getoutput('echo $USER')
		# 获取当前用户ID
		self.uid = getoutput('echo $UID')
		# 获取系统类型
		self.os_type = platform.system()
		# 如果系统类型为Linux，则进一步获取具体发行版信息
		if str(self.os_type).lower() == 'linux'.lower():
			self.os_type = getoutput("""grep ^ID /etc/os-release | sed 's/ID=//' | sed -n 1p | sed 's#\"##g'""")

		# 定义日志文件路径
		log_file = path.join(self.home, 'cmd_.log')
		# 初始化日志记录器
		self.logger = ColorLogger(file=log_file, txt=logs, class_name=self.__class__.__name__)
		# 如果启用了终端模式，则获取终端相关信息
		if self.terminal:
			self._get_terminal()


	def create(self):
		"""
		创建命令脚本文件，并设置其可执行权限，最后输出脚本内容。

		参数:
			self.sh (str): 脚本文件的路径或名称。
			self.cmd_ (str): 需要写入脚本文件的命令内容。

		返回值:
			无返回值。

		异常处理:
			如果在文件操作过程中发生异常，会捕获并打印异常信息。
		"""
		try:
			# 打开或创建脚本文件，并写入指定的命令内容
			with open(file=self.sh, mode='w+', encoding='utf-8') as w:
				w.write('#!/bin/bash\n')  # 写入脚本的shebang行
				w.write(self.cmd_)       # 写入具体的命令内容
				w.close()                # 关闭文件流
		except Exception as e:
			# 捕获并打印文件操作中的异常信息
			print(e)

		# 设置脚本文件为可执行权限
		system("chmod +x %s" % self.sh)

		# 输出脚本文件的内容到终端
		system("cat %s" % self.sh)


	def _get_terminal(self):
		"""
		获取当前系统中可用的终端类型，并设置相关属性。

		该函数会检查预定义的终端程序是否存在于系统中。如果找到可用的终端程序，
		则设置 `self.terminal_type` 为终端名称，`self.terminal_arg` 为对应的参数，
		并将 `self.use_terminal` 设置为 True。

		:return: 如果找到可用的终端程序，返回 True；否则返回 False。
		:rtype: bool
		"""
		# 定义支持的终端程序及其启动参数
		t_ = {'mate-terminal': '-e', 'gnome-terminal': '-e', 'deepin-terminal': '-C'}

		# 遍历支持的终端程序，检查其是否存在
		for i in t_:
			cmd = "which %s" % str(i)  # 构造检查命令
			if int(getstatusoutput(cmd)[0]) == 0:  # 检查命令执行结果
				# 如果终端程序存在，设置相关属性并返回 True
				self.terminal_type = str(i)
				self.terminal_arg = t_[i]
				self.use_terminal = True
				return True

			# 如果终端程序不存在，继续检查下一个
			self.terminal = False

		# 如果所有终端程序都不存在，返回 False
		return False


	def terminal_fun(self):
		"""
		使用终端执行命令。

		该函数根据当前对象的终端类型和参数，构造一个终端命令并执行。
		如果无法获取终端类型，则会输出错误信息。

		参数:
			self: 当前对象实例。
				- self._get_terminal(): 方法，用于检查是否能够获取终端类型。
				- self.terminal_type: 字符串，表示终端类型（如 'xterm'）。
				- self.terminal_arg: 字符串，表示终端的启动参数。
				- self.cmd_: 字符串，表示需要在终端中执行的命令。
				- self.logs: 布尔值，表示是否启用日志记录。
				- self.logger: 日志记录器对象，用于记录调试信息。
				- self.os_type: 字符串，表示当前系统的类型。

		返回值:
			无返回值。
		"""
		# 检查是否能够获取终端类型
		if self._get_terminal():
			# 构造终端命令，包含终端类型、参数以及需要执行的命令
			cmd = """%s %s '%s;read -p "请按回车关闭此界面"'""" % (self.terminal_type, self.terminal_arg, self.cmd_)

			# 根据日志开关决定是否记录命令到日志中
			if self.logs:
				self.logger.debug(cmd)
			else:
				print(cmd)

			# 执行构造的终端命令
			getoutput(cmd)
		else:
			# 如果无法获取终端类型，输出错误信息
			print('找不到终端类型,当前系统类型: %s' % self.os_type)


	def shell(self, cmd=None, terminal=None):
		"""
		执行普通Shell命令。

		:param cmd: str, 可选参数，需要执行的命令。如果未提供，则使用实例初始化时的默认命令 (self.cmd)。
		:param terminal: bool, 可选参数，是否使用终端执行命令。如果未提供，则使用实例初始化时的默认值 (self.terminal)。
		:return: bool, 当未使用终端且命令执行成功时返回 True，否则返回 False。
				 如果发生异常，会记录错误日志但不会抛出异常。
		"""
		# 如果未提供命令，则使用实例初始化时的默认命令
		if cmd is None:
			cmd = self.cmd

		# 如果未指定是否使用终端，则使用实例初始化时的默认值
		if terminal is None:
			terminal = self.terminal

		# 将命令赋值给实例变量 self.cmd_，便于后续使用
		self.cmd_ = cmd

		# 根据日志开关决定是记录日志还是直接打印命令
		if self.logs:
			self.logger.debug(self.cmd_)
		else:
			print(self.cmd_)

		# 如果启用了终端模式并且实例允许使用终端，则调用终端相关函数
		if terminal and self.use_terminal:
			self.terminal_fun()
		else:
			try:
				# 执行命令并获取返回码
				self.code = system(self.cmd_)
			except Exception as e:
				# 捕获异常并记录错误日志
				self.logger.error(str(e))

			# 根据返回码判断命令执行是否成功
			if int(self.code) == 0:
				return True
			return False


	def sudo(self, cmd=None, terminal=None, name=None):
		"""
		执行sudo命令。

		:param cmd: 需要执行的命令，默认使用实例初始命令 (self.cmd)。
		:param terminal: 是否使用终端执行（创建新进程，无法获取执行结果），默认使用实例值 (self.terminal)。
		:param name: 任务名称，用于标识任务。
		:return:
			- 如果 terminal 等于 True，则直接返回 True。
			- 否则返回命令执行结果 (bool)，并将退出代码赋予 self.code。
		"""
		# 如果未提供 cmd 参数，则使用实例的初始命令
		if cmd is None:
			cmd = self.cmd

		# 如果未提供 terminal 参数，则使用实例的默认值
		if terminal is None:
			terminal = self.terminal

		# 构造 sudo 命令，包含密码输入
		self.cmd_ = str("""echo %s | sudo -S %s""" % (self.password, cmd))

		# 如果当前用户为 root 或 UID 为 0，则无需使用 sudo
		if str(self.user).lower() == 'root' or str(self.uid) == '0':
			self.cmd_ = cmd

		# 如果需要通过终端执行且允许使用终端，则调用终端执行函数
		if terminal and self.use_terminal:
			self.terminal_fun()
			if name:
				print("[ %s ] 已通过终端执行" % str(name))
			return True
		else:
			# 初始化执行状态信息
			mess = '执行成功'
			ok = True
			try:
				# 执行命令并获取退出代码
				self.code = system(self.cmd_)
			except Exception as e:
				# 捕获异常并记录错误日志
				self.logger.error(str(e))

			# 根据退出代码判断命令是否执行成功
			if int(self.code) != 0:
				mess = '执行失败'
				ok = False

			# 如果未提供任务名称，则使用命令本身作为名称
			if name is None:
				name = self.cmd_

			# 打印任务执行结果
			print("[ %s ] %s" % (str(name), str(mess)))

			# 更新实例的执行状态并返回结果
			self.ok = ok
			return self.ok


	def getout(self, cmd=None):
		"""
		获取命令输出。

		:param cmd: 需要执行的命令，默认为None。如果未提供，则使用实例初始化时的默认命令（self.cmd）。
		:return: 返回执行命令的标准输出（str类型）。执行结果的状态码会存储在实例属性self.code中。
		"""
		# 如果未提供cmd参数，则使用实例初始化时的默认命令
		if cmd is None:
			cmd = self.cmd
		# 检查cmd是否仍然为None，如果是，则记录错误并返回None
		if cmd is None:
			self.logger.error("未提供命令")
			return None
		# 如果传入的是列表，则将其转换为字符串命令
		if isinstance(cmd, list):
			cmd = ' '.join(cmd)
		# 如果启用了日志记录功能，将命令内容记录到调试日志中
		if self.logs:
			self.logger.debug(cmd)

		# 执行命令并获取状态码和输出结果
		i = getstatusoutput(cmd)

		# 将命令执行的状态码存储到实例属性self.code中
		self.code = i[0]

		# 返回命令执行的标准输出
		return i[1]


	def getout_sudo(self, cmd=None, name=None, debug=None, mess_ok=None, mess_failed=None):
		"""
		获取sudo权限命令输出。

		:param cmd: 需要执行的命令，默认使用实例初始命令（self.cmd）。
		:param name: 任务名称，默认为完整命令字符串。
		:param debug: 是否开启调试模式，若为None则使用实例的默认日志设置（self.logs）。
		:param mess_ok: 执行成功时的提示信息，默认为“执行成功”。
		:param mess_failed: 执行失败时的提示信息，默认为“执行失败”。
		:return: 返回执行命令的标准输出（str），执行结果的状态码可通过self.code获取。
		"""
		# 设置默认的成功和失败提示信息
		if mess_ok is None:
			mess_ok = '执行成功'
		if mess_failed is None:
			mess_failed = '执行失败'

		# 如果未提供命令，则使用实例初始化时的默认命令
		if cmd is None:
			cmd = self.cmd
		if cmd is None:
			self.logger.error("未提供命令")
			return None
		# 如果传入的是列表
		if isinstance(cmd, list):
			cmd = ' '.join(cmd)

		# 构造带有sudo权限的命令字符串
		cmd = str("echo %s | sudo -S %s" % (self.password, cmd))

		# 如果未提供任务名称，则使用完整命令作为名称
		if name is None:
			name = cmd

		# 如果开启调试模式，记录命令到日志中
		if debug:
			self.logger.debug(cmd)

		# 如果debug参数未指定，则使用实例的默认日志设置
		if debug is None:
			debug = self.logs

		# 执行命令并获取状态码和输出
		i = getstatusoutput(cmd)
		self.code = i[0]

		# 根据执行结果输出成功或失败信息
		if int(self.code) == 0:
			if debug:
				print("[ %s ] %s" % (str(name), str(mess_ok)))
		else:
			if debug:
				print("[ %s ] %s" % (str(name), str(mess_failed)))

		# 返回命令的标准输出
		return i[1]


	def echo_to_file(self, file, cmd):
		"""
		将指定命令的输出追加到目标文件中。

		:param file: 目标文件的路径，例如: /etc/sysctl.conf。
					该文件必须具有可写权限，否则需要通过sudo提升权限。
		:param cmd: 需要执行的命令字符串，例如: echo 123。
				   该命令的输出将被追加到目标文件中。
		:return: 无返回值。
		"""
		# 使用系统命令验证当前用户的sudo权限，并确保密码正确
		system("echo {0} | sudo -S pwd".format(self.password))

		# 构造命令，将cmd的输出通过sudo权限追加到目标文件中
		cmd = str("{0} | sudo tee -a {1}".format(cmd, file))

		# 调用shell方法执行构造的命令，terminal=False表示不使用交互式终端
		self.shell(cmd=cmd, terminal=False)



	def add_path(self, paths):
		"""
		追加指定路径到用户的PATH环境变量中。

		:param paths: 需要追加的路径字符串，表示要添加到PATH中的路径。
		:return: 如果路径已经存在于PATH中，则返回False；如果成功添加路径，则返回True；
				 如果在操作过程中发生异常，则返回False。
		"""
		# 获取当前PATH环境变量，并处理可能为空的情况
		current_path = getenv("PATH")
		if current_path is None:
			self.logger.error("Environment variable PATH is not set.")
			return False

		# 将PATH环境变量按冒号分割成列表，保持原始大小写
		path_list = current_path.split(":")

		# 检查需要追加的路径是否已存在于PATH中
		if str(paths) in path_list:
			self.logger.debug("Path '%s' already exists in PATH." % paths)
			return False

		# 打印提示信息，表明正在将路径添加到PATH中
		self.logger.info("Add [ %s ] To PATH" % paths)

		# 定位到用户主目录下的.bashrc文件
		file = path.join(self.home, '.bashrc')

		try:
			# 使用 with 语句管理文件操作，确保文件句柄正确关闭
			with open(file=file, mode='a', encoding='utf8') as w:
				txt_path = str("\nexport PATH=${{PATH}}:%s" % paths)
				w.write(txt_path)
			return True
		except Exception as e:
			# 捕获异常并记录详细的错误日志
			self.logger.error(str("Failed to add path '%s' to file '%s': %s"% (paths, file, e)))
			return False


