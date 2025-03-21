#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   Public6.py
@Time    :   2024-12-13 10:28
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
import platform
import re
import socket
import subprocess
from subprocess import getstatusoutput

from loguru import logger


def _socket_get_ipv6_public(show: bool, target_address: str = '2400:3200::1', target_port: int = 53):
	"""
	使用socket编程获取IPv6公网地址。

	参数:
	show (bool): 是否显示日志信息。
	target_address (str): 目标地址，默认为'2400:3200::1'。
	target_port (int): 目标端口，默认为53。

	返回:
	str: 成功时返回IPv6公网地址，失败时返回None。
	"""
	sock = None
	try:
		# 创建IPv6 UDP套接字
		sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
		# 尝试连接到目标地址和端口
		sock.connect((target_address, target_port))
		ip = sock.getsockname()[0]
		# 如果show为True，打印调试日志
		if show:
			logger.debug(f"当前IPv6公网地址是: {ip}")
		return ip
	except socket.error as e:
		# 捕获socket相关异常
		if show:
			logger.warning(f"通过socket请求的方式获取IPv6失败: {str(e)}", exc_info=True)
	except Exception as e:
		# 捕获其他异常
		if show:
			logger.error(f"发生未知错误: {str(e)}", exc_info=True)
	finally:
		# 确保套接字关闭
		if sock:
			sock.close()
	return None


def execute_command(command: str) -> (int, str, str):
	"""
	执行外部命令并返回状态码、标准输出和错误输出。
	"""
	try:
		result = subprocess.run(command, shell=True, text=True, capture_output=True)
		return result.returncode, result.stdout.strip(), result.stderr.strip()
	except Exception as e:
		logger.error(f"执行命令失败: {command}, 错误: {str(e)}")
		return -1, "", str(e)
def _linux_get_ipv6_public_ip_a(show: bool):
	"""
	获取Linux系统的IPv6公网地址。

	参数:
	show (bool): 是否显示IPv6地址的调试信息。

	返回:
	str: IPv6地址字符串，如果获取失败则返回None。
	"""

	# 检测是否存在ip命令
	status, _, stderr = execute_command("which ip")
	if status != 0:
		logger.warning(f"未检测到ip命令, 请自行安装... 错误信息: {stderr}")
		return None

	# 执行ip a命令获取IPv6地址信息
	status, output, stderr = execute_command(
		"ip a | grep inet6 | grep global | awk '{print $2}' | awk -F/ '{print $1}'"
	)
	if status == 0 and output:
		# 提取第一个IPv6地址
		ip_addresses = output.split("\n")
		if ip_addresses:
			ip = ip_addresses[0].strip()
			# 校验IPv6地址格式
			if re.match(r"^([0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{1,4}$", ip):
				if show:
					logger.debug(f"当前IPv6公网地址是: {ip}")
				return ip
			else:
				logger.warning(f"提取的IPv6地址格式无效: {ip}")
		else:
			logger.warning("未找到有效的IPv6地址...")
	else:
		logger.warning(f"通过 ip a 命令获取IPv6失败... 错误信息: {stderr}")
	return None



def _linux_get_ipv6_public_ifconfig(show: bool):
	"""
	使用ifconfig命令获取Linux系统的IPv6公网地址。

	参数:
	show (bool): 是否打印日志信息。

	返回:
	str: IPv6公网地址，如果获取失败则返回None。
	"""
	# 检测是否存在ifconfig命令
	res = getstatusoutput("which ifconfig")
	if res[0] != 0:
		# 如果没有找到ifconfig命令，记录警告日志并返回None
		logger.warning("未检测到ifconfig命令,请自行安装...")
		return None

	# 执行ifconfig命令并解析输出，提取IPv6地址
	res, txt = getstatusoutput("ifconfig  | grep inet6 | awk '{print $2}' | grep ^240")
	if res == 0:
		# 提取成功，根据show参数决定是否打印日志
		ip_ = txt.split("\n")[0].strip()
		if show:
			logger.debug(f"当前IPv6公网地址是: {ip_}")
		return ip_
	else:
		# 提取失败，记录警告日志
		logger.warning("通过 ifconfig 命令获取IPV6失败...")




