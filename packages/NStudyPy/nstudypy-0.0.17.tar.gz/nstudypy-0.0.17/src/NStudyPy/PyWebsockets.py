#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025-03-18 11:00
# @Author  : Jack
# @File    : PyWebsockets

"""
PyWebsockets
"""
import websockets


async def start_server(handler, host: str = "127.0.0.1", port: int = 56655, logger=None):
    """
    start websocket server
    :param handler:
    :param host:
    :param port:
    :param logger:
    :return:
    """
    server = await websockets.serve(handler, host, port, logger=logger)
    if server and logger:
        logger.info("start websocket server at {}:{}".format(host, port))
    await server.wait_closed()
