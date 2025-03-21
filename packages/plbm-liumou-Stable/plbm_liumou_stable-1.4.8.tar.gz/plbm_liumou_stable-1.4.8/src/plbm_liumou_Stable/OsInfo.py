# -*- encoding: utf-8 -*-
import os
import platform
from typing import NoReturn

from .logger import ColorLogger


class OsInfo:
    def __init__(self):
        self.logger = ColorLogger()
        self._detect_platform()

    def _detect_platform(self) -> None:
        """统一处理平台检测逻辑"""
        system = platform.system().lower()
        self.os_arch = platform.machine()
        self.os_release = platform.release()

        if system == 'linux':
            self._detect_linux_info()
        else:
            self._detect_windows_info()

    def _detect_linux_info(self) -> None:
        """处理Linux系统信息检测"""
        try:
            self.home_dir = os.getenv("HOME", "")
            self.username = os.getenv("USER", "")
            self.uid = os.getuid()

            # 使用标准库获取发行版信息
            os_release = platform.freedesktop_os_release()
            self.os_type = os_release.get('ID', 'linux')
            self.os_ver = os_release.get('VERSION_ID', '')

            # 麒麟系统特殊处理
            if self.os_type.lower() == 'kylin':
                self._detect_kylin_version()

        except (OSError, KeyError) as e:
            self.logger.error(f"Error detecting Linux info: {str(e)}")
            self._set_defaults()

    def _detect_kylin_version(self) -> None:
        """处理麒麟系统版本检测"""
        try:
            with open('/etc/kylin-build', 'r') as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    self.os_ver = lines[1].strip().split()[1]
        except (FileNotFoundError, IndexError) as e:
            self.logger.warning(f"Kylin version detection failed: {str(e)}")

    def _detect_windows_info(self) -> None:
        """处理Windows系统信息检测"""
        self.os_type = 'Windows'
        self.home_dir = os.getenv("USERPROFILE", "")
        self.username = os.getenv("USERNAME", "")
        self.uid = os.getuid()  # Windows返回-1但保持类型一致
        self.os_ver = platform.release()

    def _set_defaults(self) -> None:
        """设置默认值"""
        self.os_type = 'Unknown'
        self.os_ver = ''
        self.home_dir = ''
        self.username = ''
        self.uid = -1

    def show(self) -> NoReturn:
        """显示系统信息"""
        info_items = [
            ("系统类型", self.os_type),
            ("系统版本", self.os_ver),
            ("系统架构", self.os_arch),
            ("release", self.os_release),
            ("登录用户", self.username),
            ("用户目录", self.home_dir),
            ("用户ID", self.uid)
        ]

        for label, value in info_items:
            self.logger.info(f"{label}: {value}")

if __name__ == '__main__':
    os_info = OsInfo()
    os_info.show()