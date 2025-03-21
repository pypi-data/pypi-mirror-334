#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   ReplaceIP.py
@Time    :   2022-06-29 12:00
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   更换IP
"""
from os import system
from subprocess import getoutput, getstatusoutput
from sys import exit
from time import sleep
from platform import system as os_type
from loguru import logger as log
from argparse import ArgumentParser


class GetNetwork:
	def __init__(self):
		self.gw = None
		self.ip = None
		self.mask = 24
	
	def get_ip(self):
		"""
		get localhost ip address
		:return:
		"""
	
	def get_gw(self):
		"""
		get localhost gateway address

		:return:
		"""


class ReplaceIp:
	def __init__(self,
	             sub,
	             gw,
	             mask,
	             connect="zb",
	             dev_="USB",
	             start=2,
	             stop=253,
	             debug=False):
		"""
		更换IP
		:param sub: 子网地址
		:param mini: 最小IP
		:param max: 最大IP
		:param gw: 设置网关
		:param connect: 连接名称
		:param mask: 子网掩码
		"""
		self.debug = debug
		self.mask = mask
		self.os_ = os_type()
		self.gw = gw
		self.connect = connect
		self.sub = sub
		self.max = stop
		self.mini = start
		if int(self.mini) > int(self.max):
			print("参数配置错误: 最小数大于最大数")
			exit(1)
		# 存活的IP
		self.ip = []
		self.dev = dev_
		if self.os_.lower() == 'linux'.lower():
			self.dev = getoutput("nmcli d | grep ethernet").split(" ")[0]
	
	def create(self):
		"""
		生成IP
		:return:
		"""
		for ip in range(self.mini, self.max):
			ip_ = str(self.sub) + str(ip)
			self.ip.append(ip_)
	
	def ping(self, ip):
		"""
		使用ping检查是否有人使用这个IP
		:param ip:
		:return:
		"""
		c = "ping %s" % ip
		if self.os_.lower() == 'linux'.lower():
			c = str(c) + " -c 5"
		if getstatusoutput(c)[0] == 0:
			log.debug("IP已有人使用: %s" % ip)
			return True
		log.info("IP未有人使用: %s " % ip)
		return False
	
	def dns(self):
		"""
		配置dns
		"""
		if str(os_type()).lower() == "Windows".lower():
			log.debug("暂不更新")
			return True
		s = 0
		for i in ["119.29.29.29", "180.76.76.76"]:
			if int(s) == 0:
				cmd = str("""nmcli connection modify zb ipv4.dns %s""" % i)
			else:
				cmd = str("""nmcli connection modify zb +ipv4.dns %s""" % i)
			u = getstatusoutput(cmd)
			if u[0] == 0:
				log.info("DNS配置成功: %s" % i)
			else:
				log.error("DNS配置失败: %s" % i)
			s += 1
	
	def add_connect(self):
		"""
		添加连接
		:return:
		"""
		connect_list_cmd = """nmcli connection | awk '{print $1}'"""
		connect_list = getoutput(connect_list_cmd).split("\n")
		if str(self.connect) in connect_list:
			mode_cmd = """nmcli connection show %s  | grep ipv4.method | awk '{print $2}'""" % self.connect
			if getoutput(mode_cmd) == str('auto'):
				manual_cmd = """nmcli connection modify %s ipv4.method manual""" % self.connect
				r = getstatusoutput(manual_cmd)
				if r[0] == 0:
					log.info("修改IP连接为手动模式: 成功")
				else:
					log.error("修改IP连接为手动模式: 失败")
					log.warning("请手动设置一个静态连接配置")
					print(r[1])
					exit(1)
		else:
			add_connect_cmd = """nmcli connection add type ethernet ipv4.method manual  con-name %s ifname %s""" % (
				self.connect,
				self.dev)
			r = getstatusoutput(add_connect_cmd)
			if r[0] == 0:
				log.info("连接创建成功: %s" % self.connect)
			else:
				log.error("连接创建失败: %s" % self.connect)
				print(r[1])
				exit(2)
	
	def update(self, ip):
		"""
		更新IP
		:return:
		"""
		ok = True
		if self.ping(ip=ip):
			return False
		if self.os_.lower() == 'Windows'.lower():
			mask = '255.255.255.0'
			if self.mask == 32:
				mask = "255.255.255.255"
			elif self.mask == 16:
				mask = '255.255.0.0'
			try:
				system("netsh interface ip set address %s static %s %s %s" % (self.dev, ip, mask, self.gw))
			except Exception as e:
				log.error(e)
				ok = False
		else:
			self.add_connect()
			c = "nmcli connection modify %s ipv4.addresses %s/%s  > /dev/null" % (self.connect,
			                                                                      ip,
			                                                                      self.mask)
			i = getstatusoutput(c)
			if i[0] == 0:
				log.info("IP修改成功: %s" % ip)
				gw_cmd = """nmcli connection modify %s ipv4.gateway %s""" % (self.connect,
				                                                             self.gw)
				if getstatusoutput(gw_cmd)[0] == 0:
					log.info("网关设置成功")
					u_ = "nmcli connection up %s  > /dev/null" % self.connect
					system(u_)
					d_ = "nmcli device reapply %s > /dev/null" % self.dev
					system(d_)
				else:
					log.error("网关设置失败")
					exit(3)
			else:
				log.error(" IP 修改失败: %s" % ip)
				print(i[1])
				ok = False
		sleep(5)
		try:
			c = "ping %s " % self.gw
			if self.os_.lower() == 'Linux'.lower():
				c = c + str(" -c 3 > /dev/null")
			system(c)
		except Exception as e:
			log.error(e)
			ok = False
		return ok
	
	def start(self):
		"""
		开始处理
		:return:
		"""
		if self.ping(self.gw):
			log.info("当前IP可正常使用,无需更换")
			self.dns()
		else:
			self.create()
			for ip in self.ip:
				if self.update(ip):
					return True


if __name__ == "__main__":
	arg = ArgumentParser(description='当前脚本版本: 1.0', prog="自动更换本机IP-梯度")
	arg.add_argument('-s', '--sub', type=str, help='设置IP子网', required=True)
	arg.add_argument('-g', '--gateway', type=str, help='设置网关', required=True)
	arg.add_argument('-m', '--mask', type=int, default=24, help='设置掩码,默认: 24', required=False)
	arg.add_argument('-c', '--connect', type=str, default='connect', help='设置连接名称,默认: connect', required=False)
	arg.add_argument('-u', '--up', type=int, default=3, help='设置IP生成开始IP', required=False)
	arg.add_argument('-e', '--end', type=int, default=253, help='设置IP生成最终IP', required=False)
	arg.add_argument('-y', '--yes', type=bool, default=False, help='是否显示提示内容,默认:1', required=False)
	args = arg.parse_args()
	e_ = int(args.end)
	u_ = int(args.up)
	sub_ = str(args.sub)
	gw_ = str(args.gateway)
	y_ = bool(args.yes)
	mask_ = int(args.mask)
	connect_ = str(args.connect)
	if gw_ is None or len(gw_) <= 8:
		log.error("plase use -gw set gateway")
		exit(1)
	up = ReplaceIp(sub=sub_, gw=gw_, mask=mask_, connect=connect_, start=u_, stop=e_)
	up.start()
