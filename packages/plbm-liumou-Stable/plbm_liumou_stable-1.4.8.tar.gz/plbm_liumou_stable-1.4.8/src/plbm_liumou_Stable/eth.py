import psutil


class NewEthTools:
	def __init__(self):
		"""
		初始化类的实例，设置以太网连接、IPv4和IPv6相关属性以及需要特殊处理的网络接口名称前缀。

		参数:
			无

		返回值:
			无
		"""

		# 初始化以太网连接的列表和字典，用于存储以太网连接的相关信息
		self.eth_connected_list = []
		self.eth_connected_dict = {}

		# 初始化IPv4相关属性，包括是否启用IPv4标志和IPv4地址列表
		self._ipv4 = False
		self._ipv4_list = []

		# 初始化IPv6相关属性，包括是否启用IPv6标志和IPv6地址列表
		self._ipv6 = False
		self._ipv6_list = []

		# 定义需要特殊处理的网络接口名称前缀，用于过滤或特殊处理特定的网络接口
		self.force_name = ["lo", "docker0", "veth", "virbr", "vmnet", "wlan"]


	def get_connected_eth_list4(self):
		"""
		获取已连接IPV4的网卡列表。

		该函数通过设置内部标志 `_ipv4` 为 True，调用 `get_connected_eth_list` 方法，
		并将结果存储在 `_ipv4_list` 中，最终将 `_ipv4_list` 赋值给 `eth_connected_list`。

		:return: 无返回值。结果存储在实例变量 `eth_connected_list` 中。
		"""
		# 设置内部标志，表示当前操作针对 IPV4
		self._ipv4 = True

		# 初始化存储 IPV4 网卡列表的变量
		self._ipv4_list = []

		# 调用通用方法获取已连接的网卡列表（针对 IPV4）
		self.get_connected_eth_list()

		# 将获取的 IPV4 网卡列表赋值给实例变量 eth_connected_list
		self.eth_connected_list = self._ipv4_list


	def get_connected_eth_list6(self):
		"""
		获取已连接IPV6的网卡列表。

		该函数通过设置内部标志 `_ipv6` 为 True，调用 `get_connected_eth_list` 方法，
		并将结果存储在 `_ipv6_list` 中，最终将 `_ipv6_list` 赋值给 `eth_connected_list`。

		:return: None
		"""
		# 设置内部标志，表示当前操作针对 IPV6
		self._ipv6 = True

		# 初始化用于存储 IPV6 网卡列表的变量
		self._ipv6_list = []

		# 调用通用方法获取已连接的网卡列表（此时会根据 _ipv6 标志筛选 IPV6 网卡）
		self.get_connected_eth_list()

		# 将筛选后的 IPV6 网卡列表赋值给 eth_connected_list
		self.eth_connected_list = self._ipv6_list

		# 重置内部标志，恢复为默认状态（非 IPV6）
		self._ipv6 = False


	def get_connected_eth_list(self):
		"""
		获取已连接的网卡及配置信息。

		该函数通过 `psutil.net_if_addrs()` 获取所有网络接口的信息，筛选出已连接的网卡，
		并根据 IPv4 和 IPv6 的支持情况将网卡信息分类存储。

		:return: bool
			- True: 成功获取已连接的网卡信息。
			- False: 获取过程中发生异常或未找到符合条件的网卡。
		"""
		self.eth_connected_list = []  # 存储已连接的网卡名称列表
		self.eth_connected_dict = {}  # 存储网卡名称及其对应的 IP 地址列表

		try:
			# 获取所有网络接口及其地址信息
			net = psutil.net_if_addrs()

			# 遍历每个网络接口，检查其连接状态和地址类型
			for interface in net:
				ipv4 = False  # 标记是否支持 IPv4
				ipv6 = False  # 标记是否支持 IPv6
				connect = False  # 标记是否为已连接的网卡

				# 检查第一个地址的协议族，判断是否支持 IPv4 或 IPv6
				if net[interface][0].family == 2:  # AF_INET (IPv4)
					ipv4 = True
					connect = True
				if net[interface][0].family == 10:  # AF_INET6 (IPv6)
					ipv6 = True
					connect = True

				ip_list = []  # 存储当前网卡的所有 IP 地址

				# 如果网卡已连接且不在强制命名列表中，进一步处理
				if net[interface] and connect:
					if interface not in self.force_name:
						print(net)  # 打印网络接口信息（调试用途）

						# 将网卡名称添加到已连接网卡列表
						self.eth_connected_list.append(interface)

						# 根据 IPv4 和 IPv6 支持情况分类存储网卡名称
						if self._ipv4 and ipv4:
							self._ipv4_list.append(interface)
						if self._ipv6 and ipv6:
							self._ipv6_list.append(interface)

						# 遍历网卡的所有地址，提取 IP 地址并存储
						for addr in net[interface]:
							print(addr.address)  # 打印地址信息（调试用途）
							print(addr.family)  # 打印地址协议族（调试用途）
							ip_list.append(addr.address)

						# 将网卡名称及其对应的 IP 地址列表存入字典
						self.eth_connected_dict[interface] = ip_list

				# 返回 True 表示成功获取网卡信息
				return True

		except Exception as err:
			# 捕获异常并打印错误信息
			print(err)

		# 返回 False 表示获取网卡信息失败
		return False



if __name__ == "__main__":
	e = NewEthTools()
	e.get_connected_eth_list4()
