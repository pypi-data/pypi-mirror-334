# -*- encoding: utf-8 -*-
"""
@File    :   DPKG.py
@Time    :   2022-09-05 09:17
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
from .Cmd import NewCommand
from .logger import ColorLogger
from os import path


class NewDpkg:
	def __init__(self, password, log=False, terminal=False):
		"""
		Apt 管理类的构造函数，用于初始化 Apt 管理对象。

		:param password: str, 主机密码，用于执行需要权限的命令。
		:param log: bool, 可选参数，默认为 False。是否启用日志记录功能。
		:param terminal: bool, 可选参数，默认为 False。是否使用终端执行命令（仅对某些 Linux 发行版有效）。
		:return: None
		"""
		# 初始化当前查询的版本信息
		self.local_package_version = ''
		# 初始化当前包名称
		self.local_package_name = ''
		# 初始化获取状态标志，默认为 False
		self.get_status = False

		# 配置日志和终端执行标志
		self.log = log
		self.terminal = terminal
		self.password = password

		# 创建命令执行对象，用于检查 apt 是否存在
		self.cmd = NewCommand(password=self.password, cmd='which apt', terminal=self.terminal, logs=self.log)

		# 初始化日志记录器
		self.logger = ColorLogger()

		# 初始化需要安装的安装包文件信息
		self.file_install = ''

		# 初始化可安装的文件列表
		self.install_list = []

		# 初始化格式错误的文件列表
		self.format_err = []

		# 初始化不存在的文件列表
		self.not_err = []


	def _show(self):
		"""
		显示信息，包括可安装的文件列表、格式错误的文件列表以及不存在的文件列表。

		参数:
			self: 当前对象实例，包含以下属性：
				- install_list: 可安装的文件列表（list类型）。
				- format_err: 格式错误的文件列表（list类型）。
				- not_err: 不存在的文件列表（list类型）。
				- logger: 日志记录器，用于记录信息、警告和错误。

		返回值:
			无返回值。
		"""
		# 如果存在可安装的文件列表，则打印并记录相关信息
		if self.install_list:
			self.logger.info('可安装的文件列表如下')
			for i in self.install_list:
				print(i)

		# 如果存在格式错误的文件列表，则打印并记录警告信息
		if self.format_err:
			self.logger.warning('格式错误的文件列表如下')
			for i in self.format_err:
				print(i)

		# 如果存在不存在的文件列表，则打印并记录错误信息
		if self.not_err:
			self.logger.error('不存在的文件列表如下')
			for i in self.not_err:
				print(i)


	def _add_file(self, file):
		"""
		检测并添加文件到安装列表中，同时记录格式错误或不存在的文件。

		:param file: 待检测的文件路径（str），可以是绝对路径或相对路径。
		:return: 无返回值，但会更新类的以下属性：
				 - self.file_install: 记录有效的安装文件路径字符串。
				 - self.install_list: 记录有效的安装文件路径列表。
				 - self.not_err: 记录不存在的文件路径列表。
				 - self.format_err: 记录格式不正确的文件路径列表。
		"""
		# 提取文件扩展名并转换为小写，用于判断文件格式是否为 'deb'
		f_name = str(file).split('.')[-1]

		# 如果文件格式为 'deb'，进一步检查文件是否存在
		if str(f_name).lower() == 'deb':
			if path.isfile(file):
				# 如果文件存在，将其添加到安装文件路径字符串和安装列表中
				self.file_install = str(self.file_install) + " " + str(file)
				self.install_list.append(file)
			else:
				# 如果文件不存在，记录错误日志并将其添加到不存在文件列表中
				self.logger.error('列表中检测到不存在的安装包: %s' % str(file))
				self.not_err.append(file)
		else:
			# 如果文件格式不正确，记录警告日志并将其添加到格式错误文件列表中
			self.logger.warning('列表中检测到格式不正确的文件: %s' % str(file))
			self.format_err.append(file)


	def install(self, deb_file=None, name=None):
		"""
		安装本地的deb安装包文件。

		:param deb_file: 需要安装的deb文件路径（建议使用绝对路径）。如果需要安装多个文件，请使用列表传入。
		:param name: 任务名称，用于标识安装任务。如果未提供，默认生成一个名称。
		:return: 安装结果，返回布尔值（True表示安装成功，False表示安装失败）。
		"""
		# 初始化安装列表，用于存储待安装的文件信息
		self.install_list = []

		# 检查deb_file是否为列表，如果是，则逐一添加文件到安装列表
		if type(deb_file) == list:
			for i in deb_file:
				self.logger.debug("Check :", str(i))
				self._add_file(file=i)
		# 如果deb_file是字符串类型，则直接添加单个文件到安装列表
		else:
			if type(deb_file) == str:
				self._add_file(file=deb_file)

		# 如果安装列表不为空，则执行安装操作
		if self.install_list:
			self.logger.info("Installing %s ..." % self.file_install)
			# 构造dpkg安装命令
			cmd = str("dpkg -i %s" % self.file_install)
			# 如果未提供任务名称，则根据安装文件数量生成默认名称
			if name is None:
				name = 'Install %s Packages' % len(self.install_list)
			# 调用sudo命令执行安装，并返回安装结果
			return self.cmd.sudo(cmd=cmd, name=name)
		else:
			# 如果安装列表为空，记录错误日志并显示相关信息
			self.logger.error('没有找到可安装的文件信息')
			self._show()

		# 如果没有任何文件被安装，返回False
		return False


	def configure(self):
		"""
		运行dpkg命令配置所有未完成配置的软件包。

		:return: 配置结果(bool)
		"""
		return self.cmd.sudo(cmd="dpkg --configure -a", name='Continue configuring all Packages')

	def uninstall(self, pac, name=None):
		"""
		卸载指定的软件包。

		:param name: 任务名称，如果未提供，则自动生成一个。
		:param pac: 需要卸载的包名称，例如：docker.io。
		:return: 卸载结果(bool)，成功与否。
		"""
		# 构建卸载软件包的命令
		cmd = str("dpkg -P %s" % pac)
		# 如果没有提供任务名称，则自动生成一个
		if name is None:
			name = 'UnInstall %s' % pac
		# 记录卸载操作的日志信息
		self.logger.info("UnInstalling %s ..." % name)
		# 执行卸载命令，并返回结果
		return self.cmd.sudo(cmd=cmd, name=name)

	def check_local_pac_version(self, pac=None, pac2=None, pac_v=None):
		"""
		检查已安装软件版本是否正确。

		:param pac: 软件包名称（不支持仅传入关键词）。
		:param pac2: 软件包关键词2（如果传入该值，则使用两个关键词进行匹配）。
		:param pac_v: 标准版本，用于与已安装版本进行比较。
		:return: 返回布尔值，表示已安装的软件版本是否与标准版本一致。
		"""
		# 初始化状态标志为 False
		self.get_status = False

		# 构造命令以查询已安装的软件包信息
		cmd = """dpkg -l | grep %s | awk '{print $1,$2,$3}'""" % pac
		if pac2 is not None:
			# 如果提供了第二个关键词，则在命令中加入额外的过滤条件
			cmd = """dpkg -l | grep %s | grep %s | awk '{print $1,$2,$3}'""" % (pac, pac2)

		# 执行命令并解析输出
		info = self.cmd.getout(cmd=cmd).split(' ')
		if self.cmd.code == 0:
			# 如果命令执行成功，提取软件包名称和版本信息
			self.local_package_name = info[1]
			self.local_package_version = info[2]
			self.logger.debug('already installed: ', pac)

			# 检查软件包状态是否正常
			if str(info[0]) == 'ii':
				self.get_status = True
				self.logger.debug("Normal status")

				# 检查软件包名称是否匹配
				if str(info[1]).lower() == str(pac).lower():
					self.logger.debug("Matching succeeded")

					# 检查软件包版本是否匹配
					if str(info[2]) == str(pac_v):
						return True
					else:
						self.logger.warning("Version mismatch")
				else:
					self.logger.warning("Software matching failed")
			else:
				self.logger.warning("Damaged")
		return False


	def get_local_pac_version(self, pac, pac2=None):
		"""
		获取本地包版本，通过调用 `check_local_pac_version` 方法进行版本检查。

		参数:
			pac (str): 包名称，用于指定需要检查的软件包。
			pac2 (str, optional): 软件包关键词2。如果传入该值，则使用两个关键词进行匹配。默认为 None。

		返回:
			bool: 获取结果，表示是否成功获取本地包版本。
		"""
		# 调用 check_local_pac_version 方法进行版本检查，传递包名称和可选的第二个关键词
		self.check_local_pac_version(pac=pac, pac2=pac2, pac_v='get_local_pac_version')

		# 返回获取状态，表示操作是否成功
		return self.get_status