def _windows_get_ipv6_public(show: bool) -> str | None:
	"""
	在Windows系统中获取公网IPv6地址。

	该函数通过执行ipconfig命令来获取系统的所有IP配置信息，然后从中寻找以240开头的IPv6地址，
	这通常是中国移动分配的公网IPv6地址。如果找到匹配的IPv6地址，函数会返回该地址；如果未找到，
	或者执行命令失败，则返回None。

	参数:
	show (bool): 一个布尔值，指示是否在找到IPv6地址时打印日志信息。
	如果为True，则打印, 如果为False，则不打印。

	返回:
	str: 找到的IPv6公网地址，如果没有找到或获取失败，则返回None。
	"""
	# 定义正则表达式，匹配以240开头的合法IPv6地址
	_IPV6_PATTERN = re.compile(r"240[0-9a-fA-F:]+")
	try:
		# 执行ipconfig /all命令获取IP配置信息
		res, txt = getstatusoutput("ipconfig")

		# 如果命令执行失败，记录警告日志并返回None
		if res != 0:
			logger.warning(f"通过 ipconfig 命令获取IPV6失败，返回码: {res}")
			return None

		# 检查ipconfig输出是否为空
		if not txt.strip():
			logger.warning("通过 ipconfig 命令获取的输出为空...")
			return None

		# 遍历每一行输出，寻找匹配的IPv6地址
		for line in txt.split("\n"):
			match = _IPV6_PATTERN.search(line)
			if match:
				# 找到匹配的IPv6地址
				ip_ = match.group(0).strip()
				# 如果show参数为True，打印当前IPv6公网地址的日志信息
				if show:
					logger.debug(f"当前IPv6公网地址是: {ip_}")
				# 返回找到的IPv6地址
				return ip_

		# 如果没有找到匹配的IPv6地址，记录警告日志并返回None
		logger.warning("通过ipconfig命令未找到IPV6公网地址...")
		return None

	except Exception as e:
		# 捕获异常并记录错误日志
		logger.error(f"执行 ipconfig 命令时发生异常: {e}")
		return None



def get_ipv6_public(show=False):
	"""
	获取本机的IPv6公共地址。

	本函数尝试通过多种方法获取本机的IPv6公共地址。首先，它尝试使用一个私有方法
	_socket_get_ipv6_public(show) 来获取地址。如果该方法失败，它将根据操作系统的类型
	使用特定的方法来获取IPv6地址。

	参数:
	show (bool): 一个可选的布尔参数，决定是否显示获取IPv6地址的过程信息。默认为False。

	返回:
	str: 本机的IPv6公共地址，如果无法获取，则返回None。
	"""
	# 记录获取IPv6公共地址的开始
	logger.debug("开始获取本机IPV6地址")

	# 尝试通过私有方法获取IPv6公共地址
	try:
		ipv6_public = _socket_get_ipv6_public(show)
		if ipv6_public:
			logger.debug(f"通过_socket_get_ipv6_public成功获取IPv6地址: {ipv6_public}")
			return ipv6_public
	except Exception as e:
		logger.warning(f"_socket_get_ipv6_public失败: {e}")

	# 根据操作系统类型选择合适的获取IPv6地址的方法
	os_name = platform.system()
	logger.debug(f"检测到操作系统: {os_name}")

	try:
		if os_name == "Linux":
			# 对于Linux系统，优先使用'ip a'命令，备选使用'ifconfig'
			ipv6_public = _linux_get_ipv6_public_ip_a(show)
			if ipv6_public:
				logger.debug(f"通过_linux_get_ipv6_public_ip_a成功获取IPv6地址: {ipv6_public}")
				return ipv6_public

			ipv6_public = _linux_get_ipv6_public_ifconfig(show)
			if ipv6_public:
				logger.debug(f"通过_linux_get_ipv6_public_ifconfig成功获取IPv6地址: {ipv6_public}")
				return ipv6_public
		elif os_name == "Windows":
			# 对于Windows系统，使用特定的Windows方法
			ipv6_public = _windows_get_ipv6_public(show)
			if ipv6_public:
				logger.debug(f"通过_windows_get_ipv6_public成功获取IPv6地址: {ipv6_public}")
				return ipv6_public
		else:
			logger.warning(f"未知操作系统: {os_name}，无法获取IPv6地址")
	except Exception as e:
		logger.error(f"获取IPv6地址时发生错误: {e}")

	# 如果所有方法均失败，返回None
	logger.debug("未能获取本机IPv6地址")
	return None



if __name__ == '__main__':
	print(get_ipv6_public(show=True))
