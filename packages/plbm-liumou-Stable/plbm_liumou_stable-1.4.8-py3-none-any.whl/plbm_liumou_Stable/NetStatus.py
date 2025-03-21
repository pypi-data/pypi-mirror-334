# -*- encoding: utf-8 -*-
"""
@File    :   NetStatus.py
@Time    :   2022/04/13 11:19:25
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   网络管理
"""
import re
import socket
from os import path, getcwd
from sys import platform

from . import NewFile, NewCommand, get
from .logger import ColorLogger


class NewNetworkCardInfo:
	def __init__(self, eth=None, debug=False):
		"""
		初始化函数，用于获取本地网卡信息并设置相关属性。

		:param eth: str, 可选参数，指定网卡名称。如果未设置，则自动检测网卡。
		:param debug: bool, 可选参数，是否开启调试模式，默认为False。
		:return: None
		"""
		# 初始化DNS地址列表为空
		self.dns = None
		# 设置调试模式标志
		self.debug = debug
		# 设置网卡名称
		self.eth = eth
		# 获取当前操作系统名称并转换为小写
		self.os = platform.lower()
		# 标记是否为Linux系统
		self.linux = False
		if self.os.lower() == 'linux'.lower():
			self.linux = True

		# 初始化网关地址
		self.gw = None
		# 初始化IP地址
		self.ip = None
		# 初始化子网信息
		self.sub = None
		# 初始化MAC地址
		self.mac = None
		# 初始化子网掩码，默认值为24
		self.mask = 24
		# 初始化连接名称
		self.connect = None
		# 初始化连接速率
		self.rate = None

		# 初始化命令工具类实例，用于执行系统命令
		self.cmd = NewCommand(password="pd")
		# 初始化日志工具类实例，用于记录日志
		self.logger = ColorLogger()


	def show(self):
		"""
		显示网卡信息。

		该函数通过日志记录的方式输出当前网卡的详细信息，包括网卡名称、网关、IP地址、子网掩码、DNS列表、MAC地址、连接速率以及连接名称。

		:param self: 当前对象实例，包含以下属性：
		             - eth: 网卡名称
		             - gw: 网关地址
		             - ip: IP地址
		             - mask: 子网掩码
		             - dns: DNS服务器列表
		             - mac: MAC地址
		             - rate: 连接速率
		             - connect: 连接名称
		:return: 无返回值。
		"""
		# 记录网卡名称
		self.logger.info("Eth_self.eth :", self.eth)
		# 记录网关地址
		self.logger.info("Gateway_self.gw : ", self.gw)
		# 记录IP地址
		self.logger.info("IP_self.ip: ", self.ip)
		# 记录子网掩码
		self.logger.info("Subnet Mask_self.mask : ", self.mask)
		# 记录DNS服务器列表
		self.logger.info("Dns List_self.dns: ", str(self.dns))
		# 记录MAC地址
		self.logger.info("Mac _self.mac : ", self.mac)
		# 记录连接速率
		self.logger.info("Connect Rate_self.rate: ", self.rate)
		# 记录连接名称
		self.logger.info("Connect Name_self.connect: ", self.connect)


	def get_dev_list(self):
		"""
		获取网卡列表并检测网卡信息。

		该函数通过执行系统命令获取当前设备的网卡列表，并检查是否包含预设的网卡名称。
		如果预设网卡名称存在，则记录日志并返回 True；否则，记录警告日志并尝试自动检测。

		:return:
			- True: 如果预设的网卡名称存在于网卡列表中。
			- False: 如果预设的网卡名称不存在或需要使用自动检测。
		"""
		# 定义命令及其参数，避免直接拼接字符串以防止命令注入
		command = ["nmcli", "device"]
		try:
			# 执行命令并提取网卡设备名称列表
			raw_output = self.cmd.getout(cmd=command)
			device_list = [line.split()[0].strip() for line in raw_output.split("\n") if line.strip()]
		except Exception as e:
			# 捕获命令执行异常并记录错误日志
			self.logger.error(f"Failed to execute command 'nmcli device': {e}")
			return False

		# 检查是否设置了预设网卡名称 (self.eth)，并判断其是否在网卡列表中
		if self.eth is not None:
			if str(self.eth) in device_list:
				# 如果预设网卡名称存在，记录信息日志并返回 True
				self.logger.info(f"The set device name '{self.eth}' is in the existing list")
				return True
			else:
				# 如果预设网卡名称不存在，记录警告日志并提示将使用自动检测
				self.logger.warning(f"Device not found: {self.eth}")
				self.logger.debug("Automatic detection will be used")

		# 调用自动检测方法获取 IP 请求
		self.getip_request()
		return False



	def get_all(self):
		"""
		获取所有网卡信息
		:return: 获取结果(bool)
		"""
		existence = self.get_dev_list()
		if self.linux:
			if not existence:
				# 使用自动检测网卡信息
				self.logger.debug("Use automatic network card detection")
				try:
					# 防止命令注入，使用参数化方式构建命令
					dev_cmd = "ip r | grep default | grep {} | awk '{{print $5}}'".format(self.sub)
					self.eth = self.cmd.getout(cmd=dev_cmd)
				except Exception as e:
					self.logger.error(f"Automatic network card detection failed: {e}")
					return False
			else:
				# 检测指定网卡信息
				self.logger.debug("Detect the specified network card information")
				if not self.getip_dev():
					self.logger.error("Query failed for specified network card")
					return False
		else:
			self.logger.error("Current device is not Linux")
			return False

		try:
			# 获取连接参数
			connect_arg_cmd = "nmcli device show {} | grep IP4".format(self.eth)
			connect_arg = self.cmd.getout(connect_arg_cmd).split("\n")

			# 边界条件检查
			if len(connect_arg) < 2:
				self.logger.error("Insufficient connection arguments from nmcli output")
				return False

			# 子网掩码
			mask_part = str(connect_arg[0]).split("/")
			if len(mask_part) < 2:
				self.logger.error("Invalid subnet mask format in nmcli output")
				return False
			self.mask = int(mask_part[1])

			# 网关
			self.gw = connect_arg[1]

			# 设备信息
			search_cmd = "nmcli device show {} | grep GENERAL | awk '{{print $2}}'".format(self.eth)
			search_info = self.cmd.getout(search_cmd).split("\n")

			# 边界条件检查
			if len(search_info) < 6:
				self.logger.error("Insufficient device information from nmcli output")
				return False

			# Mac地址、连接速率、连接名称
			self.mac = search_info[2]
			self.rate = search_info[4]
			self.connect = search_info[5]

			# Dns列表
			dns_cmd = "nmcli device show {} | grep IP4 | grep DNS | awk '{{print $2}}'".format(self.eth)
			self.dns = str(self.cmd.shell(cmd=dns_cmd)).split('\n')

			# 显示信息
			self.show()
			return True

		except Exception as e:
			self.logger.error(f"Error occurred while processing network card information: {e}")
			return False



	def getip_dev(self):
		"""
		使用指定设备的方式获取IP
		:return: 成功返回 True，失败返回 False
		"""
		try:
			# 构造命令，使用 subprocess 参数化方式避免命令注入
			command = ["nmcli", "device", "show", self.eth]
			output = self.cmd.getout(command)  # 假设 self.cmd.getout 支持传入列表
			if self.cmd.code != 0:
				# 记录详细的错误信息
				self.logger.error(f"Query failed. Command exited with code {self.cmd.code}. Output: {output}")
				return False

			# 使用正则表达式提取 IP 地址和子网掩码
			ip_pattern = re.compile(r"^IP4\.ADDRESS\[?\d*]?\s*:\s*([\d.]+)/(\d+)", re.MULTILINE)
			match = ip_pattern.search(output)
			if not match:
				self.logger.error("No valid IP address found in the command output.")
				return False

			# 提取 IP 和子网掩码
			self.ip, self.mask = match.groups()
			self.logger.debug("query was successful")
			return True

		except Exception as e:
			# 捕获所有异常并记录详细信息
			self.logger.error(f"An unexpected error occurred: {e}")
			return False


	def getip_request(self):
		"""
		使用网络请求的方式获取IP
		:return:
		"""
		try:
			csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			csock.connect(('119.29.29.29', 53))
			(addr, port) = csock.getsockname()
			csock.close()
			self.ip = addr
			tu = str(self.ip).split('.')
			self.sub = str("%s.%s.%s." % (tu[0], tu[1], tu[2]))
			return True
		except Exception as e:
			self.logger.error(str(e))
			return False


