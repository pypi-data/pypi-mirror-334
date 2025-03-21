#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   __init__.py
@Time    :   2024-12-13 10:22
@Author  :   坐公交也用券
@Version :   1.0.1
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
from .Public4 import get_ipv4_public
from .Public6 import get_ipv6_public

__all__ = ['get_ipv4_public', 'get_ipv6_public']
