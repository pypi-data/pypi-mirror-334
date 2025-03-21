# -*- encoding: utf-8 -*-
# 定义一个包含多个键值对的字典，用于存储模拟的浏览器Cookie信息。
# 该字典可以用于模拟HTTP请求中的Cookie数据，通常用于网络爬虫或测试环境。
#
# 字典中的每个键表示Cookie的名称，值表示对应的Cookie值。
# 这些Cookie可能包含用户的身份信息、会话状态、偏好设置等。
cookies = {
    'BIDUPSID': '2C38F3EB848A082341E751BAED2BC2FA',  # 用户的唯一标识符
    'PSTM': '1666017860',  # 时间戳，可能表示用户的登录时间
    'BAIDUID': '2C38F3EB848A08231F2FC958AC261F79:FG=1',  # 百度用户ID，可能用于跟踪用户行为
    'BD_UPN': '12314753',  # 可能与用户的账户或会话相关
    'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',  # 可能是加密的会话信息
    'BA_HECTOR': '0500ag0l8g25012g8ga126qc1hl2ppb1a',  # 可能用于标识特定的会话或设备
    'BAIDUID_BFESS': '2C38F3EB848A08231F2FC958AC261F79:FG=1',  # 类似于BAIDUID，可能是备用字段
    'ZFY': 'TBZVN1ED8yM4eAQ6wGGPTH0OPaPbyZNmeHwz4jpsubs:C',  # 可能是某种加密或编码的数据
    'baikeVisitId': '43179892-7680-40af-bae0-3b55f1a3f5b3',  # 可能用于跟踪用户访问百科页面的行为
    'delPer': '0',  # 可能表示删除权限或某种状态标志
    'BD_CK_SAM': '1',  # 可能是某种采样标志或开关
    'PSINO': '7',  # 可能与用户的地理位置或服务区域相关
    'H_PS_PSSID': '36561_37584_36884_37486_36807_36786_37532_37497_26350_37371',  # 可能是会话ID集合
    'H_PS_645EC': '1fc3CbZpKIDdoSN7Wm7Y7GUGosO8XkKSTTstqL9QT0fa7oTkNcJPtdIQMqM',  # 可能是加密的会话信息
    'BDSVRTM': '0',  # 可能与服务器响应时间或状态相关
}


# 定义一个包含HTTP请求头的字典
# 该字典用于模拟浏览器发送HTTP请求时的头部信息，通常用于爬虫或API请求中。
#
# 参数说明：
# 无参数，这是一个直接定义的字典对象。
#
# 返回值：
# 无返回值，这是一个字典对象，直接定义并赋值给变量headers。

headers = {
    'Connection': 'keep-alive',  # 保持连接以复用TCP连接
    'Cache-Control': 'max-age=0',  # 禁用缓存，确保获取最新数据
    'sec-ch-ua': '";Not A Brand";v="99", "Chromium";v="10"',  # 客户端用户代理的品牌和版本信息
    'sec-ch-ua-mobile': '?0',  # 表示设备是否为移动设备（?0表示非移动设备）
    'sec-ch-ua-platform': '"Linux"',  # 表示操作系统平台
    'Upgrade-Insecure-Requests': '1',  # 请求将不安全的HTTP升级为HTTPS
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',  # 模拟浏览器的用户代理字符串
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',  # 定义客户端可接受的内容类型及优先级
    'Sec-Fetch-Site': 'none',  # 表示请求的来源站点（none表示跨站请求）
    'Sec-Fetch-Mode': 'navigate',  # 表示请求的模式（navigate表示导航请求）
    'Sec-Fetch-User': '?1',  # 表示请求是否由用户触发（?1表示是）
    'Sec-Fetch-Dest': 'document',  # 表示请求的目标资源类型（document表示HTML文档）
    'Accept-Language': 'zh-CN,zh;q=0.9',  # 定义客户端支持的语言及优先级
}
