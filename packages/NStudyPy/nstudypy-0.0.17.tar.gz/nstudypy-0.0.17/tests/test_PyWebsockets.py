#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025-03-18 11:09
# @Author  : Jack
# @File    : test_PyWebsockets

"""
test_PyWebsockets
"""
import asyncio
from NStudyPy import PyWebsockets
from NStudyPy.PyLogger import get_logger

logger = get_logger(__name__)


async def handle_service(websocket):
    logger.info("Client connected")
    try:
        async for message in websocket:
            logger.info(f"Received: {message}")
            response = f"Hello from server!"
            await websocket.send(response)
    except Exception as e:
        logger.error("Client exception:", repr(e))


if __name__ == '__main__':
    asyncio.run(PyWebsockets.start_server(handle_service, logger=logger))
