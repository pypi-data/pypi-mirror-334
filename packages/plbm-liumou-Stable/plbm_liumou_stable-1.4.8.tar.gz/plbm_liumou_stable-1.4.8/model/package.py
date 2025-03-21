# -*- encoding: utf-8 -*-
s='''
@File    :   Package.py
@Time    :   2022/04/13 18:45:40
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   包管理模块
'''
print(s)
from subprocess import getstatusoutput, getoutput
from os import getcwd, path, system, chdir
from sys import exit
from model.osinfo import OsInfo
from su import Jurisdiction
from network import NetworkTools

class PackageManager:
    def __init__(self, passwd):
        """_summary_
        包管理模块
        Args:
            passwd (str): 主机密码
        """
        self.passwd = passwd
        oi = OsInfo
        self.os_type = oi.os_type
        self.os_ver = oi.os_ver
        self.arch = oi.arch
        self.status = False
        # 本地已存在的包列表
        self.local_list = []
    def check(self):
        """_summary_
        开局先检查权限
        """
        up = Jurisdiction(passwd=self.passwd)
        if up.verification(name="PackageManager-check"):
            self.passwd = up.password
            self.status = True
        else:
            print("权限获取失败")
        return self.status
        
    def f(self):
        """_summary_
        修复依赖
        """
        c = "apt install -f"
        self.sudo(cmd=c)
        
    def configure(self):
        c = "dpkg --configure -a"
        self.sudo(cmd=c)
        

    
    def sudo(self, cmd, display=True):
        """_summary_
        执行超级命令
        Args:
            cmd (str): 需要执行的命令
        """
        c = str("echo % s | sudo -S %s" % (self.passwd, cmd))
        if display:
            c = str("echo % s | sudo -S %s;echo $? > s" % (self.passwd, cmd))
            system(c)
            status = getoutput('cat s')
            if str(status) == '0':
                return True
            print(c)
            return False
        else:
            status = getstatusoutput(c)
            if status[0] == 0:
                return True
        print(c)
        return False
    
    def uninstall(self, package = None):
        """_summary_
        卸载包
        Args:
            package (list, optional): 传入需要卸载的包名(非文件名). Defaults to [].
        """
        if package is None:
            package = []
        success = []
        fail = []
        skip = []
        if type(package) is not list:
            print("请通过列表传入需要卸载的包")
            return False

        if len(package) == 0:
            print("传入的数量不正确,跳过处理")
            return False
        self.configure()
        for pac in package:
            if self.installed(package=pac):
                print("正在卸载: " + pac)
                if self.sudo(cmd="dpkg -P %s" % pac):
                    print("卸载成功: " + pac)
                    success.append(pac)
                else:
                    print("卸载失败: " + pac)
                    fail.append(pac)
            else:
                print("跳过: 查询结果找不到包名: " + pac)
                print("请传入需要卸载的包全名,例如 vsftpd")
                skip.append(pac)
        print("处理结束...")
        print("卸载成功数量: ", len(success))
        print("卸载失败数量: ", len(fail))
        print("跳过处理数量: ", len(skip))
        return success, fail, skip

    def install_apt(self, package = None, server='baidu.com'):
        """_summary_
        通过APT安装包
        Args:
            package (list, optional): 需要安装的包名列表. Defaults to [].
            server (str, optional): 设置源服务器地址网络检测,默认使用baidu进行网络判断
        """
        if package is None:
            package = []
        success = []
        fail = []
        if type(package) is not list:
            print("请通过列表传入需要安装的包名")
            return False
        if len(package) == 0:
            print("传入的数量不正确,跳过处理")
            return False
        net = NetworkTools()
        if not net.pingstatus(server=server):
            print("测试服务器连接失败: " + server)
            return False
        self.configure()
        self.f()
        for i in package:
            c = str("apt install %s -y" % i)
            if self.sudo(cmd=c):
                success.append(i)
            else:
                fail.append(i)
        print("安装结束...")
        print("安装成功数量: ", len(success))
        print("安装失败数量: ", len(fail))
        return success, fail
           
    def install_debfile(self, file_list = None, work=getcwd()):
        """_summary_
        安装deb文件
        通过列表传入需要安装的文件路径,默认使用当前路径作为目录
        Args:
            file_list (list): 需要安装的文件列表
            work (str): 设置一个工作目录,默认当前目录
        """
        if file_list is None:
            file_list = []
        add_file = []
        skip_file = []
        skip_other = []
        chdir(work)
        file_ = ''
        if type(file_list) is not list:
            print("请通过列表传入需要安装的文件")
            return False
        if len(file_list) == 0:
            print("文件列表为空")
            return False
        for file in file_list:
            if path.isfile(file):
                if path.splitext(file)[-1].lower() == 'deb':
                    file_ = str(file_) + " " + str(file)
                    add_file.append(file)
                else:
                    print("跳过非安装包文件: ", file)
                    skip_file.append(file)
            else:
                print("跳过非文件: ", file)
                skip_other.append(file)
        print("添加文件数量: ", len(add_file))
        print("跳过文件数量: ", len(skip_file))
        print("跳过非文件数: ", len(skip_other))
        if int(add_file) == 0:
            return False
        c = str("dpkg -i %s" % file_)
        if self.sudo(cmd=c):
            print("全部安装成功")
            print(file_)
            return True, add_file, skip_file, skip_other
        else:
            print("全部/部分安装失败")
        return False, add_file, skip_file, skip_other

    def deepin_install_debfile(self, file_list = None, work=getcwd()):
        """_summary_
        使用图形化安装deb文件-UOS
        通过列表传入需要安装的文件路径,默认使用当前路径作为目录
        Args:
            file_list (list): 需要安装的文件列表
            work (str): 设置一个工作目录,默认当前目录
        """
        if str(self.os_type).lower() != 'uos' or str(self.os_type).lower() != 'deepin'.lower():
            print("仅限使用统信-UOS、深度-deepin系统使用")
            return False
        if file_list is None:
            file_list = []
        add_file = []
        skip_file = []
        skip_other = []
        chdir(work)
        file_ = ''
        if type(file_list) is not list:
            print("请通过列表传入需要安装的文件")
            return False
        if len(file_list) == 0:
            print("文件列表为空")
            return False
        for file in file_list:
            if path.isfile(file):
                if path.splitext(file)[-1].lower() == 'deb':
                    file_ = str(file_) + " " + str(file)
                    add_file.append(file)
                else:
                    print("跳过非安装包文件: ", file)
                    skip_file.append(file)
            else:
                print("跳过非文件: ", file)
                skip_other.append(file)
        print("添加文件数量: ", len(add_file))
        print("跳过文件数量: ", len(skip_file))
        print("跳过非文件数: ", len(skip_other))
        if int(add_file) == 0:
            return False
        c = str("deepin-deb-installer %s" % file_)
        if self.sudo(cmd=c):
            print("全部安装成功")
            print(file_)
            return True, add_file, skip_file, skip_other
        else:
            print("全部/部分安装失败")
        return False, add_file, skip_file, skip_other
    def dpkg_list(self, pac1, pac2=None):
        """_summary_
        获取本地已安装的软件包列表,可通过self.local_list实例变量获取结果
        Args:
            pac1 (str): 包关键词1
            pac2 (str, optional): 包关键词2. Defaults to None.
        """
        if pac1 is None:
            return False
        c = "dpkg -l | grep  %s | grep %s" % (pac1, pac2)
        if pac2 is None or str(pac2) == 'None':
            c = "dpkg -l | grep  %s" % pac1
        c = c + "| awk '{print $2}'"
        self.local_list = getoutput(c).split("\n")
        if len(self.local_list) == 0:
            return False
        return True
    
    def dpkg_installed(self, pac1, pac2=None):
        """_summary_    
        查询是否已安装这个包,模糊查询
        Args:
            package (str): 需要查询的包名称
        """
        return self.dpkg_list(pac1=pac1, pac2=pac2)
    
    def apt(self, key1, key2):
        """
		查询在线包
		:return:
		"""
        c = """apt search %s | grep %s | grep / | awk -F '/' '{print $1}' """ % (key1, key2)
        print("执行命令")
        print(c)
        status = getstatusoutput(c)
        if status[0] == 0:
            print("执行查询命令成功,正在检测结果")
            txt = status[1]
            txt = str(txt).replace("WARNING: apt does not have a stable CLI interface. Use with caution in scripts.", '')
            txt = str(txt).split("\n")
            result_dic = {}
            s = 1
            for i in txt:
                if len(i) >= 2:
                    print(s, ":", i)
                    result_dic[s] = i
                    self.pac_list.append(i)
                    s += 1
        else:
            print("无法完成在线查询,请检查网络或者源配置")
            return False
        return True