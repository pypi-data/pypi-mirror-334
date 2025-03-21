# -*- encoding: utf-8 -*-
"""
@File    :   FileManagement.py
@Time    :   2022/04/13 20:16:27
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   文件管理
"""
from os import path, makedirs
from shutil import rmtree, copy2, move
from subprocess import getstatusoutput
from .logger import ColorLogger


class NewFile:
	def __init__(self, target=None, log=True, log_file=None, txt_log=False):
		"""
		初始化文件管理模块。

		:param target: 管理目标，指定需要管理的文件或目录，默认为 None。
		:param log: 是否开启日志功能，布尔值，默认为 True。
		:param log_file: 日志文件路径，指定日志输出的文件，默认为 None。
		:param txt_log: 是否开启文件日志功能，布尔值，默认为 False。
		:return: 无返回值。
		"""
		# 初始化日志功能标志
		self.log = log
		# 初始化 MD5 校验值为空字符串
		self.md5 = ''
		# 设置管理目标
		self.target = target
		# 初始化日志记录器，支持颜色日志和文件日志功能
		self.logger = ColorLogger(file=log_file, txt=txt_log)


	def rmdir(self, target=None, ignore_errors=True):
		"""
		删除指定路径的文件夹。

		:param target: str, 可选参数，需要删除的文件夹路径。如果未提供，则使用实例的 `self.target`。
		:param ignore_errors: bool, 可选参数，是否忽略删除过程中发生的错误。默认为 True。
		:return: bool, 如果文件夹不存在或成功删除，则返回 True；如果删除失败，则返回 False。
		"""
		# 如果未指定目标路径，则使用实例的默认路径
		if target is None:
			target = self.target

		# 检查目标路径是否为文件夹
		if path.isdir(target):
			try:
				# 尝试递归删除文件夹及其内容
				rmtree(path=target, ignore_errors=ignore_errors)
				return True
			except Exception as e:
				# 捕获异常并记录错误日志
				self.logger.error(str(e))
				return False

		# 如果目标路径不是文件夹，则返回 True
		return True


	def move(self, src, dst, cover=False):
		"""
		移动文件或目录。

		:param src: 源文件或目录的路径。可以是字符串或路径对象。
		:param dst: 目标文件或目录的路径。可以是字符串或路径对象。
		:param cover: 是否覆盖目标路径。如果为True，且目标路径已存在，则会先删除目标路径。默认为False。
		:return: 如果移动成功，返回True；如果发生异常，记录错误日志并返回False。
		"""
		# 检查源路径是否存在
		if path.exists(src):
			# 如果cover为True且目标路径存在，则删除目标路径
			if cover:
				self.rmdir(target=dst)
			try:
				# 尝试移动源路径到目标路径
				move(src=str(src), dst=str(dst))
				return True
			except Exception as e:
				# 捕获异常并记录错误日志
				self.logger.error(str(e))
				return False


	def copyfile(self, src, dst, cover=False):
		"""
		复制文件或文件夹到目标路径。

		:param src: 源文件或文件夹的路径。必须是有效的路径。
		:param dst: 目标文件路径或文件夹路径。如果为文件夹路径，源文件将被复制到该文件夹中。
		:param cover: 布尔值，指示当目标文件已存在时是否覆盖。默认为False（不覆盖）。
					  如果设置为True，且目标文件已存在，则会先将目标文件移动到一个临时位置。
		:return: 布尔值，指示复制操作是否成功。成功返回True，失败返回False。
		"""
		ok = False  # 初始化操作状态为失败

		# 检查源文件是否存在
		if path.exists(src):
			# 如果允许覆盖且目标文件已存在，先将目标文件移动到临时位置
			if cover and path.exists(dst):
				self.move(src=dst, dst=str('%s_move' % dst))

			try:
				# 尝试复制文件或文件夹到目标路径
				copy2(src=str(src), dst=str(dst))
				ok = True  # 如果复制成功，更新操作状态为成功
			except Exception as e:
				# 捕获异常并记录错误日志
				self.logger.error(str(e))

			# 如果复制成功且启用了覆盖选项，删除临时移动的文件
			if ok:
				self.rmdir(target=str('%s_move' % dst))

		return ok  # 返回操作状态


	def mkdir_p(self, target=None, mode=644):
		"""
		创建递归文件夹，类似于Linux中的`mkdir -p`命令。

		:param target: 需要创建的路径。如果未提供，则默认使用实例化对象的`target`属性。
		:param mode: 创建文件夹时的权限模式，默认值为644。
		:return: 如果文件夹创建成功或已存在，则返回True；如果发生异常，则返回False。
		"""
		# 如果未指定目标路径，则使用实例化对象的target属性
		if target is None:
			target = self.target

		try:
			# 尝试递归创建目标路径的文件夹，exist_ok=True确保路径已存在时不抛出异常
			makedirs(name=target, mode=mode, exist_ok=True)
			return True
		except Exception as e:
			# 捕获异常并记录错误日志
			self.logger.error(str(e))
			return False


	def get_md5(self, filename=None):
		"""
		获取文件的MD5值。

		:param filename: str, 可选参数，需要获取MD5值的文件路径。如果未提供，则使用 self.target 作为文件路径。
		:return: bool, 表示是否成功获取MD5值。如果成功，具体的MD5值会存储在 self.md5 中。
		"""
		# 初始化获取状态为 False
		get = False

		# 如果未提供文件名且 self.target 存在，则使用 self.target 作为文件路径
		if filename is None and self.target:
			filename = self.target

		# 检查文件是否存在
		if path.isfile(filename):
			# 使用系统命令计算文件的MD5值，并通过 awk 提取结果
			c = "md5sum %s | awk '{print $1}'" % filename
			res = getstatusoutput(c)

			# 如果命令执行成功 (返回码为0)，将结果存储到 self.md5 并更新获取状态
			if res[0] == 0:
				self.md5 = res[1]
				get = True
		else:
			# 如果文件不存在，记录警告日志
			self.logger.warning('文件不存在: %s' % filename)

		# 返回获取状态
		return get



# 主程序入口，用于执行文件操作相关的功能。
# 以下代码展示了如何使用一个假设的 `NewFile` 类来执行文件 MD5 校验、目录创建和删除操作。

if __name__ == "__main__":
	# 创建一个 NewFile 实例，指定目标文件为 `/etc/hosts`。
	fm = NewFile(target='/etc/hosts')

	# 调用 get_md5 方法计算目标文件的 MD5 值。
	fm.get_md5()

	# 调用 mkdir_p 方法递归创建目标目录 `/home/liumou`，并设置权限为 666。
	fm.mkdir_p(target='/home/liumou', mode=666)

	# 调用 rmdir 方法删除目标目录 `/home/liumou`。
	fm.rmdir(target='/home/liumou')
