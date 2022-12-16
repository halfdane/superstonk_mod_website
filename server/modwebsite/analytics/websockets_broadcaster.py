import asyncio
import logging
from typing import AsyncGenerator


class WebsocketsBroadcaster:
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.connections = dict()

    async def publish(self) -> None:
        self.logger.info(self.connections)
        for connection, state in self.connections.items():
            callback, args = state
            message = await callback(*args)
            await connection.put(message)

    async def subscribe(self, callback, *args) -> AsyncGenerator[str, None]:
        connection = asyncio.Queue()
        self.connections[connection] = (callback, args)
        try:
            while True:
                yield await connection.get()
        finally:
            self.logger.info("Cleaning up from connection broker")
            del self.connections[connection]
