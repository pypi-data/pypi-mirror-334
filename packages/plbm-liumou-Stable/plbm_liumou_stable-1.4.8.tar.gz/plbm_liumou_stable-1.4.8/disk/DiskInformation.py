#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   DiskInformation.py
@Time    :   2022-08-10 11:10
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
import psutil


class DiskInfo:
	def __init__(self):
		self.dev_list = []
		self.partition_path = {}
		self.partition_total = {}
		self.partition_used = {}
		self.partition_free = {}
		self.utilization_rate = {}
		self.idle_rate = {}

	def base(self):
		"""
		获取基础信息
		:return:
		"""
		# 获取设备(分区)列表
		for i in psutil.disk_partitions(all=False):
			dev = i.device
			self.dev_list.append(dev)
			# 记录设备与挂载路径信息
			self.partition_path[dev] = i.mountpoint
			# 获取设备使用情况
			info = psutil.disk_usage(self.partition_path[dev])
			# 记录设备与总容量
			self.partition_total[dev] = info.total
			# 记录设备与使用量
			self.partition_used[dev] = info.used
			# 记录设备与剩余量
			self.partition_free[dev] = info.free
			# 记录设备与使用率
			self.utilization_rate[dev] = info.used / info.total
			# 记录设备与空闲率
			self.idle_rate[dev] = info.free / info.total

	def info(self, base=1024):
		"""
		获取磁盘使用情况
		:param base: 设置存储容量单位转换进制
		:return:
		"""
		self.base()
		for dev in self.dev_list:
			print('\n')
			print(f"当前设备/分区: {dev}")
			print(f"挂载路径: {self.partition_path[dev]}")
			print(f"总容量: {self.partition_total[dev] / base / base} MB")
			print(f"使用量: {self.partition_used[dev] / base / base} MB")
			print(f"剩余量: {self.partition_free[dev] / base / base} MB")
			print(f"使用率: {str(float(self.utilization_rate[dev]) * 100)[0:5]} %")
			print(f"空闲率: {str(float(self.idle_rate[dev]) * 100)[0:5]} %")


if __name__ == "__main__":
	up = DiskInfo()
	up.info()
