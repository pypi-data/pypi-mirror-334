# -*- encoding: utf-8 -*-
"""
@File    :   Apt.py
@Time    :   2022-09-05 09:17
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
from .Cmd import NewCommand
from .logger import ColorLogger
from .Jurisdiction import Jurisdiction
from os import path


class NewApt:
	def __init__(self, password, log=False, terminal=False, package=None, file=None):
		"""
		Apt 管理类的构造函数，用于初始化 Apt 管理对象。

		:param password: str, 主机密码，用于权限验证和命令执行。
		:param log: bool, 可选参数，默认为 False。是否启用日志记录功能。
		:param terminal: bool, 可选参数，默认为 False。是否使用终端执行命令（仅对某些 Linux 发行版有效）。
		:param package: str, 可选参数，默认为 None。需要处理的包名。
		:param file: str, 可选参数，默认为 None。日志文件路径。
		:return: None
		"""
		# 初始化包名、终端标志、日志标志和密码
		self.package = package
		self.terminal = terminal
		self.log = log
		self.password = password

		# 权限验证模块，确保当前用户有权限执行 Apt 管理操作
		ju = Jurisdiction(passwd=password, log_file=file)
		if not ju.verification(name='AptManagement'):
			exit(1)

		# 初始化命令执行模块，用于检查系统中是否存在 apt 工具
		self.cmd = NewCommand(password=self.password, cmd='which apt', terminal=self.terminal, logs=self.log)

		# 初始化日志记录器，用于记录操作日志
		self.logger = ColorLogger(file=file, txt=log, class_name=self.__class__.__name__)

		# 需要处理的包文件列表
		self.deb_pac_list = []

		# 实际存在的包文件列表
		self.deb_ok_list = []

		# 不存在的包文件列表
		self.deb_not_exists = []

		# 最终安装的包字符串
		self.deb_install_str = ''

		# 当前查询到的本地包版本
		self.local_package_version = ''

		# 当前查询到的本地包名称
		self.local_package_name = ''

		# 当前获取状态标志，用于标记是否成功获取包信息
		self.get_status = False


	def install(self, pac='git', update=False):
		"""
		安装在线包。

		:param pac: 需要安装的包名称，类型为字符串，默认值为 'git'。
		:param update: 是否在安装前更新源索引，类型为布尔值，默认值为 False。
		:return: 安装结果，类型为布尔值，表示安装是否成功。
		"""
		# 如果 update 参数为 True，则更新源索引
		if update:
			self.update_index()

		# 记录日志，表明正在安装指定的包
		self.logger.debug("Installing %s ..." % pac)

		# 构造安装命令，使用 apt 工具安装指定的包
		cmd = str("apt install -y %s" % pac)

		# 执行安装命令，并返回安装结果
		return self.cmd.sudo(cmd=cmd, name='Install %s' % pac)


	def update_index(self):
		"""
		更新索引

		该函数用于通过执行系统命令更新软件源的索引信息。

		参数:
			无

		返回值:
			bool: 更新操作的结果，True 表示成功，False 表示失败。
		"""
		# 调用 sudo 命令执行 "apt update"，并指定操作名称为 "Update Sources Index"
		return self.cmd.sudo(cmd="apt update", name="Update Sources Index")


	def installed(self, pac=None):
		"""
		查询是否已安装指定的包。

		:param pac: str, 可选参数，表示需要查询的包名。如果未提供，则使用实例属性 self.package。
		:return: bool, 返回是否已安装指定的包。如果包已安装，返回 True；否则返回 False。
		"""
		# 如果未传入包名参数，则使用实例属性 self.package
		if pac is None:
			pac = self.package

		# 如果包名仍然为空，记录错误日志并退出程序
		if pac is None:
			self.logger.error('未传入有效包名')
			exit(2)

		# 执行系统命令 "dpkg -s <包名>" 查询包的安装状态
		self.cmd.getout(cmd="dpkg -s %s" % pac)

		# 根据命令执行的返回码判断包是否已安装
		# 返回码为 0 表示包已安装，返回 True；否则返回 False
		if self.cmd.code == 0:
			return True
		return False


	def local_install_f(self, file):
		"""
		实现通过APT安装本地Debian包的功能，等效于执行命令 `apt install -y -f ./install.deb`。

		:param file: str
			指定要安装的本地Debian包文件路径。
		:return: bool
			返回安装结果，True表示安装成功，False表示安装失败。
		"""
		# 调用sudo命令执行APT安装操作，并传递安装包文件路径作为参数
		return self.cmd.sudo(cmd="apt install -y -f %s" % file, name='Install Local Package')


	def install_f(self):
		"""
		执行 `apt install -y -f` 命令以修正环境。此功能需要谨慎使用，因为如果处理不当，
		可能会对系统组件造成损害。

		参数:
			无

		返回值:
			bool: 表示命令执行结果的布尔值，True 表示成功，False 表示失败。

		重要代码块说明:
			1. 调用 `self.update_index()` 更新包索引，确保在执行安装命令前索引是最新的。
			2. 使用 `self.cmd.sudo` 执行 `apt install -y -f` 命令，尝试修复系统依赖关系。
		"""
		self.update_index()
		return self.cmd.sudo(cmd="apt install -y -f", name='Install Local Package')


	def reinstall_rc(self, update=False):
		"""
		一键修复 rc 状态的包列表。

		:param update: 是否更新源索引，默认为 False（不会更新源索引）。
		:return: 执行结果，返回布尔值 (bool)，表示命令执行是否成功。
		"""
		# 如果 update 参数为 True，则更新源索引
		if update:
			self.update_index()

		# 构造命令以重新安装所有处于 rc 状态的包
		# rc 状态表示包已被卸载但保留了配置文件
		# 通过 dpkg -l 查找 rc 状态的包，并使用 apt 重新安装
		cmd = "apt install -y --reinstall `dpkg -l | grep -v ii  | grep rc | awk '{print $2}' | sed '1,5 d'`"

		# 执行命令并返回结果
		return self.cmd.sudo(cmd=cmd, name='List of packages to repair rc status', terminal=False)


	def remove_rc(self, update=False):
		"""
		一键卸载 rc 状态的包列表。

		:param update: 是否更新源索引，默认为 False。如果设置为 True，则会在执行卸载前更新源索引。
		:return: 返回执行结果，类型为布尔值 (bool)。True 表示成功执行，False 表示执行失败。
		"""
		# 如果 update 参数为 True，则调用 update_index 方法更新源索引
		if update:
			self.update_index()

		# 构造命令以卸载所有处于 rc 状态的包
		# 1. 使用 dpkg -l 列出所有包，并通过 grep 筛选出状态为 rc 的包
		# 2. 使用 awk 提取包名，并通过 sed 删除前五行（通常是表头信息）
		# 3. 最终通过 apt purge 命令卸载这些包
		cmd = "apt purge -y `dpkg -l | grep -v ii  | grep rc | awk '{print $2}' | sed '1,5 d'`"

		# 调用 sudo 方法执行命令，并返回执行结果
		return self.cmd.sudo(cmd=cmd, name='List of packages in unloaded rc status', terminal=False)


	def upgrade(self, update=True):
		"""
		执行系统软件包升级操作（apt-get upgrade），根据需要决定是否先更新源索引。

		:param update: 是否在升级前更新源索引。如果为True，则会调用update_index()方法更新源索引；如果为False，则跳过索引更新步骤。默认值为True。
		:return: 返回一个布尔值，表示升级操作是否成功完成。
		"""
		# 如果update参数为True，则先更新源索引
		if update:
			self.update_index()

		# 定义执行的命令，使用apt upgrade进行系统升级，并自动处理缺失依赖
		cmd = 'apt upgrade -y --fix-missing'

		# 调用sudo方法执行升级命令，返回执行结果
		return self.cmd.sudo(cmd=cmd, terminal=False, name='更新系统-upgrade')


	def upgrade_dist(self, update=True):
		"""
		执行系统升级命令 `apt-get dist-upgrade`，该命令在升级软件包时会智能处理依赖关系，
		确保系统中所有软件包的依赖关系得到正确解决。

		:param update: 是否在执行升级前更新源索引。如果为 True，则调用 `update_index` 方法更新源索引；
		               如果为 False，则跳过更新源索引步骤。默认值为 True。
		:return: 返回一个布尔值，表示升级操作是否成功。True 表示成功，False 表示失败。
		"""
		# 如果参数 update 为 True，则先更新源索引
		if update:
			self.update_index()

		# 定义执行的命令，使用 apt dist-upgrade 进行系统升级，并添加必要选项
		cmd = 'apt dist-upgrade -y --fix-missing'

		# 调用 sudo 方法执行升级命令，返回执行结果
		return self.cmd.sudo(cmd=cmd, terminal=False, name='更新系统-dist-upgrade')


	def _parse_list(self):
		"""
		解析列表，将 self.deb_pac_list 中的文件路径分类为存在的文件和不存在的文件，
		并生成一个用于安装的字符串。

		:return: 无返回值。该函数的主要作用是更新以下实例变量：
		         - self.deb_install_str: 存在文件的路径拼接成的字符串，用于后续安装操作。
		         - self.deb_ok_list: 存在的文件路径列表。
		         - self.deb_not_exists: 不存在的文件路径列表。
		"""
		# 初始化实例变量
		self.deb_install_str = ''  # 用于存储存在的文件路径拼接字符串
		self.deb_ok_list = []      # 用于存储存在的文件路径列表
		self.deb_not_exists = []   # 用于存储不存在的文件路径列表

		# 遍历 self.deb_pac_list 中的每个文件路径
		for i in self.deb_pac_list:
			if path.isfile(i):  # 检查文件是否存在
				# 如果文件存在，将其添加到存在的文件列表，并更新安装字符串
				self.deb_ok_list.append(i)
				self.deb_install_str = str(self.deb_install_str) + str(" %s" % str(i))
			else:
				# 如果文件不存在，将其添加到不存在的文件列表
				self.deb_not_exists.append(i)


	def local_gui_install_deepin_deb(self, pac=None):
		"""
		使用Dde图形化安装程序(deepin-deb-installer)进行安装。

		:param pac: 传入需要安装的文件路径。
		            - 类型可以是字符串（单个文件路径）或列表（多个文件路径）。
		            - 如果为None，则不会执行安装操作。
		:return:
		        - 返回True表示安装命令已成功执行。
		        - 返回False表示传入的安装文件异常，无法继续安装。
		"""
		# 判断传入的参数是否为列表类型
		if type(pac) == list:
			self.deb_pac_list = pac  # 将传入的列表赋值给deb_pac_list
			self._parse_list()  # 调用解析列表的方法处理deb_pac_list
		else:
			# 如果传入的是单个文件路径，将其赋值给deb_install_str并加入到deb_ok_list中
			self.deb_install_str = pac
			self.deb_ok_list.append(pac)

		# 检查deb_ok_list中是否有待安装的文件
		if len(self.deb_ok_list) >= 1:
			# 如果有待安装文件，记录日志并准备执行安装命令
			self.logger.info("正在进入安装,安装数量: ", len(self.deb_ok_list))
		else:
			# 如果没有待安装文件，记录错误日志并返回False
			self.logger.error("传入的安装文件异常")
			return False

		# 构造deepin-deb-installer命令并执行
		cmd = str("deepin-deb-installer  %s" % self.deb_install_str)
		self.cmd.getout(cmd=cmd)  # 执行安装命令

		# 返回True表示安装命令已成功执行
		return True