class NewNetStatus:
	def __init__(self, ip=None, port=80, log_file=None, txt_log=False, debug=True):
		"""
		网络工具，用于判断网络是否正常
		:param ip: 需要判断的IP
		:param port:  需要判断的端口. Defaults to None.
		:param log_file: 日志文件
		:param txt_log: 是否开启文本日志
		"""
		self.debug = debug
		self.ip = ip
		self.port = port
		self.status = False
		#
		self.headers = {}
		self.headers = get.headers
		self.cmd = NewCommand(password='Gxxc@123')
		self.fm = NewFile()
		self.logger = ColorLogger(file=log_file, txt=txt_log)

	def ping_status(self, server=None):
		"""
		使用ping检测网络连接
		:param server: 设置服务器地址. Defaults to self.ip.
		:return:
		"""
		self.status = False
		if server is None:
			server = self.ip
		self.logger.info('正在检测： %s' % server)
		cmd = 'ping %s -c 5' % server
		if platform.lower() == 'win32':
			cmd = 'ping %s ' % server
		if self.cmd.shell(cmd=cmd):
			self.logger.info("Ping 连接成功: %s" % server)
			self.status = True
		else:
			self.logger.error("Ping 连接失败: %s" % server)
		return self.status

	def downfile(self, url, filename=None, cover=False, md5=None):
		"""
		下载文件
		:param url: 下载链接
		:param filename: 保存文件名,默认当前目录下以URL最后一组作为文件名保存
		:param cover: 是否覆盖已有文件. Defaults to False.
		:param md5: 检查下载文件MD5值
		:return: 下载结果(bool)
		"""
		if filename is None:
			filename = str(url).split("/")[-1]
			filename = path.join(getcwd(), filename)
		filename = path.abspath(filename)
		if path.exists(filename):
			if not cover:
				self.logger.info("检测到已存在路径: %s" % filename)
				self.logger.info("放弃下载： %s" % url)
				return True
			self.logger.debug("检测到已存在路径,正在删除...")
			c = 'rm -rf ' + filename
			if self.cmd.shell(cmd=c):
				self.logger.info("删除成功: %s" % filename)
			else:
				self.logger.warning("删除失败,跳过下载")
				return False
		c = str("wget -c -O %s %s" % (filename, url))
		self.cmd.shell(cmd=c, terminal=False)
		if int(self.cmd.code) == 0:
			self.logger.info("下载成功: %s" % filename)
			if md5:
				get_ = self.fm.get_md5(filename=filename)
				if get_:
					if str(md5).lower() == str(self.fm.md5).lower():
						return True
				else:
					return False
			return True
		self.logger.error("下载失败: %s" % filename)
		self.logger.error("下载链接: ", url)
		self.logger.error("保存路径: ", filename)
		return False

	def tcp_port_status(self, port, timeout=5, ip=None):
		"""
		检测TCP端口是否开放
		:param ip: 
		:param port: 
		:param timeout: 
		:return: 
		"""
		if ip is None:
			if self.ip is None:
				self.logger.error("未设置对端IP地址")
			else:
				self.logger.debug("使用实例配置IP进行检测")
				ip = self.ip
		else:
			self.logger.debug("使用函数传入IP")
		self.logger.info("正在检测地址: [", ip, "] - 端口: [ ", port, " ]")
		
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(timeout)
		try:
			sock.connect((self.ip, port))
			return True
		except socket.error:
			return False


if __name__ == "__main__":
	up = NewNetStatus()
	up.ping_status(server='baidu.com')
