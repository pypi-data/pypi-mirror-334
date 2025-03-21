# -*- encoding: utf-8 -*-
"""
@File    :   ColorInfo.py
@Time    :   2022-10-19 16:01
@Author  :   坐公交也用券
@Version :   1.1.9
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   彩色日志
"""
import inspect
import os
from datetime import datetime
from os import path, environ
import platform
from threading import Lock
from sys import exit


class ColorLogger:
	def __init__(self, file=None, txt=False, class_name=None, cover=False, fileinfo=False, basename=True):
		"""
		初始化日志模块
		:param file: 设置日志文件 (字符串，绝对路径)
		:param txt: 是否启用文本记录功能 (布尔值)
		:param class_name: 调用的Class名称 (字符串)
		:param cover: 当使用文本记录的时候，是否覆盖原内容 (布尔值)
		:param fileinfo: 是否显示日志文件信息 (布尔值)
		:param basename: 设置日志文件显示信息, True(只显示文件名), False(显示绝对路径) (布尔值)
		"""
		# 参数校验
		if file and not isinstance(file, str):
			raise ValueError("参数 'file' 必须是字符串类型")
		if not isinstance(txt, bool):
			raise ValueError("参数 'txt' 必须是布尔类型")
		if class_name and not isinstance(class_name, str):
			raise ValueError("参数 'class_name' 必须是字符串类型")
		if not isinstance(cover, bool):
			raise ValueError("参数 'cover' 必须是布尔类型")
		if not isinstance(fileinfo, bool):
			raise ValueError("参数 'fileinfo' 必须是布尔类型")
		if not isinstance(basename, bool):
			raise ValueError("参数 'basename' 必须是布尔类型")

		# 颜色代码管理
		self.colors = {
			"Red": "\033[31m",  # 红色
			"Greet": "\033[32m",  # 绿色
			"Yellow": '\033[33m',  # 黄色
			"Blue": '\033[34m',  # 蓝色
			"RESET_ALL": '\033[0m'  # 清空颜色
		}

		# 日志等级配置
		self.level_dic = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
		self.level_text = 0  # 文件记录最低等级
		self.level_console = 0  # 控制台显示最低等级

		# 初始化属性
		self.basename = basename
		self.fileinfo = fileinfo
		self.cover = cover
		self.class_name = class_name
		self.txt_mode = txt
		self.file_name = None
		self.file_path = file if file and path.isabs(file) else None
		self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 格式化日期
		self.line_ = 1
		self.module_name = None
		self.filename = None
		self.msg1 = None
		self.format_filename = True
		self.format_date = True
		self.format_time = True
		self.format_class = True
		self.format_fun = True
		self.format_line = True
		self.format_level = True
		self._date = None
		self._lock = Lock()  # 用于确保线程安全
		# 检查文件路径有效性
		if self.file_path:
			if not path.exists(path.dirname(self.file_path)):
				raise ValueError(f"日志文件路径无效: {self.file_path}")
			if not os.access(path.dirname(self.file_path), os.W_OK):
				raise PermissionError(f"无权限写入日志文件路径: {self.file_path}")

		# 初始化实例参数
		self._init_fun()


	def _init_fun(self):
		"""
		初始化函数
		:return:
		"""
		# 如果 file_path 为 None 且启用了文本模式，则设置默认日志文件路径
		if self.file_path is None and self.txt_mode:
			try:
				home_dir = environ.get('HOME') or environ.get('USERPROFILE')
				if not home_dir:
					raise ValueError("无法获取用户主目录路径")
				self.file = path.join(home_dir, 'ColorInfo.log')
				self.file_path = path.abspath(self.file)
			except Exception as e:
				print(f"初始化日志文件路径失败: {e}")
				exit(1)
		else:
			self.file_name = " "
		self.reset_color = self.colors.get("RESET_ALL", "")
		# 如果开启了文本记录模式，则实例化文件写入对象
		if self.txt_mode:
			try:
				mode = 'w+' if self.cover else 'a+'
				self.txt_wr = open(file=self.file_path, mode=mode, encoding='utf-8')
			except FileNotFoundError:
				print(f"文件路径不存在: {self.file_path}")
				exit(1)
			except PermissionError:
				print(f"无权限访问文件: {self.file_path}")
				exit(1)
			except Exception as e:
				print(f"初始化文件写入失败: {e}")
				exit(1)

		# 如果需要获取文件名，则设置 file_name
		if self.basename:
			self.file_name = path.basename(str(self.file_path))


	def set_format(self, date_on=True, time_on=True, filename_on=True, class_on=True, fun=True, line=True, level=True):
		"""
		设置日志格式的开关，控制日志输出中各部分信息的显示与否。
		默认情况下，所有格式开关均开启。

		:param date_on: 是否显示日期，默认为 True。格式示例：2022-11-03。
		:param time_on: 是否显示时间，默认为 True。格式示例：20:42:24。
		:param filename_on: 是否显示文件名（源码文件），默认为 True。格式示例：ColorInfo.py。
		:param class_on: 是否显示类名，默认为 True。
		:param fun: 是否显示函数名，默认为 True。
		:param line: 是否显示行号，默认为 True。格式示例：line: 230。
		:param level: 是否显示日志等级，默认为 True。格式示例：DEBUG。
		:return: 无返回值。
		"""
		# 设置日期显示开关
		self.format_date = date_on
		# 设置文件名显示开关
		self.format_filename = filename_on
		# 设置时间显示开关
		self.format_time = time_on
		# 设置类名显示开关
		self.format_class = class_on
		# 设置函数名显示开关
		self.format_fun = fun
		# 设置行号显示开关
		self.format_line = line
		# 设置日志等级显示开关
		self.format_level = level


	def set_level(self, console="DEBUG", text="DEBUG"):
		"""
		设置显示等级，当实际等级低于设置等级时，信息将不会显示或写入。

		:param console: 设置控制台显示的最低等级，默认为 "DEBUG"。
						可选值为 "DEBUG"、"INFO"、"WARNING"、"ERROR"。
						如果传入的值无效，则默认使用 "DEBUG"。
		:param text: 设置文本记录的最低等级，默认为 "DEBUG"。
					 可选值为 "DEBUG"、"INFO"、"WARNING"、"ERROR"。
					 如果传入的值无效，则默认使用 "DEBUG"。
		:return: 无返回值。
		"""
		# 定义有效的日志等级列表
		level_list = ["DEBUG", "INFO", "WARNING", "ERROR"]

		# 检查并校正控制台日志等级，若传入值无效则重置为默认值 "DEBUG"
		if console.upper() not in level_list:
			console = "DEBUG"

		# 检查并校正文本日志等级，若传入值无效则重置为默认值 "DEBUG"
		if text.upper() not in level_list:
			text = "DEBUG"

		# 将校正后的日志等级映射为内部使用的数值
		self.level_console = self.level_dic[console.upper()]
		self.level_text = self.level_dic[text.upper()]


	def fun_info(self, info):
		"""
		获取function信息，并解析传入的info参数以设置类的属性。

		:param info: 一个包含函数相关信息的列表或元组，结构如下：
					 - info[0]: 文件路径或文件名。
					 - info[1]: 函数所在的行号。
					 - info[2]: 模块名称。
		:return: 无返回值。该方法主要用于设置类的属性：line_、module_name 和 filename。
		"""
		# 设置函数所在的行号
		self.line_ = info[1]

		# 设置模块名称
		self.module_name = info[2]

		# 提取文件名并处理路径分隔符问题
		filename = info[0]
		filename = str(filename).split('/')[-1]  # 提取文件名（适用于Unix/Linux系统）

		# 如果运行环境为Windows系统，则进一步处理路径分隔符
		if platform.system().lower() == 'windows'.lower():
			filename = path.split(filename)[1]

		# 设置最终的文件名属性
		self.filename = filename


	def _create_msg(self, msg, level='DEBUG'):
		"""
		根据提供的信息和格式化选项，生成一条格式化的消息字符串。

		:param msg: 需要格式化的信息内容。
		:param level: 信息的级别，默认为 'DEBUG'。
		:return: 无返回值，生成的消息存储在实例变量 self.msg1 中。

		该函数根据实例变量中的格式化选项（如日期、时间、文件名等）逐步构建消息字符串。
		"""
		# 初始化消息列表，用于高效拼接
		msg_parts = []

		# 提取日期和时间部分，并增加异常处理
		try:
			date_, time_ = self.date.split(' ')
		except (AttributeError, ValueError):
			date_, time_ = '', ''  # 如果日期格式不正确，使用空字符串代替

		# 根据格式化选项添加日期
		if self.format_date:
			msg_parts.append(date_)

		# 根据格式化选项添加时间
		if self.format_time:
			msg_parts.append(time_)

		# 根据格式化选项添加文件名
		if self.format_filename:
			msg_parts.append(self.filename)

		# 根据格式化选项添加行号
		if self.format_line:
			msg_parts.append(f"line: {self.line_}")

		# 根据格式化选项添加类名
		if self.class_name is not None and self.format_class:
			msg_parts.append(f"Class: {self.class_name}")

		# 根据格式化选项添加函数名
		if self.module_name != '<module>' and self.format_fun:
			msg_parts.append(f"Function: {self.module_name}")

		# 根据格式化选项添加信息级别和原始信息
		if self.format_level:
			msg_parts.append(f"{level}: {msg}")
		else:
			msg_parts.append(msg)  # 确保消息至少包含原始信息

		# 将最终生成的消息存储到实例变量中
		self.msg1 = ' '.join(msg_parts)


	def _wr(self):
		try:
			# 如果开启了文本日志
			if self.txt_mode:
				self.txt_wr.write(self.msg1)
				self.txt_wr.write("\n")
		except Exception as e:
			# 检查颜色字典是否存在对应的键
			red_color = self.colors.get("Red", "")
			reset_color = self.colors.get("RESET_ALL", "")
			# 使用颜色字典中的值输出错误信息
			print(f"{red_color}{str(e)}{reset_color}")


	def _arg(self, arg):
		"""
		解析参数并将其转换为字符串形式。

		:param arg: 可迭代对象（如字符串、列表、元组等），需要解析的参数。
		:return: 将输入的每个元素转换为字符串后拼接成的完整字符串。
		:raises TypeError: 如果输入参数不是可迭代对象，则抛出异常。
		"""
		# 检查输入是否为可迭代对象
		if not hasattr(arg, '__iter__'):
			raise TypeError("输入参数必须是可迭代对象，例如字符串、列表或元组。")

		# 使用 str.join() 提高字符串拼接效率
		return ''.join(str(i) for i in arg)


	def _get_time(self):
		try:
			# 使用标准的时间格式化方法，避免硬编码字符串操作
			with self._lock:  # 确保线程安全
				self._date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		except Exception as e:
			# 捕获异常并记录日志，避免程序崩溃
			print(f"Error occurred while getting time: {e}")
			self._date = None  # 设置默认值，避免返回意外结果


	def info(self, msg, *arg, **kwarg):
		"""
		打印信息
		:param msg: 打印内容
		:param arg: 可变参数，用于扩展消息内容
		:param kwarg: 关键字参数，用于扩展消息内容
		:return: None
		"""
		try:
			# 获取调用者信息
			caller_frame = inspect.currentframe().f_back
			if caller_frame is None:
				raise ValueError("无法获取调用者信息")
			fun_info = inspect.getframeinfo(caller_frame)
			self.fun_info(info=fun_info)
		except Exception as e:
			# 异常处理，记录错误信息
			self._handle_error(f"获取调用者信息失败: {e}")

		# 缓存消息字符串
		msg_str = str(msg)

		# 处理可变参数和关键字参数
		try:
			if arg:
				msg_str += str(self._arg(arg=arg))
			if kwarg:
				msg_str += str(self._arg(arg=kwarg))
		except Exception as e:
			self._handle_error(f"处理参数失败: {e}")

		# 创建日志消息
		self._create_msg(msg=msg_str, level="INFO")

		# 构造输出信息
		mess = str(self.colors.get("GREEN", "") + self.msg1 + self.reset_color)
		if self.fileinfo and self.txt_mode:
			mess = str(self.colors.get("GREEN", "") + str(self.file_name) + ' <<-- ' + self.msg1 + self.reset_color)

		# 根据日志级别决定是否输出到控制台或文件
		if self._should_log_console():
			print(mess)
		if self._should_log_file():
			self._wr()

	def _should_log_console(self):
		"""判断是否需要输出到控制台"""
		return self.level_console <= 1

	def _should_log_file(self):
		"""判断是否需要写入文件"""
		return self.level_text <= 1

	def _handle_error(self, error_msg):
		"""统一处理错误信息"""
		# 可根据需求扩展错误处理逻辑
		print(f"Error: {error_msg}")


	def debug(self, msg, *arg, **kwarg):
		"""
		打印信息
		:param msg: 打印内容
		:param arg: 可变参数
		:param kwarg: 关键字参数
		:return:
		"""
		try:
			# 获取调用者信息
			fun_info = inspect.getframeinfo(inspect.currentframe().f_back)
			self.fun_info(info=fun_info)
		except Exception as e:
			# 捕获调用栈信息获取失败的异常
			print(f"Failed to retrieve caller info: {e}")

		# 获取时间信息
		self._get_time()

		# 处理 msg 参数
		try:
			if not isinstance(msg, str):
				msg = str(msg) if msg is not None else ""

			# 拼接 arg 和 kwarg
			if arg:
				msg += self._arg(arg=arg)
			if kwarg:
				msg += self._arg(arg=kwarg)
		except Exception as e:
			print(f"Error processing arguments: {e}")
		mess = ''
		# 创建日志消息
		try:
			self._create_msg(msg=msg)
		except Exception as e:
			print(f"Error creating message: {e}")

		# 构建最终输出消息
		try:
			# 安全地从 Blue 字典中获取值，默认为空字符串
			blue_color = self.colors.get("Blue", "")

			mess = f"{blue_color}{self.msg1}{self.reset_color}"
			if self.fileinfo and self.txt_mode:
				mess = f"{blue_color}{self.file_name} <<-- {self.msg1}{self.reset_color}"
		except Exception as e:
			print(f"Error building message: {e}")

		# 控制台输出
		try:
			if self.level_console == 0:
				print(mess)
		except Exception as e:
			print(f"Error printing to console: {e}")

		# 文件写入
		try:
			if self.level_text <= 0:
				self._wr()
		except Exception as e:
			print(f"Error writing to file: {e}")


	def warning(self, msg, *arg, **kwarg):
		"""
		打印信息
		:param msg: 打印内容
		:param arg: 可变参数，用于扩展消息内容
		:param kwarg: 关键字参数，用于扩展消息内容
		:return:
		"""
		try:
			# 获取调用者信息
			fun_info = inspect.getframeinfo(inspect.currentframe().f_back)
			self.fun_info(info=fun_info)
		except Exception as e:
			# 捕获异常并记录
			print(f"Error occurred while fetching caller info: {e}")

		try:
			# 获取时间信息
			self._get_time()
		except Exception as e:
			# 捕获异常并记录
			print(f"Error occurred while fetching time info: {e}")

		# 处理可变参数和关键字参数
		try:
			if arg:
				msg = str(msg) + str(self._arg(arg=arg))
			if kwarg:
				msg = str(msg) + str(self._arg(arg=kwarg))
		except Exception as e:
			# 捕获异常并记录
			print(f"Error occurred while processing arguments: {e}")

		# 创建日志消息
		self._create_msg(msg=msg, level="WARNING")

		# 生成日志输出内容
		base_message = self.colors.get("Yellow", "") + self.msg1 + self.reset_color
		if self.fileinfo and self.txt_mode:
			mess = self.colors.get("Yellow", "") + str(self.file_name) + ' <<-- ' + self.msg1 + self.reset_color
		else:
			mess = base_message

		# 根据日志级别决定是否输出到控制台或文件
		if self.level_console <= 2 or self.level_text <= 2:
			if self.level_console <= 2:
				print(mess)
			if self.level_text <= 2:
				self._wr()


	def error(self, msg, *arg, **kwarg):
		"""
		打印错误信息，并根据配置决定是否输出到控制台或写入文件。

		:param msg: 错误信息的主要内容
		:param arg: 可变参数，用于补充错误信息
		:param kwarg: 关键字参数，用于补充错误信息
		"""
		try:
			# 获取调用者的信息
			fun_info = inspect.getframeinfo(inspect.currentframe().f_back)
			self.fun_info(info=fun_info)
		except Exception as e:
			# 捕获获取调用者信息时的异常
			print(f"Error retrieving caller info: {e}")

		try:
			# 获取时间信息
			self._get_time()
		except Exception as e:
			# 捕获获取时间信息时的异常
			print(f"Error retrieving time info: {e}")

		# 处理可变参数和关键字参数
		try:
			if arg:
				msg = str(msg) + str(self._arg(arg=arg))
			if kwarg:
				msg = str(msg) + str(self._arg(arg=kwarg))
		except Exception as e:
			# 捕获参数处理中的异常
			print(f"Error processing arguments: {e}")

		# 创建错误消息
		self._create_msg(msg=msg, level="ERROR")

		# 构造输出消息
		try:
			base_message = self.colors.get("Red", "") + self.msg1 + self.reset_color
			if self.fileinfo and self.txt_mode:
				mess = self.colors.get("Red", "") + str(self.file_name) + ' <<-- ' + self.msg1 + self.reset_color
			else:
				mess = base_message

			# 根据日志级别决定是否输出到控制台
			if self.level_console <= 3:
				print(mess)

			# 根据日志级别决定是否写入文件
			if self.level_text <= 3:
				self._wr()
		except Exception as e:
			# 捕获消息构造和输出中的异常
			print(f"Error constructing or outputting message: {e}")


# 主程序入口，用于演示 ColorLogger 类的使用。
# 该代码块展示了如何实例化 ColorLogger 类并调用其方法记录日志。

if __name__ == "__main__":
	# 实例化 ColorLogger 类，设置日志记录的相关参数：
	# - fileinfo: 是否在日志中包含文件信息（布尔值）。
	# - basename: 是否仅显示文件的基本名称（布尔值）。
	# - txt: 是否将日志输出为纯文本格式（布尔值）。
	log = ColorLogger(fileinfo=True, basename=True, txt=True)

	# 记录一条 INFO 级别的日志，包含自定义消息和额外参数。
	log.info(msg='1', x="23")

	# 记录一条 ERROR 级别的日志，包含多个参数。
	log.error('2', '22', '222')

	# 设置日志的控制台输出级别为 INFO。
	log.set_level(console="INFO")

	# 记录一条 DEBUG 级别的日志，由于控制台级别设置为 INFO，该日志可能不会显示。
	log.debug('3', '21')

	# 记录一条 WARNING 级别的日志，包含字符串和数字参数。
	log.warning('4', '20', 22)
