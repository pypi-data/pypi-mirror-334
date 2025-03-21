# -*- encoding: utf-8 -*-
from model.cmd import Cmd
from model.apt import Apt
from os import path
from loguru import logger

class Docker:
	def __init__(self, passwd, debug=False):
		"""

		:param passwd:
		"""
		self.manger = 'apt'
		self.cmd = Cmd(passwd=passwd, debug=debug)
		self.apt = Apt(passwd, debug)
		self.home = self.cmd.home
		if self.cmd.shell(command='which yum'):
			self.manger = 'yum'
	
	def check(self):
		if self.manger.lower() == 'apt':
			cmd = "dpkg -l | grep docker.io"
			if self.cmd.shell(command=cmd):
				logger.debug("Docker Is Installed")
				return False
			else:
				return True
	
	def restart(self):
		self.cmd.sudo(cmd="systemctl daemon-reload", name='daemon-reload')
		self.cmd.sudo(cmd="systemctl restart docker", name='restart')
	
	def config(self):
		"""

		:return:
		"""
		txt = """{
	"registry-mirrors": ["https://mirror.ccs.tencentyun.com"]
}
"""
		dir_ = '/etc/docker/'
		self.cmd.sudo(cmd="mkdir -p %s" % dir_, name='Mkdir')
		file = path.join(dir_, 'daemon.json')
		file_tmp = path.join(self.home, 'daemon.json')
		if path.isdir(dir_):
			w = open(file=file_tmp, mode='w+', encoding='utf8')
			try:
				w.write(txt)
			finally:
				w.close()
			cmd = "cp %s %s" % (file_tmp, file)
			self.cmd.sudo(cmd=cmd, name=cmd)
	
	def install(self):
		"""

		:return:
		"""
		self.apt.install(pac='docker.io')
	
	def start(self):
		"""

		:return:
		"""
		if self.check():
			self.install()
		self.config()
		self.restart()
