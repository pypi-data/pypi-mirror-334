#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   Package.py
@Time    :   2022-10-23 01:40
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   Linux包管理工具
"""
import os
import subprocess
from typing import Optional

from .Apt import NewApt
from .Cmd import NewCommand
from .Dpkg import NewDpkg
from .Jurisdiction import Jurisdiction
from .Yum import NewYum
from .logger import ColorLogger


class NewPackage:
	def __init__(self, password: str, logs: bool = True,
				file: Optional[str] = None, package: Optional[str] = None):
		"""
		Linux包管理模块
		:param password: 主机密码（敏感参数，处理完成后应立即清除）
		:param logs: 是否开启日志
		:param file: 需要安装的文件路径
		:param package: 需要安装的包名
		"""
		if not password or len(password) < 8:
			raise ValueError("Invalid password format")

		self.logs = logs
		self.file = file
		self.package = package
		self._password = password  # 使用保护属性存储

		# 优先检测包管理工具
		self.install_tools = 'apt'
		try:
			subprocess.run(['which', 'yum'], check=True,
						  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			self.install_tools = 'yum'
		except subprocess.CalledProcessError:
			pass

		# 动态初始化管理对象
		if self.install_tools == 'yum':
			self.manager = NewYum(password=password, log=logs)  # 假设存在对应类
		else:
			self.manager = NewApt(password=password, log=logs)
			self.local = NewDpkg(password=password, log=logs)

		self.cmd = NewCommand(password=password, logs=logs)
		self.ju = Jurisdiction(passwd=password, logs=logs)
		self.logger = ColorLogger(txt=logs,  # 参数重命名避免混淆
								  class_name=self.__class__.__name__)
		self.init()

	
	def init(self):
		"""
		初始化函数，用于根据安装工具类型设置管理器。

		该函数检查当前对象的 `install_tools` 属性值是否为 'yum'（不区分大小写）。
		如果是，则创建一个 `NewYum` 类型的管理器实例，并将其赋值给 `self.manager`。

		:return: 无返回值。
		"""
		if self.install_tools.lower() == 'yum':
			# 如果安装工具为 'yum'，初始化 NewYum 管理器实例
			self.manager = NewYum(password=self._password, log_file=self.file, log=self.logs)
			del self._password


	def check_sudo(self):
		"""
		检测当前用户是否已具备sudo权限。

		本函数通过调用 `self.ju.verification` 方法来验证权限，
		并返回验证结果。

		:return: 返回 `self.ju.verification` 方法的执行结果，
				 通常为布尔值或特定的验证状态。
		"""
		return self.ju.verification(name='PackageManger - check_sudo')

	
	def install(self, package, update=False):
		"""
		在线安装服务。

		:param package: str，需要安装的包名称。
		:param update: bool，可选参数，默认为False。如果为True，则在安装前更新索引。
		:return: bool，安装结果，True表示安装成功，False表示安装失败。
		"""
		# 调用管理器的install方法执行实际的安装操作
		return self.manager.install(pac=package, update=update)

	
	def _format_check(self):
		"""
		检查文件格式是否为支持的格式（deb 或 rpm）。

		参数:
			self: 当前对象实例，包含以下属性：
				- file: 文件路径或文件名，用于检查格式。
				- logs: 布尔值，指示是否记录日志。
				- logger: 日志记录器，用于记录错误信息（仅在 logs 为 True 时使用）。

		返回值:
			bool: 如果文件格式为 deb 或 rpm，返回 True；否则返回 False。
		"""
		# 确保 self.file 是字符串类型
		if not isinstance(self.file, str):
			if self.logs:
				self.logger.error("文件名无效: 输入不是字符串")
			return False

		# 提取文件扩展名并转换为小写
		parts = self.file.split('.')
		if len(parts) < 2:  # 检查是否有扩展名
			if self.logs:
				self.logger.error("文件格式不正确: 缺少扩展名 (%s)", self.file)
			return False

		format_ = parts[-1].lower()  # 缓存扩展名的小写形式

		# 检查文件格式是否为支持的格式
		if format_ in ('deb', 'rpm'):
			return True

		# 如果文件格式不正确且启用了日志记录，则记录错误日志
		if self.logs:
			self.logger.error("文件格式不正确: 不支持的格式 (%s)", self.file)
		return False


	
	def install_local_file_single(self, file=None):
		"""
		安装单个本地安装包文件
		:param file: 需要安装的文件,只能传入一个安装包文件
		:return: 安装结果(bool)
		"""
		# 检查输入参数是否有效
		if not file or not isinstance(file, str) or file.strip() == "":
			if self.logs:
				self.logger.error("无效的文件路径: {0}".format(file))
			return False

		# 更新文件路径
		self.file = file

		try:
			# 格式检查
			if not self._format_check():
				if self.logs:
					self.logger.error("文件格式检查失败: {0}".format(file))
				return False

			# 检查文件是否存在
			if not os.path.isfile(file):
				if self.logs:
					self.logger.error("文件不存在: {0}".format(file))
				return False

			# 调用管理器进行安装
			return self.manager.local_install_f(file=file)

		except Exception as e:
			# 捕获异常并记录日志
			if self.logs:
				self.logger.error("安装过程中发生异常: {0}, 错误信息: {1}".format(file, str(e)))
			return False

	
	def install_local_matching(self, file=None):
		"""
		安装多个本地安装包文件(不检查是否存在文件)
		:param file: 需要安装的文件,可以使用通配符(后缀必须使用文件格式),例如： /root/*.deb
		:return: 安装结果(bool)
		"""
		# 日志配置

		# 参数校验
		if file is not None:
			if not isinstance(file, str):
				self.logger.error("参数 file 必须是字符串类型")
				return False
			if not self._is_valid_path(file):
				self.logger.error(f"无效的文件路径: {file}")
				return False
			self.file = file

		# 格式检查
		if not self._format_check():
			self.logger.error("文件格式检查失败")
			return False

		# 调用安装方法
		try:
			if self.manager is None:
				self.logger.error("manager 未初始化")
				return False
			return self.manager.local_install_f(file=self.file)
		except Exception as e:
			self.logger.error(f"安装过程中发生错误: {e}")
			return False

	def _is_valid_path(self, path: str) -> bool:
		"""
		校验路径是否合法，避免路径注入风险
		:param path: 文件路径
		:return: 是否合法(bool)
		"""
		# 简单校验路径是否包含非法字符或试图访问上级目录
		if ".." in path or not os.path.isabs(path):
			return False
		return True
	def uninstall(self, package=None) -> bool:
		"""
		卸载指定的软件包，使用系统包管理工具（如 apt purge 或 yum remove）进行操作。

		:param package: str, 可选参数，表示需要卸载的软件包名称。如果未提供，则使用实例中已有的 package 属性。
		:return: 调用 self.local.uninstall 方法的返回值，具体返回值类型和内容取决于该方法的实现。
		"""
		# 参数校验：确保 package 是有效的非空字符串
		if package is not None:
			if not isinstance(package, str) or not package.strip():
				raise ValueError("参数 package 必须是非空字符串")
			self.package = package

		# 检查 self.package 是否为空
		if not hasattr(self, 'package') or not self.package:
			raise ValueError("实例属性 package 未设置或为空，无法执行卸载操作")

		try:
			# 调用本地卸载方法，传入当前实例的 package 属性作为参数
			return self.local.uninstall(pac=self.package)
		except Exception as e:
			# 捕获异常并记录错误信息
			raise RuntimeError(f"卸载软件包 {self.package} 失败: {str(e)}") from e


	
	def uninstall_local(self, package=None, name=None):
		"""
		使用(dpkg -P /rpm -e)移除软件包
		:param package: 需要移除的包名称，字符串类型，不能为空
		:param name: 软件包的显示名称，字符串类型，默认值为 self.package
		:return: 卸载结果(bool)，如果卸载过程中发生异常则返回 False
		"""
		# 参数校验
		if package is None or not isinstance(package, str) or not package.strip():
			raise ValueError("参数 'package' 必须是非空字符串")
		if name is not None and (not isinstance(name, str) or not name.strip()):
			raise ValueError("参数 'name' 如果提供，必须是非空字符串")

		# 设置默认值
		if name is None:
			if not hasattr(self, 'package') or not self.package:
				raise AttributeError("参数 'name' 未提供且 self.package 未初始化或为空")
			name = self.package

		try:
			# 调用卸载方法
			return self.local.uninstall(pac=package, name=name)
		except Exception as e:
			# 异常处理
			print(f"卸载软件包时发生异常: {e}")
			return False

	
	def installed(self, pac=None) -> bool:
		"""
		查询服务是否安装
		:param pac: 要查询的服务包名，默认为 None，表示使用 self.package
		:return: bool，表示服务是否已安装
		"""
		# 如果 pac 为 None，则使用 self.package
		if pac is None:
			pac = self.package

		# 检查 pac 是否为有效值
		if pac is None:
			self.logger.error('未提供有效的服务包名')
			return False

		try:
			# 调用 manager 的 installed 方法查询安装状态
			ok = self.manager.installed(pac=pac)
			if ok:
				self.logger.info(f'已安装: {pac}')
			else:
				self.logger.warning(f'未安装: {pac}')
			return ok
		except Exception as e:
			# 捕获异常并记录日志
			self.logger.error(f'查询安装状态时发生错误: {e}')
			return False


	def upgrade(self, update_index=True, dist=True):
		"""
		升级系统。

		:param update_index: 是否更新索引，默认为 True。如果为 True，则在升级前会尝试更新包索引。
		:param dist: 是否执行温柔地更新（针对 apt 工具），默认为 True。如果为 True 且安装工具为 apt，则调用 `upgrade_dist` 方法；否则调用普通 `upgrade` 方法。
		:return: 返回升级操作的结果，具体返回值由 `self.manager.upgrade` 或 `self.manager.upgrade_dist` 方法决定。
		"""
		try:
			# 检查 install_tools 属性是否存在且为有效字符串
			if not hasattr(self, 'install_tools') or not isinstance(self.install_tools, str):
				raise ValueError("self.install_tools 必须是一个有效的字符串")

			# 根据安装工具类型选择不同的升级逻辑
			if self.install_tools.lower() == 'apt':
				if dist:
					# 如果使用 apt 工具且 dist 为 True，调用温柔升级方法
					return self.manager.upgrade_dist(update=update_index)
				else:
					# 如果使用 apt 工具但 dist 为 False，调用普通升级方法
					return self.manager.upgrade(update=update_index)
			else:
				# 对于非 apt 工具，直接调用普通升级方法
				return self.manager.upgrade(update=update_index)

		except AttributeError as e:
			# 捕获属性访问错误并抛出运行时异常
			raise RuntimeError(f"属性访问错误: {e}")
		except Exception as e:
			# 捕获其他异常并抛出运行时异常，包含详细错误信息
			raise RuntimeError(f"升级过程中发生错误: {e}")


