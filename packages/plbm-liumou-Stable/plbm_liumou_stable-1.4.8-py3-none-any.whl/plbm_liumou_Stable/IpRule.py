# -*- coding: UTF-8 -*-
"""
设置进程网络走向
"""
from .Process import NewProcess
from .LISTEN import NewListen
from .logger import ColorLogger
from .Nmcli import NewNmcli
from sys import exit


class IpRule:
	def __init__(self, cmd, eth=None):
		"""
		初始化函数，用于将指定命令的流量绑定到一个网卡。

		:param cmd: str
			需要绑定的命令，通常是一个可执行的命令或脚本。
		:param eth: str, optional
			需要绑定的网卡名称。如果未指定，则默认使用第一个处于连接状态的网卡。
		:return: None
			无返回值，初始化过程中会设置实例变量。
		"""
		self.eth = eth  # 指定的网卡名称
		self.cmd = cmd  # 需要绑定的命令
		self.port_list = []  # 用于存储端口列表
		self.eth_list = []  # 已连接的网卡列表
		self.gw = None  # 网关信息，默认为None
		self.pid = None  # 当前进程的PID，默认为None
		self.ppid = []  # 父进程PID列表，默认为空
		self.logger = ColorLogger(class_name=__class__.__name__)  # 初始化日志记录器，用于记录类的操作日志


	def get_status(self):
		"""
		获取命令状态(是否运行中)。

		该函数通过创建一个 NewProcess 对象来检查当前命令的运行状态。
		如果无法获取进程的 PID，则记录错误日志并退出程序。

		:return: 无返回值。
		"""
		# 创建一个 NewProcess 对象以检查命令的运行状态
		p = NewProcess(self.cmd)

		# 如果无法获取 PID，记录错误日志并退出程序
		if not p.get_pid():
			self.logger.error("无法获取Pid")
			exit(2)

		# 将获取到的 PID 赋值给当前对象的 pid 属性
		self.pid = p.pid


	def get_port(self):
		"""
		获取端口列表。

		该函数通过调用 `NewListen` 类的实例方法 `get_listen_list_tcp`，获取与当前进程相关的 TCP 监听端口信息。

		:param self: 当前对象实例，包含 `pid` 属性，用于标识目标进程。
					 - self.pid: 进程 ID，用于初始化 `NewListen` 对象。
		:return: 无返回值（当前实现未明确返回内容）。
		"""
		# 创建 NewListen 实例，并传入当前进程的 PID
		p = NewListen(pid=self.pid)

		# 调用实例方法获取 TCP 监听端口列表
		p.get_listen_list_tcp()


	def get_eth(self):
		"""
		获取网卡列表并设置默认网卡。

		该函数通过调用 NewNmcli 类的实例方法获取当前连接的网卡列表，
		并根据条件设置默认网卡。如果未设置网卡或网卡未连接，会进行相应的处理。

		:return: 无返回值。
		"""
		# 创建 NewNmcli 实例并获取当前连接的网卡列表
		n = NewNmcli()
		self.eth_list = n.get_dev_list_connected()

		# 如果未设置网卡 (self.eth 为 None)，自动选择列表中的第一个网卡作为默认网卡
		if self.eth is None:
			self.eth = self.eth_list[0]
			print("未设置网卡,自动使用: " + self.eth)

		# 检查当前设置的网卡是否在已连接的网卡列表中，若不在则提示错误并退出程序
		if self.eth not in self.eth_list:
			print("网卡未连接: ", self.eth)
			exit(2)


	# start函数是类中的一个方法，用于初始化或启动某些操作。
	# 该函数没有参数（除了隐式的self）。
	# 返回值：无返回值。
	# 功能概述：
	# 1. 调用get_eth()方法，可能用于获取以太网相关信息。
	# 2. 调用get_status()方法，可能用于获取当前状态信息。
	# 3. 调用get_port()方法，可能用于获取端口相关信息。

	def start(self):
		# 调用get_eth()方法，获取以太网相关信息
		self.get_eth()

		# 调用get_status()方法，获取当前状态信息
		self.get_status()

		# 调用get_port()方法，获取端口相关信息
		self.get_port()


# 主程序入口，用于启动IpRule实例并执行start方法。
# 参数说明：
#   无直接参数，但内部创建了IpRule类的实例，其参数如下：
#   - cmd: 指定规则的命令类型，此处为"sshd"，表示与SSH服务相关的规则。
#   - eth: 指定网络接口编号，此处为0，表示第一个网络接口。
# 返回值：
#   无返回值。

if __name__ == "__main__":
	# 创建IpRule实例，配置cmd为"sshd"，eth为0。
	r = IpRule(cmd="sshd", eth=0)

	# 调用start方法，启动规则处理逻辑。
	r.start()
