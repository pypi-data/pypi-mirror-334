# -*- encoding: utf-8 -*-
"""
@File    :   Public4.py
@Time    :   2024-12-13 10:23
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   获取当前主机的公网IP地址
"""
import requests
from requests import get
from loguru import logger


def get_ipv4_public(show=False):
	"""
	获取当前主机所在网络的公网地址

	:param show: 是否打印出获取到的公网IP地址，默认为False
	:return: 返回获取到的公网IP地址字符串，如果获取失败则返回None
	"""
	# 定义API地址列表，便于维护和扩展
	api_urls = [
		"https://checkip.amazonaws.com",
		"http://icanhazip.com",
		"http://ip.liumou.site/api"
	]

	# 遍历API地址列表，尝试获取公网IP
	for url in api_urls:
		try:
			# 设置超时时间为5秒，避免请求长时间挂起
			req = get(url, timeout=5)
			if req.status_code == 200:
				ip = req.text.strip()  # 统一去除多余字符
				if show:
					logger.info(f"当前公网IP: {ip} (来源: {url})")
				return ip
		except requests.exceptions.RequestException as e:
			# 捕获具体的异常类型，并记录详细日志
			logger.warning(f"访问API失败: {url}, 错误信息: {e}")
		except Exception as e:
			# 捕获其他未知异常
			logger.error(f"发生未知错误: {e}")

	# 如果所有API都失败，返回None
	return None



if __name__ == "__main__":
	get_ipv4_public(show=True)
