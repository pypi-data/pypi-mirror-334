# -*- encoding: utf-8 -*-
"""
@File    :   Process.py
@Time    :   2022-09-05 09:17
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   进程信息获取
"""
import psutil
from .logger import ColorLogger

class NewProcess:
	def __init__(self, cmd):
		"""
		通过命令查找进程ID
		:param cmd: 需要查找的已运行的命令，例如：nginx。
					要求为非空字符串，且不应包含非法字符。
		"""
		# 输入校验：确保 cmd 是非空字符串
		if not isinstance(cmd, str) or not cmd.strip():
			raise ValueError("cmd 参数必须是非空字符串")

		# 初始化属性
		self.cmd = cmd.strip()  # 去除首尾空白字符，增强健壮性
		self.pid = None         # 进程ID
		self.ppid = None        # 父进程ID
		self.logger = ColorLogger(class_name=self.__class__.__name__)


	def get_pid(self, cmd=None):
		"""
		通过命令获取PID
		:param cmd: 可选: 传入需要获取的命令(默认使用实例化的初始参数/最后一次传参(优先)的参数)
		:return: bool(结果赋值到self.pid)
		"""
		# 校验输入参数
		if cmd is not None:
			self.cmd = cmd
		if not isinstance(self.cmd, str) or not self.cmd.strip():
			raise ValueError("self.cmd 必须是一个非空字符串")

		self.pid = None  # 初始化 PID

		try:
			# 遍历进程列表
			for proc in psutil.process_iter(['pid', 'name']):
				if proc.info['name'] == self.cmd:
					self.pid = proc.info['pid']
					return True
		except (psutil.Error, Exception) as e:
			# 捕获 psutil 可能抛出的异常
			self.logger.error(f"获取进程信息时发生错误: {e}")
			return False

		return False


	def get_ppid_cmd(self, cmd=None):
		"""
		通过命令获取父进程ID（PPID）。

		:param cmd: 可选参数，传入需要获取的命令。如果未提供，则使用实例化的初始参数或最后一次传参的参数。
		:return: bool类型，表示是否成功获取PPID。如果成功，结果会赋值到self.ppid。
		"""
		# 如果提供了cmd参数，则更新self.cmd为传入的cmd值
		if cmd is not None:
			self.cmd = cmd

		# 初始化self.ppid为None
		self.ppid = None

		# 调用get_pid方法获取PID，如果失败则记录日志并返回False
		if not self.get_pid():
			self.logger.warning("Failed to retrieve PID. Ensure the process is running and accessible.")
			return False

		# 尝试获取父进程ID（PPID）
		try:
			# 使用psutil模块获取当前进程的父进程ID（PPID）
			process = psutil.Process(self.pid)
			self.ppid = process.ppid()
			return True

		except psutil.AccessDenied:
			# 捕获权限不足的异常
			self.logger.error(f"Access denied for process with PID {self.pid}.")
		except psutil.ZombieProcess:
			# 捕获僵尸进程的异常
			self.logger.error(f"Process with PID {self.pid} is a zombie process.")
		except psutil.NoSuchProcess:
			# 捕获进程不存在的异常
			self.logger.error(f"Process with PID {self.pid} not found.")
		except Exception as e:
			# 捕获其他未知异常
			self.logger.error(f"An unexpected error occurred while retrieving PPID: {e}")

		# 如果未能成功获取PPID，返回False
		return False



	def get_ppid_pid(self, pid=None):
		"""
		通过Pid获取Ppid
		:param pid: 需要获取的PID父进程
		:return: bool(结果赋值到self.ppid)
		"""
		# 参数校验与初始化
		if pid is not None:
			if not isinstance(pid, int) or pid <= 0:
				self.logger.error(f"Invalid PID value: {pid}")
				return False
			self.pid = pid
		elif self.pid is None:
			self.logger.error("PID is not set and no valid PID provided")
			return False

		# 初始化 ppid
		self.ppid = None

		try:
			# 获取父进程ID
			process = psutil.Process(self.pid)
			self.ppid = process.ppid()
			return True


		except psutil.AccessDenied:
			self.logger.error(f"Access denied for process with PID {self.pid}")
		except psutil.ZombieProcess:
			self.logger.error(f"Process with PID {self.pid} is a zombie process")
		except psutil.NoSuchProcess:
			self.logger.error(f"Process with PID {self.pid} not found")
		except Exception as e:
			self.logger.error(f"An unexpected error occurred while retrieving PPID: {e}")

		return False

