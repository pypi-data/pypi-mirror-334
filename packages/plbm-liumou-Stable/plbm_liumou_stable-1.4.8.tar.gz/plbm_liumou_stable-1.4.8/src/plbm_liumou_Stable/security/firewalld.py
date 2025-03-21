#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   firewalld.py
@Time    :   2022-08-11 11:06
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   firewalld防火墙管理
"""
from sys import exit
from subprocess import getstatusoutput


class FireWall:
	def __init__(self):
		self.agreement = 'tcp'
		self.port = 80
		self.source = "0.0.0.0/0"
		self.zone = 'public'
		self.ok = False
		self.status()
	
	def open_all(self, agreement=None, port=None, zone=None, permanent=True):
		"""
		开放端口给某个安全域的所有设备
		:param permanent: 是否设置永久生效
		:param zone: 指定区域
		:param agreement: 协议(tcp/udp),默认：TCP
		:param port: 端口号,默认: 80
		:param source: 源地址,默认: 0.0.0.0/0
		:param family: 设置IP协议类型
		:return: 配置结果
		"""
		if agreement is None:
			agreement = self.agreement
		if port is None:
			port = self.port
		if zone is None:
			zone = self.zone
		cmd = f"firewall-cmd --zone={zone} --add-port={port}/{agreement} "
		cmd = f"firewall-cmd --zone={zone} --add-port={port}/{agreement} "
		if permanent:
			cmd = str(f"{cmd} --permanent")
		print(cmd)
	
	def get(self):
		"""
		获取已经开放的端口
		:return:
		"""
		cmd = "firewall-cmd --zone=public --list-ports"
		g = getstatusoutput(cmd)
		if g[0] == 0:
			print("执行查询成功")
			print(g[1])
		else:
			print("执行查询失败")
	
	def start(self):
		"""
		启动服务
		:return:
		"""
		cmd = "systemctl restart firewalld.service"
		c = getstatusoutput(cmd)
		if c[0] == 0:
			self.status()
		else:
			print("防火墙启动失败")
			print(c[1])
			exit(1)
	
	def status(self):
		"""
		获取当前状态
		:return:
		"""
		cmd = getstatusoutput("firewall-cmd --state")
		if cmd[0] == 0:
			if str(cmd[1]).lower() == 'running'.lower():
				print("服务已启动")
				self.ok = True
				return True
			else:
				self.start()
		else:
			print("状态查看失败")
			print(cmd[1])
			exit(2)


if __name__ == "__main__":
	up = FireWall()
	up.get()
