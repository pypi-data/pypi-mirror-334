#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   __init__.py
@Time    :   2022-10-24 00:20
@Author  :   坐公交也用券
@Version :   1.4.8
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   这是一个Linux管理脚本的基础库，通过对Linux基本功能进行封装，实现快速开发的效果
"""

# 导入本项目自定义的模块
from .Apt import NewApt
from .Cmd import NewCommand
from .Dpkg import NewDpkg
from .Iptables import IpTables
from .Jurisdiction import Jurisdiction
from .File import NewFile
from .NetStatus import NewNetStatus, NewNetworkCardInfo
from .Nmcli import NewNmcli
from .OsInfo import *
from .OsInfo import OsInfo
from .Package import NewPackage
from .Service import NewService
from .Yum import NewYum
from .base import list_get_len, list_remove_none
from .get import headers, cookies
from .logger import ColorLogger
from .LISTEN import NewListen
from .Process import NewProcess

# 定义模块的导出列表，方便外部调用
__all__ = ["NewCommand", "NewApt", "NewDpkg", "NewFile", "Jurisdiction",
           "NewNmcli", "NewNetStatus", "NewPackage", "NewService", "NewYum",
           "IpTables", "OsInfo", "NewNetworkCardInfo", "list_get_len", "list_remove_none",
           "ColorLogger", "NewListen", "NewProcess"]

# 检查当前运行环境是否为Linux系统
if platform.system().lower() != 'linux'.lower():
    print('Plmb模块仅支持Linux系统')
