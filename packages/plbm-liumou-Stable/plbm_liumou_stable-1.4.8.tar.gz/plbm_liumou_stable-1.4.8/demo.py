# -*- encoding: utf-8 -*-
"""
@File    :   demo.py
@Time    :   2022-10-24 22:45
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
from plbm_liumou_Stable import NewNmcli
from plbm_liumou_Stable import ColorLogger


class TestCon:
	def __init__(self):
		self.logger = ColorLogger(class_name=self.__class__.__name__)

	def get(self):
		try:
			n = NewNmcli()
			self.logger.info("开始测试获取连接信息")
			u = n.get_con_info(con="wifi")
			if u["status"]:
				print("获取成功")
				print(u)
			else:
				print("获取失败")
			self.logger.info("测试成功")
		except Exception as e:
			self.logger.warning("测试失败: ", str(e))

	def start(self):
		self.get()


class Test:
	def __init__(self):
		self.logger = ColorLogger(class_name=self.__class__.__name__)

	def con(self):
		self.logger.info("开始进入连接测试")
		c = TestCon()
		c.start()

	def start(self):
		self.con()


if __name__ == "__main__":
	t = Test()
	t.start()
