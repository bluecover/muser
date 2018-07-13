#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Facade(object):

    """ 全局变量集中营
    """

    config = None           # 配置信息
    code_stash = None       # 验证码临时存储器
    sms_provider = None     # 短信服务提供者
    oss_provider = None     # OSS 服务提供者
    redis_cli = None        # Redis 连接
