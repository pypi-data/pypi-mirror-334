# -*- encoding: utf-8 -*-
"""
@File    :   pacman.py
@Time    :   2022-09-05 09:17
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
from model.cmd import Cmd


class Apt:
    def __init__(self, passwd, debug=False):
        """
        Apt Manger
        :param passwd:
        """
        self.passwd = passwd
        self.cmd = Cmd(passwd=passwd, debug=debug)

    def install(self, pac='git'):
        """

        :param pac:
        :return:
        """
        print("Installing %s ..." % pac)
        cmd = str("pacman -Sy %s" % pac)
        return self.cmd.sudo(cmd=cmd, name='Install %s' % pac)

    def update(self):
        """

        :return:
        """
        return self.cmd.sudo(cmd="apt update", name="Update Sources")

    def local(self, file):
        """

        :param file:
        :return:
        """
        return self.cmd.sudo(cmd="apt install -y -f %s" % file, name='Install Local Package')