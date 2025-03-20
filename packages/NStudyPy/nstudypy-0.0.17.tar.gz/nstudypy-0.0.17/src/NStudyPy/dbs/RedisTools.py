#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-07-11 13:54
# @Author  : Jack
# @File    : RedisTools

"""
RedisTools
"""
from __future__ import annotations

import redis
from typing import Optional
from datetime import datetime
from NStudyPy import PyEnv


class RedisTools:
    """
    RedisTools 工具类
    """

    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0, username: Optional[str] = None, password: Optional[str] = None):
        """
        初始化 RedisTools 实例
        :param host: Redis 服务器地址
        :param port: Redis 服务器端口
        :param db: Redis 数据库编号
        :param username: Redis 用户名（如果需要）
        :param password: Redis 密码（如果需要）
        """
        self.host = PyEnv.get_env("redis_host", host)
        self.port = PyEnv.get_env("redis_port", port)
        self.db = PyEnv.get_env("redis_db", db)
        self.username = PyEnv.get_env("redis_username", username)
        self.password = PyEnv.get_env("redis_password", password)
        self.client = None

    def __enter__(self):
        """
        上下文管理器进入方法
        :return: RedisTools 实例
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        上下文管理器退出方法，关闭 Redis 连接
        """
        self.close()

    def connect(self):
        """
        建立与 Redis 服务器的连接
        """
        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            username=self.username,
            password=self.password
        )

    def close(self):
        """
        关闭与 Redis 服务器的连接
        """
        if self.client:
            self.client.close()
            self.client = None

    def set_string(self, key: str, value: str, expire: Optional[int] = None) -> bool:
        """
        将字符串值存储到 Redis
        :param key: 键
        :param value: 值
        :param expire: 过期时间，单位为秒
        :return: 操作是否成功
        """
        if self.client:
            return self.client.set(name=key, value=value, ex=expire)
        raise ConnectionError("Redis client is not connected")

    def get_string(self, key: str) -> Optional[str]:
        """
        从 Redis 中获取字符串值
        :param key: 键
        :return: 对应的值，如果键不存在则返回 None
        """
        if self.client:
            value = self.client.get(name=key)
            return value.decode('utf-8') if value else None
        raise ConnectionError("Redis client is not connected")
