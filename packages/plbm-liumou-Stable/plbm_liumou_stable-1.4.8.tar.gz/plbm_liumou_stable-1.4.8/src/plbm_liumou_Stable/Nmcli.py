# -*- encoding: utf-8 -*-
"""
@File    :   Nmcli.py
@Time    :   2022/04/17 01:06:40
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   网络管理模块
"""
import ipaddress
import re
import shlex
import socket
import subprocess
from typing import Optional

from .Cmd import NewCommand
from .base import list_get_len
from .logger import ColorLogger


class NewNmcli(object):
	def __init__(self, password=None, ip=None, gw=None, mask=24, dns1=None, dns2=None, net=None, dev=None, log=True):
		"""
		基于nmcli命令实现的网络管理模块,参数均为可选传参，请根据实际需求传入
		:param password: (str, optional): 设置主机密码. Defaults to None.
		:param ip: (str, optional): 设置IP地址. Defaults to "192.168.1.138".
		:param gw: (str, optional): 设置网关. Defaults to "192.168.1.1".
		:param mask: (int, optional): 设置子网掩码. Defaults to 24.
		:param dns1: (str, optional): 设置DNS1. Defaults to "114.114.114.114".
		:param dns2: (str, optional): 设置DNS2. Defaults to "119.29.29.29".
		:param net: (str, optional): 设置网段,一般是自动尝试配置IP需要. Defaults to '192.168.1.'.
		:param dev: (str, optional): 设置网卡名称. Defaults to 'ens33'.
		:param log: (bool, optional): 是否启用日志功能
		"""
		self.deviceConnectedList = None  # 获取已连接的设备列表
		self.DefaultDnsList = None  # 默认网卡DNS地址列表
		self.DefaultMask = None  # 默认掩码
		self.DefaultIp4 = None  # 默认IP地址
		self.DefaultGw = None  # 默认网关地址
		# 以下为设置默认值
		if ip is None:
			ip = "192.168.1.138"
		if gw is None:
			gw = "192.168.1.1"
		if dns1 is None:
			dns1 = "223.5.5.5"
		if dns2 is None:
			dns2 = "119.29.29.29"
		if net is None:
			net = "192.168.1."
		if dev is None:
			dev = 'ens33'
		self.log = log
		# 主机密码
		self.password = password
		# 网段
		self.net = net
		# 子网地址
		self.subnet = None
		# IP地址
		self.ipv4 = ip
		# 网关
		self.gateway = gw
		# DNS1
		self.dns1 = dns1
		# DNS2
		self.dns2 = dns2
		# 子网掩码
		self.netmask = mask
		# 连接名称
		self.connect_name = 'Y'
		# 连接模式
		self.connect_mode = 'auto'
		# DNS列表
		self.dns_list = []
		# 网卡设备
		self.device = dev
		self.DefaultDev = None  # 默认网卡设备名称
		self.deviceList = []  # 网卡列表
		# 初始化日志记录器
		self.logger = ColorLogger()
		# 初始化命令执行器
		self.cmd = NewCommand(password=password)
		self.debug = False
		self.Err = None
		# 获取默认网络配置
		self.get_default()

	def get_default(self):
		"""
		获取默认网卡信息

		该方法通过调用子方法来获取系统的默认网卡信息，包括IPv4地址和默认网关
		"""
		# 获取默认的IPv4地址信息
		self._get_default_ipv4_socket()
		# 获取默认网关信息
		self._get_default_gateway()

	def _get_default_gateway(self):
		"""
		获取系统的默认网关

		该方法通过执行shell命令来获取当前系统的默认网关地址，并将其保存在self.DefaultGw中
		如果获取失败，会记录错误信息，并设置self.DefaultGw为None
		"""
		# 执行shell命令获取默认网关信息
		output = subprocess.check_output('ip route show default', shell=True)

		# 使用正则表达式解析命令输出，提取默认网关IP和设备名
		match = re.search(r'default via (\d+\.\d+\.\d+\.\d+) dev (\w+)', output.decode())

		if match:
			# 如果成功匹配到默认网关信息，更新self.DefaultGw，并记录日志
			self.logger.info("默认网关获取成功")
			self.DefaultGw = match.group(1)
		else:
			# 如果匹配失败，记录错误日志，设置self.DefaultGw为None，并设置错误信息
			self.logger.error("默认网关获取失败")
			self.DefaultGw = None
			self.Err = "无法获取默认网关"

	def _get_default_ipv4_socket(self):
		"""
		通过socket获取本机IP，并通过DefaultIp4属性存储实际值
		:return: bool 获取IP成功返回True，否则返回False
		"""
		try:
			# 获取主机名
			hostname = socket.gethostname()
			# 通过主机名获取主机IP地址，并将其赋值给DefaultIp4属性
			self.DefaultIp4 = socket.gethostbyname(hostname)
			return True
		except Exception as e:
			# 日志记录错误信息
			self.logger.error(str(e))
			# 将错误信息存储在Err属性中
			self.Err = str(e)
		return False

	def connect_create(self, name="Y", mode='auto'):
		"""
		创建连接
		:param name: (str, optional): 连接名称. Defaults to "Y".
		:param mode: (str, optional): 连接模式. Defaults to "auto".
		:return: bool
		"""
		# 初始化错误信息
		self.Err = None
		# 构建创建连接的命令并执行
		c = str("""nmcli connection add type ethernet  con-name {0} ifname {1}""".format(name, self.device))
		get = self.cmd.shell(cmd=c)
		# 根据执行结果提供日志输出或错误处理
		if get:
			self.logger.info("连接创建成功")
		else:
			print(c)
			self.Err = "连接创建失败"
			self.logger.error(self.Err)
			return False
		# 根据所选模式配置IP获取方式
		if mode != "auto":
			self.logger.debug("使用静态IP配置")
			c = str("""nmcli connection modify {0} ipv4.method manual ipv4.addresses {1}""".format(name, self.ipv4))
		else:
			self.logger.debug("使用自动获取IP")
			c = str("""nmcli connection modify {0} ipv4.method auto""".format(name))
		# 执行IP获取模式配置命令
		return self.run(c=c, n_="IP获取模式配置")

	def run(self, c, n_):
		"""
		执行给定的命令并记录结果。

		该方法主要用于执行命令并根据执行结果记录日志。执行成功会记录成功信息，
		失败则记录错误信息，并返回执行结果的布尔表示。

		参数:
		:param c: 需要执行的命令字符串。
		:param n_: 命令的名称，用于在日志中标识命令。

		返回值:
		:return: bool - 如果命令执行成功，返回True；否则返回False。
		"""
		# 执行命令
		get = self.cmd.shell(cmd=c)

		# 判断命令执行结果并记录日志
		if get:
			self.logger.info("[ %s ]成功" % n_)
			return True
		else:
			# 打印命令以便调试
			print(c)
			# 记录错误信息
			self.Err = "[ %s ]失败" % n_
			self.logger.warning(self.Err)

		return False

	def get_con_uuid(self, name):
		"""
		通过名称或者关键词获取一个连接的UUID
		:param name: 连接的名称或关键词
		:return: UUID字符串或False
		"""
		# 构建命令以筛选出包含特定名称或关键词的连接
		c = str("""nmcli connection  | grep "%s" """ % name)
		# 执行命令并获取输出
		get = self.cmd.getout(c)
		# 检查命令执行是否成功
		if self.cmd.code == 0:
			# 分割输出以获取各个连接的信息
			sp = str(get).split(" ")
			# 过滤出元素长度大于10的元素，因为UUID的长度通常较长
			sp = list_get_len(sp, 10)
			# 如果只有一个元素满足条件，则返回该UUID
			if len(sp) == 1:
				return sp[0]
			# 如果有多个元素满足条件，则进一步检查每个元素
			if len(sp) > 1:
				for i in sp:
					# 分割元素以检查是否符合UUID的格式
					ts = str(i).split("-")
					# 当找到符合UUID格式的元素时，返回该UUID
					if len(ts) == 5:
						return i
		# 如果没有找到符合条件的UUID，返回False
		return False

	def con_delete(self, con):
		"""
		删除网络连接。

		此函数通过名称、名称关键词或UUID来删除指定的网络连接。如果提供的连接参数为空，则使用实例的connect_name属性作为默认值。

		参数:
		:param con: 需要删除的连接的名称、名称关键词或UUID。
		返回值:
		:return: bool - 如果删除成功返回True，否则返回False。
		"""
		# 如果未提供连接名称，则使用实例的默认连接名称
		if con is None:
			con = self.connect_name

		# 获取连接的UUID
		cl = self.get_con_uuid(name=con)

		# 如果成功获取到连接的UUID，则执行删除操作
		if cl:
			# 构建并执行删除连接的命令
			c = str("""nmcli connection  delete %s""" % cl)
			self.cmd.shell(c)

			# 检查命令执行结果，如果执行失败，则记录错误日志并返回False
			if self.cmd.code != 0:
				self.logger.error("删除失败")
				return False
		else:
			# 如果无法获取到连接的UUID，则记录警告日志
			self.logger.warning("无法获取连接")

		# 默认返回True，表示操作成功或未执行删除操作（因为未找到连接）
		return True


	def get_dev_list(self):
		"""
		获取设备列表。

		该函数通过执行系统命令获取当前活动的网络设备列表，并将结果存储在 self.deviceList 中。
		如果命令执行成功且获取到至少一个设备，则返回 True；否则返回 False。

		:return: bool
			- True：成功获取设备列表，设备信息可通过 self.deviceList 获取。
			- False：未能成功获取设备列表，self.deviceList 可能为空或未更新。
		"""
		try:
			# 使用参数化方式构造命令，避免命令注入风险
			command = [
				"ip", "link", "show", "up"
			]

			# 执行命令并获取输出
			result = subprocess.run(command, capture_output=True, text=True, check=True)
			output = result.stdout

			# 使用 Python 替代 grep/sed/awk 处理输出
			lines = output.splitlines()
			self.deviceList = [
				line.split()[1].strip(":") for line in lines
				if "<" in line and not line.startswith("docker") and not line.startswith("lo")
			]

			# 如果设备列表中至少有一个设备，记录日志并返回 True
			if self.deviceList:
				self.logger.info("网卡信息获取成功")
				return True

			# 如果未获取到设备，记录错误日志
			self.logger.error("无法获取网卡设备信息：未找到有效设备")
			return False

		except subprocess.CalledProcessError as e:
			# 捕获命令执行失败的异常，记录详细错误信息
			self.logger.error(f"命令执行失败：{e}")
			return False
		except Exception as e:
			# 捕获其他异常，记录详细错误信息
			self.logger.error(f"发生未知错误：{e}")
			return False




	def get_dev_list_connected(self):
		"""
		获取已连接的设备列表
		:return: bool (数据请通过 self.deviceConnectedList 获取)
		"""
		try:
			# 执行命令并获取输出
			output = self.cmd.getout("nmcli device status")

			# 检查命令执行状态码
			if self.cmd.code != 0:
				self.logger.error(f"命令执行失败，状态码: {self.cmd.code}, 命令: nmcli device status")
				return False

			# 确保输出为字符串类型
			if not isinstance(output, str):
				self.logger.error(f"命令返回值类型错误，期望 str，实际为 {type(output)}")
				return False

			# 使用正则表达式处理输出
			lines = output.strip().split("\n")
			pattern = re.compile(r'^(\S+)\s+ethernet\s+(?!.*--).*$')
			self.deviceConnectedList = [pattern.match(line).group(1) for line in lines if pattern.match(line)]

			# 检查设备列表是否为空
			if not self.deviceConnectedList:
				self.logger.warning("未检测到任何已连接的网卡设备")
				return False

			# 日志记录成功信息
			self.logger.info("网卡信息获取成功")
			return True

		except Exception as e:
			# 捕获异常并记录详细错误信息
			self.logger.error(f"获取网卡设备信息时发生异常: {e}")
			return False




	def _getIp(self, lr: list):
		"""
		从列表数据中获取IPV4地址
		:param lr: 需要获取的字符串
		:return: 返回IP地址或者False
		"""
		# 边界条件检查：如果输入为空列表，直接返回 False
		if not lr:
			self.logger.warning("输入列表为空，无法获取IP地址")
			return False

		# 遍历列表，尝试解析每个元素为 IPv4 地址
		for i in lr:
			try:
				ip = ipaddress.IPv4Address(i)
				return ip  # 找到有效 IP 地址后立即返回
			except (ipaddress.AddressValueError, ValueError):
				continue  # 捕获特定异常，忽略无效数据

		# 如果遍历结束仍未找到有效 IP 地址，记录详细日志并返回 False
		self.logger.warning(f"无法从输入列表中获取IP地址，输入数据前5项: {lr[:5]}")
		return False


	def get_eth_dns_list(self, eth):
		"""
		获取指定网卡设备的DNS地址列表。

		:param eth: str，指定的网卡设备名称，用于查询其DNS配置。
		:return: list，包含该网卡设备的DNS地址列表；如果无法获取DNS信息，则返回False。
		"""
		# 构造命令以通过nmcli工具获取指定网卡的IPv4 DNS信息
		c = str("""nmcli device show %s | grep DNS | grep IP4| awk '{print $2}'""" % eth)
		# 执行命令并获取输出结果
		get = self.cmd.getout(cmd=c)
		if self.cmd.code == 0:
			# 如果命令执行成功，打印输出结果并按行分割
			print(get)
			sp = str(get).split("\n")
			# 如果分割后的列表长度大于等于1，返回DNS地址列表
			if len(sp) >= 1:
				return sp
		# 如果命令执行失败，打印命令内容并记录警告日志
		print(c)
		self.logger.warning("无法获取网卡的DNS信息: %s" % eth)
		return False


	def get_default_dev(self):
		"""
		获取默认网卡设备信息，并将获取到的信息存储在实例变量中（以Default开头的变量）。
		包括以下信息：
		- DefaultDev: 默认网卡名称
		- DefaultGw: 默认网关
		- DefaultDnsList: 默认网卡的DNS列表
		- DefaultMask: 默认网卡的子网掩码

		:return: bool
			返回值固定为False，可能用于表示函数执行完成或未实现完整逻辑。
		"""
		# 获取默认网卡名称（通过解析命令输出）
		self.DefaultDev = self.cmd.getout("ip r | grep default | sed -n 1p | awk '{print $5}'")

		# 获取默认网关地址
		self.DefaultGw = self.cmd.getout("ip r | grep default | sed -n 1p | awk '{print $3}'")

		# 获取默认网卡的DNS列表
		self.DefaultDnsList = self.get_eth_dns_list(self.DefaultDev)

		# 构造命令以获取默认网卡的IP地址和子网掩码信息
		c = str("""ip addr show %s  | grep inet | sed -n 1p | awk '{print $2}'""" % self.DefaultDev)
		get = self.cmd.getout(c)

		# 如果命令执行成功，解析子网掩码并存储到DefaultMask变量中
		if self.cmd.code == 0:
			self.DefaultMask = str(get).split("/")[-1]

		# 返回固定值False
		return False



	def get_con_uuid_all(self):
		"""
		获取所有可用的连接UUID列表,返回数据格式: ['7dc597e8-23ad-4360-8dc3-87058a2d08aa', 'b3a484ff-73a6-4e0e-8c1a-0e829b36a848']
		:return: bool/list
		"""
		# 执行命令获取所有活动连接的信息
		command = "nmcli con show --active"
		output = self.cmd.getout(command)

		# 检查命令执行是否成功
		if self.cmd.code != 0:
			return False

		# 使用正则表达式提取 UUID 列表
		try:
			# 定义正则表达式，匹配非 loopback、非 NAME、非 docker0 的行，并提取第二列（UUID）
			pattern = re.compile(r"^(?!.*loopback)(?!.*NAME)(?!.*docker0)\s+\S+\s+(\S+)", re.MULTILINE)
			matches = pattern.findall(output)

			# 过滤掉空字符串并返回结果
			uuid_list = [match.strip() for match in matches if match.strip()]
			return uuid_list if uuid_list else False
		except Exception as e:
			# 捕获异常并记录错误日志
			self.logger.error(f"正则表达式匹配失败: {e}")
			return False


	def get_con_list_eth_uuid(self, eth):
		"""
		获取指定网卡的连接配置的UUID列表,返回数据格式: ['7dc597e8-23ad-4360-8dc3-87058a2d08aa', 'b3a484ff-73a6-4e0e-8c1a-0e829b36a848']
		:param eth: 网卡名称
		:return: list
		"""
		try:
			# 使用参数化命令避免命令注入风险
			command = "nmcli connection show | grep {} | awk '{{print $2}}'".format(shlex.quote(eth))
			get = self.cmd.getout(command)

			# 检查命令执行是否成功
			if self.cmd.code == 0:
				# 处理返回值，确保分割后是有效的列表
				result = str(get).strip().split("\n")
				return [item for item in result if item]  # 过滤掉空字符串
			else:
				return []  # 命令执行失败时返回空列表
		except Exception as e:
			# 捕获异常并返回空列表
			print(f"Error occurred while executing command: {e}")
			return []

	def get_eth_info(self, eth):
		"""
		获取指定网卡的网络配置信息, 包含: IP4、网关、掩码、DNS
		:param eth: 需要获取的网卡名称
		:return: dict
		"""
		info = {}

		# 定义命令模板
		COMMAND_IP_MASK = "nmcli device show {} | grep ADDRESS | sed -n 1p | awk '{{print $2}}'"
		COMMAND_GATEWAY = "nmcli device show {} | grep IP4.GATE | awk '{{print $2}}'"

		try:
			# 检查网卡是否存在
			if not self._check_device_exists(eth):
				self.logger.error(f"网卡 {eth} 不存在")
				return {}

			# 获取 IP 和掩码
			ip_mask_command = COMMAND_IP_MASK.format(eth)
			ip_mask_result = self.cmd.shell(ip_mask_command)
			if self.cmd.code == 0:
				ip_mask = str(ip_mask_result).split("/")
				if len(ip_mask) == 2:
					info["mask"] = ip_mask[1]
					info["ip"] = ip_mask[0]
					self.ipv4 = ip_mask[0]
					self.netmask = int(ip_mask[1])
				else:
					self.logger.warning(f"IP和掩码格式错误，网卡: {eth}")
			else:
				self.logger.error(f"获取IP和掩码失败，命令: {ip_mask_command}, 错误码: {self.cmd.code}")

			# 获取网关
			gateway_command = COMMAND_GATEWAY.format(eth)
			gateway_result = self.cmd.shell(gateway_command)
			if self.cmd.code == 0:
				info["gw"] = gateway_result.strip()
				self.gateway = gateway_result.strip()
			else:
				self.logger.error(f"获取网关失败，命令: {gateway_command}, 错误码: {self.cmd.code}")
				info["gw"] = None
				self.gateway = None

			# 获取 DNS
			dns = self.get_eth_dns_list(eth=eth)
			if dns:
				info["dns"] = dns
			else:
				self.logger.warning(f"DNS获取失败，网卡: {eth}")
				info["dns"] = []

			# 获取子网
			if self.get_dev_subnet(eth=eth):
				info["subnet"] = self.subnet

		except PermissionError as e:
			self.logger.error(f"权限不足，无法执行命令: {e}")
		except TimeoutError as e:
			self.logger.error(f"命令执行超时: {e}")
		except Exception as e:
			self.logger.error(f"获取网卡信息时发生未知异常: {e}")

		return info

	def _check_device_exists(self, eth):
		"""
		检查指定网卡是否存在
		:param eth: 网卡名称
		:return: bool
		"""
		try:
			command = f"nmcli device show {eth}"
			result = self.cmd.shell(command)
			if self.cmd.code != 0:
				self.logger.warning(f"网卡 {eth} 不存在或无法访问")
				return False
			return True
		except Exception as e:
			self.logger.error(f"检查网卡存在性时发生异常: {e}")
			return False


	def get_dev_subnet(self, eth):
		"""
		获取指定设备的子网信息
		:param eth:
		:return:
		"""
		c = f"nmcli device show {eth} | grep IP4.ROUTE"
		get = self.cmd.getout(cmd=c)
		if self.cmd.code == 0:
			match = re.search(r'IP4.ROUTE[ \t]*:\s*(\S+)', get)
			if match:
				txt = match.group(1).split(",")[0].strip()
				if len(txt.split(".")) >= 3:
					self.subnet = txt
					return True
		return False


	def get_con_dns(self, con):
		"""
		获取指定连接的DNS信息
		:param con: 需要获取的连接名称或者uuid
		:return:list
		"""
		# 使用nmcli原生字段输出功能
		c = ["nmcli", "-g", "IP4.DNS", "con", "show", shlex.quote(str(con))]
		get = self.cmd.getout(c)

		if self.debug:
			self.logger.debug(f"执行命令: {' '.join(c)}")

		if self.cmd.code == 0:
			# 使用正则表达式提取有效IP
			dns_entries = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d+)?', get)
			if dns_entries:
				return dns_entries

		self.logger.warning("无法获取连接的DNS信息")
		return [None]



	def get_con_gw(self, con: str) -> Optional[str]:
		"""
		获取连接的网关信息
		:param con: 需要获取的连接名称或者uuid
		:return: 网关IP地址或None
		"""
		try:
			# 安全构造命令参数
			cmd = ["nmcli", "con", "show", shlex.quote(con)]
			# 执行命令并获取输出
			output = self.cmd.getout(" ".join(cmd))  # 假设必须通过shell执行

			if self.debug:
				self.logger.debug(f"Command output: {output}")

			if self.cmd.code != 0:
				self.logger.warning(f"网关获取失败 (返回码: {self.cmd.code})")
				return None

			# 使用Python原生处理替代grep+awk
			for line in output.split('\n'):
				if "IP4.GATE" in line:
					return line.split()[-2]  # 直接取倒数第二列

			self.logger.warning("未找到IP4.GATE字段")
			return None
		except Exception as e:
			self.logger.error(f"获取网关时发生异常: {str(e)}")
			return None


	def get_con_ip(self, con):
		"""
		获取连接的IP地址
		:param con: 需要获取的连接名称或者uuid
		:return: 包含IP和掩码的字典，失败返回None
		"""
		# 安全执行命令获取IP4.ADDRESS字段
		cmd = ["nmcli", "-g", "ip4.address", "con", "show", con]
		if self.debug:
			self.logger.debug(f"执行命令: {' '.join(cmd)}")

		get_output = self.cmd.getout(cmd)

		# 处理命令执行失败
		if self.cmd.code != 0:
			self.logger.warning(f"获取连接信息失败 [code:{self.cmd.code}]")
			return None

		# 解析输出结果
		output = str(get_output).strip()
		if not output:
			if self.debug:
				self.logger.debug("连接未分配IP地址")
			return {"ip": None, "mask": 0}

		# 拆分IP/CIDR格式
		try:
			ip_str, cidr_str = output.split("/", 1)
			return {
				"ip": ip_str,
				"mask": int(cidr_str)
			}
		except (ValueError, TypeError) as e:
			self.logger.error(f"IP信息解析失败: {output} ({str(e)})")
			return {"ip": None, "mask": 0}


	def get_con_info(self, con):
		"""
		获取指定连接的网络配置信息,通过status判断获取结构, 格式: {'ip': '10.1.1.18', 'mask': 24, 'gw': '10.1.1.1', 'dns': ['10.1.1.1'], 'status': True}
		:param con: 连接名称或UUID
		:return: dict
		"""
		# 预初始化数据结构
		info = {
			'ip': None,
			'mask': None,
			'gw': None,
			'dns': [],
			'status': False
		}

		try:
			c = self.get_con_uuid(name=con)
			if not c:
				self.logger.error("无法获取连接信息,请检查配置参数")
				return info

			# 统一处理各配置项
			config_items = [
				('ip', self.get_con_ip),
				('gw', self.get_con_gw),
				('dns', self.get_con_dns)
			]

			for key, method in config_items:
				result = method(con=con)
				if key == 'ip':
					if isinstance(result, dict):
						info.update(result)
					else:
						raise ValueError("Invalid IP config structure")
				else:
					if result:  # 过滤空值
						info[key] = result

				if self.debug:
					self.logger.debug(f"{key.upper()} config: {str(result)}")

			# 最终状态检查：要求至少包含ip和mask
			info['status'] = bool(info['ip'] and info['mask'] is not None)

		except Exception as e:
			self.logger.error(f"获取连接信息时发生异常: {str(e)}")
			info['status'] = False

		return info


# 主程序入口: 当脚本作为独立程序运行时执行以下代码块
if __name__ == "__main__":
	# 创建NewNmcli实例
	# NewNmcli类用于封装网络管理命令行工具nmcli的操作
	n = NewNmcli()

	# 调用实例方法获取默认网络设备信息
	# get_default_dev方法用于查询系统当前的默认网络接口设备
	# 返回值: 预期返回字符串格式的设备名称（具体实现需参考类定义）
	n.get_default_dev()
