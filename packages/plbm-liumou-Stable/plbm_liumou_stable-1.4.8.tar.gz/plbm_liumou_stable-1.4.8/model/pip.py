# -*- encoding: utf-8 -*-
from model.cmd import Cmd


class Pip:
    def __init__(self, debug=False):
        self.url = 'https://pypi.tuna.tsinghua.edu.cn/simple'
        self.pac_list = "pandas requests pymysql nuitka piper xlrd loguru pyinstaller".split(" ")
        self.cmd = Cmd("1", debug=debug)

    def config(self):
        cmd = "pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple"
        self.cmd.shell(command=cmd, name='Configure Image Source')

    def install(self):
        """

        :return:
        """
        for i in self.pac_list:
            self.cmd.shell(command="pip3 install %s" % i, name="Pip Installing %s" % i)

    def update(self):
        self.cmd.shell(command="python3 -m pip install --upgrade pip", name='Upgrade pip')
