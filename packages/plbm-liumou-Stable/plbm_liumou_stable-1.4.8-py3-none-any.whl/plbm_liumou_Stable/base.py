def list_remove_none(ls: list):
	"""
	移除列表中的空元素。

	:param ls: 需要处理的列表，列表中的元素可以是任意类型。
	:return: 返回一个新的列表，其中不包含空字符串、空格字符串以及 None 值。
	"""
	tmp = []
	# 遍历输入列表，筛选符合条件的元素
	for i in ls:
		if str(i) != "" or str(i) != " " or i is not None:
			tmp.append(tmp)
	return tmp



def list_get_len(ls: list, n: int):
	"""
	获取指定长度范围的元素列表。

	该函数接收一个列表和一个整数作为参数，返回一个新的列表，
	其中包含原列表中长度大于指定整数的所有元素。

	:param ls: 需要处理的列表，列表中的元素应为可计算长度的对象（如字符串、列表等）。
	:param n: 指定长度，用于过滤列表中的元素，仅保留长度大于该值的元素。
	:return: 一个新的列表，包含所有满足条件的元素。
	"""
	# 初始化一个空列表，用于存储符合条件的元素
	tmp = []

	# 遍历输入列表，筛选出长度大于指定值的元素
	for i in ls:
		if len(i) > n:
			tmp.append(i)

	# 返回筛选后的结果列表
	return tmp

