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
from src.plbm_liumou_Stable import NewPackageManagement
from ColorInfo import ColorLogger


class ServiceManager:
	def __init__(self, pac, password):
		self.package = pac
		self.pac = NewPackageManagement(password=password, package="vsftpd")
		self.logger = ColorLogger(class_name=self.__class__.__name__)

	def remove(self):
		if self.pac.installed():
			self.logger.info(f"已安装: {self.package}")
			if self.pac.uninstall():
				self.logger.info(f"卸载成功: {self.package}")
			else:
				self.logger.error(f"卸载失败: {self.package}")

		else:
			self.logger.warning(f"未安装: {self.package}")


if __name__ == "__main__":
	demo = ServiceManager(pac="vsftpd", password="demo")
	demo.remove()
