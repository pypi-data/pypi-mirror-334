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
import socket

import psutil
from socket import SocketKind
from .logger import ColorLogger


class NewListen:
	def __init__(self, pid=None):
		"""
		初始化函数，用于通过指定的进程ID（PID）获取监听的端口。

		:param pid: int, optional
			目标进程的PID。如果未提供，则默认为None。
		:return: None
			无返回值。
		"""
		# 初始化实例变量，存储传入的PID
		self.pid = pid

		# 创建日志记录器实例，用于记录日志信息
		self.logger = ColorLogger()

		# 初始化一个空列表，用于存储监听的端口信息
		self.port_list = []



	def get_listen_list(self):
		"""
		获取当前进程监听的所有端口，并将监听的端口号存储到实例属性 `port_list` 中。

		:return: bool
			- True: 成功获取监听端口列表。
			- False: 获取失败（例如进程不存在）。
		"""
		# 初始化存储监听端口的列表
		self.port_list = []

		try:
			# 获取指定 PID 的进程对象
			process = psutil.Process(self.pid)
			# 获取该进程的所有网络连接信息
			connections = process.net_connections()

			# 遍历连接信息，筛选出状态为 LISTEN 的连接
			for conn in connections:
				if conn.status == 'LISTEN':
					# 将监听的端口号添加到 port_list 中
					self.port_list.append(conn.laddr.port)

		except psutil.NoSuchProcess:
			# 捕获进程不存在的异常，并记录错误日志
			self.logger.error(f"进程不存在: PID={self.pid}")
			return False
		except psutil.AccessDenied:
			# 捕获权限不足的异常，并记录错误日志
			self.logger.error(f"无法访问进程信息: 权限不足, PID={self.pid}")
			return False
		except Exception as e:
			# 捕获其他异常，并记录详细错误信息
			self.logger.error(f"获取监听端口失败: {str(e)}, PID={self.pid}")
			return False

		# 如果没有监听的端口，port_list 为空，但仍返回 True
		if not self.port_list:
			self.logger.info(f"进程 PID={self.pid} 没有监听任何端口")

		# 返回是否成功获取监听端口列表
		return True



	def get_listen_list_tcp(self):
		"""
		获取指定进程监听的所有TCP端口。

		本函数通过psutil库获取当前进程的网络连接信息，筛选出状态为LISTEN且类型为TCP的连接，
		并将监听的端口号存储到实例变量`self.port_list`中。

		:return: bool
			- True: 成功获取监听端口列表。
			- False: 获取失败（例如进程不存在）。
		"""
		# 初始化存储监听端口的列表
		self.port_list = []

		try:
			# 获取当前进程的Process对象
			process = psutil.Process(self.pid)
			# 获取该进程的所有网络连接信息
			connections = process.net_connections()

			# 遍历所有连接，筛选出状态为LISTEN且类型为TCP的连接
			for conn in connections:
				if conn.status == 'LISTEN' and conn.type == SocketKind.SOCK_STREAM:
					# 将监听的端口号添加到列表中
					self.port_list.append(conn.laddr.port)

		except psutil.NoSuchProcess:
			# 捕获进程不存在的异常，并记录错误日志
			self.logger.error("进程不存在: ", self.pid)
			return False

		# 返回是否成功获取监听端口列表
		return True


	def get_listen_list_udp(self):
		"""
		获取当前进程监听的所有端口（仅限UDP协议）。

		该函数通过psutil库获取指定进程的网络连接信息，筛选出状态为"LISTEN"且协议为UDP的连接，
		并将监听的端口号存储到实例变量`self.port_list`中。

		:return:
			- True: 如果成功获取监听端口列表。
			- False: 如果指定的进程不存在或发生异常。
		"""
		self.port_list = []  # 初始化端口列表，用于存储监听的端口号

		try:
			# 获取当前进程的Process对象
			process = psutil.Process(self.pid)

			# 获取该进程的所有网络连接信息
			connections = process.net_connections()

			# 遍历所有连接，筛选出状态为"LISTEN"且协议为UDP的连接
			for conn in connections:
				if conn.status == 'LISTEN' and conn.type == psutil.SOCK_DGRAM:
					# 将监听的端口号添加到端口列表中
					self.port_list.append(conn.laddr.port)
		except psutil.NoSuchProcess:
			# 捕获进程不存在的异常，并记录错误日志
			self.logger.error(f"进程不存在: PID={self.pid}")
			return False
		except psutil.AccessDenied:
			# 捕获权限不足地异常，并记录错误日志
			self.logger.error(f"权限不足，无法访问进程: PID={self.pid}")
			return False
		except Exception as e:
			# 捕获其他未知异常，并记录错误日志
			self.logger.error(f"发生未知异常: PID={self.pid}, 错误信息={str(e)}")
			return False

		# 返回True表示成功获取监听端口列表
		return True



	def get_listen_list_v4(self):
		"""
		获取进程监听的所有IPV4端口
		:return: 如果成功获取监听列表则返回 True，否则返回 False
		"""
		try:
			# 初始化局部变量以存储监听端口
			port_list = []

			# 获取进程对象
			process = psutil.Process(self.pid)

			# 获取网络连接信息
			connections = process.net_connections()

			# 遍历连接并筛选符合条件的监听端口
			for conn in connections:
				if conn.status == 'LISTEN' and conn.family == 2:  # 确保是 IPv4 的监听状态
					port_list.append(conn.laddr.port)

			# 将结果赋值给实例变量
			self.port_list = port_list

			# 如果没有监听端口，返回 False
			if not port_list:
				self.logger.warning(f"进程 {self.pid} 没有监听任何 IPv4 端口")
				return False

			return True
		except psutil.ZombieProcess:
			self.logger.error(f"进程为僵尸进程: PID={self.pid}")
			return False
		except psutil.NoSuchProcess:
			self.logger.error(f"进程不存在: PID={self.pid}")
			return False
		except psutil.AccessDenied:
			self.logger.error(f"权限不足，无法访问进程: PID={self.pid}")
			return False
		except Exception as e:
			self.logger.error(f"获取监听列表时发生未知错误: PID={self.pid}, 错误信息={str(e)}")
			return False


	def get_listen_list_v6(self):
		"""
		获取进程监听的所有IPV6端口
		:return: bool
			- True: 成功获取监听端口列表。
			- False: 获取失败（例如进程不存在）。
		"""
		# 定义常量，避免硬编码
		IPV6_FAMILY = socket.AF_INET6

		# 初始化存储监听端口的列表
		self.port_list = []

		try:
			# 获取指定 PID 的进程对象
			process = psutil.Process(self.pid)
			# 获取该进程的所有网络连接信息
			connections = process.net_connections()

			# 遍历连接信息，筛选出状态为 LISTEN 且为 IPv6 的连接
			for conn in connections:
				if conn.status == 'LISTEN' and conn.family == IPV6_FAMILY:
					# 将监听的端口号添加到 port_list 中
					self.port_list.append(conn.laddr.port)

			# 如果没有找到任何监听端口，记录日志
			if not self.port_list:
				self.logger.info(f"进程 PID={self.pid} 没有监听任何 IPv6 端口")

		except psutil.NoSuchProcess:
			# 捕获进程不存在的异常，并记录错误日志
			self.logger.error(f"进程不存在: PID={self.pid}")
			return False
		except psutil.AccessDenied:
			# 捕获权限不足地异常，并记录错误日志
			self.logger.error(f"权限不足，无法访问进程信息: PID={self.pid}")
			return False
		except Exception as e:
			# 捕获其他异常，并记录详细错误信息
			self.logger.error(f"获取监听端口失败: {str(e)}, PID={self.pid}")
			return False

		# 返回是否成功获取监听端口列表
		return True



# 主程序入口，用于执行监听列表获取的操作。
# 参数:
#   无
# 返回值:
#   无

if __name__ == "__main__":
	# 创建一个 NewListen 实例，传入 pid 参数为 5184。
	p = NewListen(pid=5184)

	# 调用 get_listen_list_v4 方法尝试获取 IPv4 监听列表。
	if p.get_listen_list_v4():
		# 如果获取成功，打印成功信息及监听的端口列表。
		print("获取成功")
		print(p.port_list)
	else:
		# 如果获取失败，打印失败信息。
		print("获取失败")
