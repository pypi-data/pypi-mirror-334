# -*- encoding: utf-8 -*-
"""
@File    :   Docker.py
@Time    :   2022-10-25 20:57
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   Docker管理功能
"""
from .Cmd import NewCommand
from .Jurisdiction import Jurisdiction
from .logger import ColorLogger
from .Package import NewPackage
from sys import exit
from .File import NewFile
from .Service import NewService


class DockerManagement:
	def __init__(self, password, logs=True, log_file=None, journal=False):
		"""
		Docker管理类的构造函数，用于初始化Docker管理工具的核心组件。

		:param password: str，主机密码，用于权限验证和执行需要sudo权限的操作。
		:param logs: bool，默认为True，是否开启日志记录功能。
		:param log_file: str，默认为None，指定日志文件的路径。如果为None，则不写入文件。
		:param journal: bool，默认为False，是否将日志记录到系统日志中。
		:return: None
		"""
		# 初始化日志记录器，支持日志文件和系统日志记录功能
		self.logs = logs
		self.logger = ColorLogger(file=log_file, txt=journal, class_name=self.__class__.__name__)

		# 验证用户权限，确保当前用户/密码具有sudo权限以执行Docker相关操作
		ju = Jurisdiction(passwd=password)
		if not ju.verification(name='DockerManagement'):
			self.logger.error("当前用户/密码无法获取sudo权限: %s" % password)
			exit(1)

		# 初始化命令执行工具，用于执行Docker相关的命令
		self.cmd = NewCommand(password=password, logs=logs)

		# 初始化包管理工具，用于管理Docker软件包的安装和配置
		self.pac = NewPackage(password=password, logs=logs, file=log_file, package='docker.io')

		# 初始化文件管理工具，用于处理与Docker相关的文件操作
		self.fm = NewFile()

		# 初始化服务管理工具，用于管理Docker服务的启动、停止和状态检查
		self.service = NewService(service='docker.service', password=password, log=logs)


	def check_install(self):
		"""
		检查Docker是否已安装。

		参数:
			self: 当前对象实例，包含以下属性：
				- pac: 一个对象，提供 `installed()` 方法用于检查软件包的安装状态。
				- logger: 一个日志记录器对象，用于记录错误信息。

		返回值:
			bool: 如果 Docker.io 或 Docker-ce 已安装，则返回 True；否则返回 False。
		"""
		# 检查默认的 Docker 是否已安装
		if not self.pac.installed():
			# 如果默认 Docker 未安装，进一步检查 Docker-ce 是否已安装
			if not self.pac.installed(pac='docker-ce'):
				# 如果两者都未安装，记录错误日志并返回 False
				self.logger.error("未安装Docker.io/Docker-ce")
				return False
		# 如果任一版本已安装，返回 True
		return True


	def mirror(self, url="https://mirror.ccs.tencentyun.com"):
		"""
		更改或新增 Docker 的镜像地址，并更新相关配置文件和服务。

		:param url: 镜像地址，默认为 "https://mirror.ccs.tencentyun.com"。
		            该地址将被写入 Docker 的配置文件 daemon.json 中。
		:return: 如果所有操作成功，则返回 True；如果任何一步失败，则返回 False。
		"""
		# 构造包含镜像地址的 JSON 格式字符串，用于写入配置文件
		txt = """{\n\t"registry-mirrors": ["%s"]\n}""" % url

		try:
			# 将构造的 JSON 字符串写入本地的 daemon.json 文件
			with open(file='daemon.json', mode='w', encoding='utf-8') as w:
				w.write(txt)
				w.close()
		except Exception as e:
			# 捕获写入文件时的异常并记录错误日志
			self.logger.error(str(e))
			return False

		try:
			# 将本地的 daemon.json 文件复制到 Docker 的配置目录
			self.fm.copyfile(src='daemon.json', dst='/etc/docker/daemon.json', cover=True)
		except Exception as e:
			# 捕获文件复制时的异常并记录错误日志
			self.logger.error(str(e))
			return False

		try:
			# 重启 Docker 服务以应用新的镜像配置
			self.service.restart(reload=True)
		except Exception as e:
			# 捕获服务重启时的异常并记录错误日志
			self.logger.error(str(e))
			return False

		# 如果所有操作均成功，返回 True
		return True

