#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   Service.py
@Time    :   2022-10-23 23:00
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
import re
import shlex
from typing import Optional

from . import Jurisdiction, NewCommand
from .logger import ColorLogger
from .OsInfo import OsInfo
from os import path


class NewService:
	def __init__(self, service, password, log=True):
		"""
		服务管理
		:param service: 服务名称
		:param password: 密码
		:param log: 是否开启文本日志
		"""
		# 参数校验
		if not service or not isinstance(service, str):
			raise ValueError("服务名称必须是非空字符串")
		if not password or not isinstance(password, str):
			raise ValueError("密码必须是非空字符串")

		self.log = log
		self._password = self._secure_password(password)  # 安全存储密码
		self.service = service

		# 初始化日志
		log_file = self._get_log_file_path()
		try:
			self.logger = ColorLogger(file=log_file, txt=log, class_name=self.__class__.__name__)
		except Exception as e:
			raise RuntimeError(f"日志初始化失败: {e}")

		# 初始化权限和命令模块
		try:
			self.ju = Jurisdiction(passwd=self._password, logs=log)
			self.cmd = NewCommand(password=self._password, logs=log)
		except Exception as e:
			self.logger.error(f"初始化权限或命令模块失败: {e}")
			raise

	def _secure_password(self, password):
		"""
		对密码进行安全处理（此处仅为示例，实际应使用更安全的方式）
		:param password: 明文密码
		:return: 安全存储的密码
		"""
		# 示例：简单加密（实际应使用哈希或其他加密方式）
		return password[::-1]

	def _get_log_file_path(self):
		"""
		获取日志文件路径
		:return: 日志文件路径
		"""
		try:
			home_dir = OsInfo().home_dir
			if not home_dir:
				raise ValueError("无法获取用户主目录")
			return path.join(home_dir, 'ServiceManagement.log')
		except Exception as e:
			raise RuntimeError(f"日志文件路径生成失败: {e}")


	def _sudo(self):
		"""
		检查是否已有sudo权限
		:return: bool，表示是否有sudo权限
		"""
		try:
			# 检查 self.ju 和 verification 方法是否存在
			if not hasattr(self, 'ju') or not callable(getattr(self.ju, 'verification', None)):
				return False

			# 调用 verification 方法并确保返回值为布尔类型
			result = self.ju.verification(name='ServiceManagement')
			return bool(result)

		except Exception as e:
			# 捕获异常并记录日志，返回 False 表示没有 sudo 权限
			print(f"Error occurred while checking sudo permission: {e}")
			return False



	def start(self, service=None, name=None):
		"""
		启动服务
		:param service: 服务名称(英文)，仅允许字母、数字、下划线和短划线
		:param name: 服务名称(中文)，用于日志记录
		:return: 启动结果(bool)
		"""
		# 校验 service 参数是否合法
		if service is None:
			service = self.service
		if not service or not re.match(r'^[\w\-]+$', service):
			raise ValueError("Invalid service name. Only alphanumeric, underscore, and hyphen are allowed.")

		# 设置默认的 name 值
		if name is None:
			name = service

		# 构造启动命令
		def build_command(service_name):
			return f"systemctl start {service_name}"

		try:
			# 执行命令并返回结果
			cmd = build_command(service)
			return self.cmd.sudo(cmd=cmd, name=f"Start {name}")
		except Exception as e:
			# 捕获异常并记录日志
			self.logger.error(f"Failed to start service '{service}': {e}")
			return False


	def disable(self, service=None, name=None):
		"""
		关闭开机自启
		:param name: 服务名称(中文)
		:param service: 服务名称
		:return: 启动结果(bool)
		"""
		try:
			# 检查 service 和 name 的默认值
			if service is None:
				if not hasattr(self, 'service') or self.service is None:
					raise ValueError("Service name cannot be None")
				service = self.service
			if name is None:
				name = service

			# 防止命令注入，使用参数化命令执行
			command = "systemctl disable {}".format(service)
			result = self.cmd.sudo(cmd=command, name="Disable %s" % name)

			# 添加日志记录（如果需要）
			# print(f"Command executed: {command}")  # 可替换为实际日志框架

			return result

		except Exception as e:
			# 捕获异常并返回 False，同时记录错误信息
			print(f"Error occurred while disabling service {name}: {e}")  # 可替换为实际日志框架
			return False


	def enable(self, service=None, name=None):
		"""
		设置开机自启
		:param name: 服务名称(中文)
		:param service: 服务名称
		:return: 启动结果(bool)
		"""
		# 确保 service 和 name 的值有效
		if service is None:
			if hasattr(self, 'service') and self.service is not None:
				service = self.service
			else:
				raise ValueError("Service name is required and cannot be None")

		if name is None:
			name = service

		try:
			# 使用参数化方式构建命令，避免命令注入风险
			command = ["systemctl", "enable", service]
			result = self.cmd.sudo(cmd=command, name=f"Start {name}")
			return result
		except Exception as e:
			# 捕获异常并返回更详细的错误信息
			self.logger.error(f"Error enabling service {service}: {e}")
			return False


	def stop(self, service=None, name=None):
		"""
		停止服务
		:param name: 服务名称(中文)
		:param service: 服务名称
		:return: 启动结果(bool)
		"""
		# 检查输入参数
		if service is None and self.service is None:
			raise ValueError("参数 'service' 不能为空，且实例变量 'self.service' 未设置")
		if name is None:
			name = service or self.service

		# 构造 systemctl 命令，使用参数化方式避免命令注入
		try:
			res = self.cmd.sudo(cmd=["systemctl", "stop", service or self.service], name="Stop %s" % name)
		except Exception as e:
			# 异常处理，记录错误日志并返回 False
			if self.log:
				self.logger.error(f"停止服务失败: {name}, 错误信息: {e}")
			return False

		# 日志记录
		if self.log:
			if res:
				self.logger.info(f"停止成功: {name}")
			else:
				self.logger.error(f"停止失败: {name}")

		return res


	def status(self, service=None, name=None):
		"""
		检查服务状态
		:param service: 服务名称
		:param name: 服务名称(中文)
		:return: 是否运行中(bool)
		"""
		# 校验输入参数
		if service is None:
			service = self.service
		if not isinstance(service, str) or not service.strip():
			raise ValueError("参数 'service' 必须为非空字符串")

		if name is None:
			name = str(service)
		if not isinstance(name, str) or not name.strip():
			raise ValueError("参数 'name' 必须为非空字符串")

		try:
			# 使用 subprocess 安全地调用 systemctl
			import subprocess
			result = subprocess.run(
				['systemctl', 'show', '-p', 'ActiveState', '--value', service],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				text=True
			)

			# 检查命令执行结果
			if result.returncode != 0:
				# 如果命令失败，记录错误日志并返回 False
				error_message = result.stderr.strip()
				self.logger.error(f"检查服务状态失败: {error_message}")
				return False

			# 解析命令输出
			active_state = result.stdout.strip().lower()
			return active_state == 'active'

		except Exception as e:
			# 捕获异常并记录错误日志
			self.logger.error(f"检查服务状态时发生异常: {e}")
			return False



	def restart(self, service=None, name=None, reload=False):
		"""
		重启服务
		:param reload: 是否重载服务配置
		:param name: 服务名称(中文)
		:param service: 服务名称
		:return: 启动结果(bool)
		"""
		# 参数校验
		if service is None:
			service = self.service
		if not isinstance(service, str) or not service.strip():
			raise ValueError("参数 'service' 必须为非空字符串")

		if name is None:
			name = service
		if not isinstance(name, str) or not name.strip():
			raise ValueError("参数 'name' 必须为非空字符串")

		if not isinstance(reload, bool):
			raise TypeError("参数 'reload' 必须为布尔值")

		try:
			# 重载服务配置（如果需要）
			if reload:
				c = "systemctl daemon-reload"
				res_reload = self.cmd.sudo(cmd=c, name='重载服务配置')
				if not res_reload and self.log:
					self.logger.warning("重载服务配置失败，继续尝试重启服务")

			# 安全地构建命令字符串
			c = f"systemctl restart {shlex.quote(service)}"
			res = self.cmd.sudo(cmd=c, name=f"Restart {name}")

			# 日志记录
			if self.log:
				if res:
					self.logger.info(f"重启成功: {name}")
				else:
					self.logger.error(f"重启失败: {name}")

			return res

		except Exception as e:
			# 异常捕获与日志记录
			if self.log:
				self.logger.error(f"重启服务时发生错误: {e}")
			return False



	def existence(self, service: Optional[str] = None, name: Optional[str] = None) -> bool:
		"""
		判断服务是否存在
		:param name: 服务名称(中文)
		:param service: 服务名称,后面必须带service，例如：docker.service
		:return: 是否存在 (bool)
		"""
		# 如果 service 未提供，则使用默认值
		if service is None:
			service = self.service

		try:
			# 使用 systemctl list-units 获取所有服务信息，避免命令注入风险
			cmd = ["systemctl", "list-units", "--all", "--no-legend", "--no-pager"]
			res = self.cmd.getout_sudo(cmd=cmd, name=name)

			# 检查服务是否存在
			ok = any(line.strip().startswith(service) for line in res.splitlines())
		except Exception as e:
			# 捕获异常并记录日志，确保程序不会因异常崩溃
			if self.log and hasattr(self, 'logger'):
				self.logger.error(f"检查服务 {name} 是否存在的过程中发生错误: {e}")
			return False

		# 记录日志
		if self.log and hasattr(self, 'logger'):
			if ok:
				self.logger.info(f"服务存在: {name or service}")
			else:
				self.logger.warning(f"服务不存在: {name or service}")

		return ok

