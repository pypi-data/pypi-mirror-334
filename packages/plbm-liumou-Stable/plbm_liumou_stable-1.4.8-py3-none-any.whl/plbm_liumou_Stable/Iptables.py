#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   iptables.py
@Time    :   2022-08-11 11:55
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   防火墙管理
"""

from subprocess import getstatusoutput
from sys import exit

from .Jurisdiction import Jurisdiction
from .Service import NewService
from .Cmd import NewCommand
from .logger import ColorLogger


class IpTables:
	def __init__(self, password=None, logs=False, log_file=None, port=80, source=None, zone=None, direction="INPUT"):
		"""
		Iptables防火墙软件配置初始化函数。

		:param password: str, 可选参数，主机密码。如果当前用户为root，则不需要提供密码。
		:param logs: bool, 可选参数，是否显示详细日志信息，默认为False。
		:param log_file: str, 可选参数，日志文件路径。如果未提供，则日志不会写入文件。
		:param port: int, 可选参数，配置的端口号，默认为80。
		:param source: str, 可选参数，源IP地址或网段，默认为"0.0.0.0/0"。
		:param zone: str, 可选参数，防火墙区域，默认为"public"。
		:param direction: str, 可选参数，规则方向，默认为"INPUT"（入口流量）。如果值不是"INPUT"，则设置为空字符串。
		:return: None
		"""
		# 初始化日志文件和日志显示设置
		self.log_file = log_file
		self.logs = logs
		self.logger = ColorLogger(file=log_file, txt=logs)

		# 初始化命令执行工具类
		self.cmd = NewCommand(password=password, logs=logs)

		# 验证当前用户的权限，确保有足够的权限操作Iptables
		ju = Jurisdiction(passwd=password, logs=logs)
		if not ju.verification(name='IpTables'):
			self.logger.error("sudo权限验证失败,请检查密码是否正确或者账号是否有权限")
			exit(1)

		# 设置默认协议为TCP
		self.agreement = 'TCP'

		# 设置端口号，并确保其为整数类型
		self.port = int(port)

		# 如果未指定源地址，则默认为"0.0.0.0/0"
		if source is None:
			source = "0.0.0.0/0"
		self.source = source

		# 如果未指定防火墙区域，则默认为"public"
		if zone is None:
			zone = 'public'
		self.zone = zone

		# 标记配置是否成功，默认为False
		self.ok = False

		# 设置规则方向，默认为"INPUT"（入口流量）
		if direction != "INPUT":
			direction = ""
		self.direction = direction

		# 初始化已配置的端口列表及相关数据结构
		self.port_list = []  # 记录已配置的端口列表
		self.port_dic = {}  # 记录端口详细情况
		self.port_accept_list = []  # 查看已配置且接受的端口列表
		self.port_id_port = {}  # 记录ID和端口的关系

		# 初始化服务名称和服务管理工具类
		self.service_name = 'ipsec'
		self.service = NewService(service=self.service_name, password=password, log=logs)

	
	def open_port_appoint_ip(self):
		"""
		开放特定端口给特定主机
		:return:
		"""
		pass
	
	def save(self):
		"""
		保存当前的iptables配置更改。

		参数:
			self: 当前对象实例，包含以下关键属性：
				- cmd: 用于执行命令的对象，需提供sudo方法。
				- logger: 用于记录日志的对象，需提供info和warning方法。

		返回值:
			无返回值。

		功能描述:
			该函数通过调用iptables-save命令保存当前的iptables配置更改，
			并根据命令执行结果记录日志信息。
		"""
		# 调用sudo方法执行iptables-save命令，并指定操作名称为"保存更改"
		self.cmd.sudo(cmd='iptables-save', name='保存更改')

		# 检查命令执行结果的状态码，判断保存是否成功
		if int(self.cmd.code) == 0:
			self.logger.info("保存成功")  # 记录保存成功的日志
		else:
			self.logger.warning("保存失败")  # 记录保存失败的警告日志


	def set_port_appoint_source(self, agreement=None, port=None, source=None, mode="ACCEPT"):
		"""
		设置特定IP接受或拒绝访问特定端口。

		:param agreement: 协议类型，支持tcp、udp、icmp等，默认为None。
						  如果未提供，则使用实例的默认协议(self.agreement)。
		:param port: 端口号，默认为None。
					 如果未提供，则使用实例的默认端口(self.port)。
		:param source: 源地址，默认为None。
					   如果未提供，则使用实例的默认源地址(self.source)。
		:param mode: 策略模式，支持"ACCEPT"(接受)或"REJECT"(拒绝)，默认为"ACCEPT"。
		:return: 配置结果(bool)，通过self.cmd.code判断是否成功。
				 如果命令执行失败，会记录错误日志。
		"""
		# 如果参数未提供，则使用实例的默认值
		if agreement is None:
			agreement = self.agreement
		if port is None:
			port = self.port
		if source is None:
			source = self.source

		# 构造iptables命令，用于设置特定IP对特定端口的访问策略
		cmd = "iptables -A INPUT -p {0} -s {1} --dport {2} -j {3}".format(agreement, source, port, mode)

		# 根据模式设置操作名称，用于日志记录
		name = "开放端口: %s" % port
		if str(mode).lower() == 'REJECT'.lower():
			name = "关闭端口: %s" % port

		# 执行iptables命令
		self.cmd.sudo(cmd=cmd, name=name)

		# 检查命令执行结果，如果失败则记录错误日志
		if int(self.cmd.code) != 0:
			if self.logs:
				mess = str(name) + "失败"
				self.logger.error(mess)

	
	def open_port_all_ip(self, agreement=None, port=None):
		"""
		开放指定端口给所有IP地址。

		:param agreement: 指定协议类型，可选值为 "tcp" 或 "udp"。默认值为 None，
						  如果未提供，则使用实例变量 self.agreement。
		:param port: 指定要开放的端口号，默认值为 None，
					 如果未提供，则使用实例变量 self.port。
		:return: 返回布尔值，表示配置是否成功。如果命令执行成功返回 True，
				 否则返回 False。
		"""
		# 如果未指定协议，则使用实例变量中的默认协议
		if agreement is None:
			agreement = self.agreement

		# 如果未指定端口，则使用实例变量中的默认端口
		if port is None:
			port = self.port

		# 构造 iptables 命令以开放指定端口
		cmd = "iptables -A INPUT -p {0} --dport {1} -j ACCEPT ".format(agreement, port)
		print(cmd)

		# 执行命令并获取执行结果
		c = getstatusoutput(cmd)

		# 根据命令执行结果判断是否成功
		if c[0] == 0:
			print("开放成功: ", port)
			self.save()  # 保存配置
			return True
		else:
			print("开放失败: ", port)

		return False

	
	def delete_port(self, port):
		"""
		通过指定的端口号删除对应的策略。

		Args:
			port (int): 需要删除的端口号。

		Returns:
			None: 该函数没有返回值。
		"""
		# 获取当前对象的状态或数据，具体逻辑由 self.get() 实现
		self.get()

		# 初始化一个列表，用于存储需要删除的 ID
		del_id_list = []

		# 遍历 self.port_id_port 字典，查找与指定端口匹配的 ID
		for id_ in self.port_id_port:
			port_ = self.port_id_port[id_]
			if int(port_) == int(port):
				del_id_list.append(id_)

		# 如果找到需要删除的 ID，则调用 delete_port_to_id 方法执行删除操作
		if del_id_list:
			self.delete_port_to_id(r_id=del_id_list, auto=True)

	
	def delete_port_to_id(self, r_id=None, auto=False):
		"""
		通过ID删除iptables中的策略规则。

		参数说明：
		:param r_id: list类型，可选参数，表示需要删除的端口ID列表。如果未提供，则默认为空列表。
		:param auto: bool类型，可选参数，表示是否使用自动模式。如果为False，则进入对答模式，用户手动输入需要删除的ID。
		:return: 无返回值。

		功能描述：
		- 如果未提供r_id且auto为False，则进入对答模式，用户需手动输入需要删除的策略ID。
		- 根据输入的ID列表，逐条删除iptables中的INPUT链规则。
		- 删除过程中会动态调整ID值以应对因删除导致的规则序号变化。
		- 每次删除成功或失败都会记录日志信息。
		"""
		if r_id is None:
			r_id = []

		# 如果未启用自动模式，则进入对答模式，提示用户输入需要删除的策略ID
		if not auto:
			print("使用对答模式")
			print(getstatusoutput("iptables -L -n --line-numbe")[1])
			id_ = input("请输入需要删除的策略ID值(整数),每个ID之间使用空格间隔\n")
			r_id = str(id_).split(' ')

		del_sum = 0  # 记录已删除的规则数量，用于动态调整ID值

		# 遍历需要删除的ID列表，逐条删除对应的iptables规则
		for id_del in r_id:
			self.logger.debug("\n删除源id: %s" % id_del)

			# 如果已经删除过规则，则需要调整当前ID值以应对规则序号的变化
			if int(del_sum) != 0:
				print("由于条目发生变化, 源规则ID [ {0} ] 减去 [ {1} ]".format(id_del, del_sum))
			id_del = int(id_del) - int(del_sum)

			# 构造删除命令并执行
			cmd = "iptables -D INPUT {0}".format(id_del)
			if self.cmd.sudo(cmd=cmd, terminal=False):
				self.logger.info('删除成功: %s' % id_del)
			else:
				self.logger.error("删除失败: %s" % id_del)

			del_sum += 1  # 更新已删除规则计数
	
	def get(self):
		"""
		获取已经开放的端口信息，并将结果存储在类的属性中。

		该函数通过执行系统命令 `iptables -L -n --line-number` 获取防火墙规则，
		解析输出内容，提取端口信息，并将其分类存储到类的多个属性中。

		:return: None
		"""
		# 定义用于查询防火墙规则的命令
		cmd = "iptables -L -n --line-number | grep -v ^Chain | grep -v ^num | sed 's/\t/_/g'"
		g = getstatusoutput(cmd)

		if g[0] == 0:
			# 如果命令执行成功，解析输出内容
			port_str_list = str(g[1]).split('\n')
			for port_str in port_str_list:
				# 将每行数据中的空格替换为下划线，并分割成列表
				port_str_list = str(port_str).replace(' ', '_').split('_')
				result = []

				# 过滤掉空字符串，保留有效字段
				if len(port_str_list) >= 2:
					for i in port_str_list:
						if str(i) != '':
							result.append(i)

					# 提取端口号并存储相关信息
					port_ = str(result[7]).split(':')[1]

					# 记录ID与端口的映射关系
					self.port_id_port[result[0]] = port_

					# 如果端口未被记录，则添加到相关列表和字典中
					if port_ not in self.port_list:
						self.port_dic[port_] = result
						self.port_list.append(port_)

						# 如果规则为ACCEPT类型，则将端口添加到接受列表
						if result[1] == 'ACCEPT':
							self.port_accept_list.append(port_)
		else:
			# 如果命令执行失败，打印错误提示
			print("执行查询失败")

	
	def start(self):
		"""
		启动服务。

		该函数调用 `self.service.restart()` 方法来重新启动服务。

		:return: 返回 `self.service.restart()` 的执行结果，具体返回值类型和内容取决于 `restart` 方法的实现。
		"""
		return self.service.restart()

	
	def status(self):
		"""
		获取当前状态。

		该函数调用内部服务的 `status` 方法，返回其结果。

		:param self: 当前对象实例，包含对服务的引用。
		:return: 返回调用 `self.service.status()` 的结果，具体类型和内容取决于 `self.service.status()` 的实现。
		"""
		# 调用服务的 status 方法获取当前状态
		res = self.service.status()
		return res

	
	def clean_all(self):
		"""
		删除所有iptables规则，包括自定义链和计数器的清理。

		参数:
			self: 当前对象实例，包含cmd和logger属性。
				- cmd: 用于执行系统命令的对象，需实现sudo方法。
				- logger: 用于记录日志的对象，需实现info和error方法。

		返回值:
			无返回值。
		"""
		sum_ = 0  # 记录成功执行的命令数量

		# 遍历并执行清理iptables规则的相关命令
		for cmd in ["iptables -X", "iptables -F", "iptables -Z"]:
			if self.cmd.sudo(cmd=cmd, terminal=False):
				sum_ += 1

		# 根据命令执行结果判断清理是否成功
		if int(sum_) == 3:
			self.logger.info("清除成功")  # 所有命令均成功执行
		else:
			self.logger.error("清除失败")  # 部分或全部命令执行失败



# 主程序入口，当该文件作为主程序运行时执行以下代码。
# 该代码块创建了一个 IpTables 类的实例，并调用其 status 方法。
# 注意：IpTables 类的定义和 status 方法的功能未在当前代码中提供。

if __name__ == "__main__":
	# 创建 IpTables 类的实例
	up = IpTables()

	# 调用 status 方法，可能用于检查或显示 IpTables 的状态
	up.status()
