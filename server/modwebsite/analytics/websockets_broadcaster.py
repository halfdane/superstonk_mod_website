import asyncio
import json
import logging
import random
from typing import AsyncGenerator


class WebsocketsBroadcaster:
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.connections = dict()

    async def update(self, client_id, *args) -> None:
        state = self.connections[client_id]
        connection, callback, old_args = state
        state = (connection, callback, args)
        self.connections[client_id] = state
        self.logger.info(f"new connections: {self.connections}")
        await self._send_data_for_single_client(client_id, state)

    async def publish(self) -> None:
        self.logger.info([state for _, state in self.connections.items()])
        for client_id, state in self.connections.items():
            await self._send_data_for_single_client(client_id, state)

    async def _send_data_for_single_client(self, client_id, state):
        connection, callback, args = state
        data = await callback(*args)
        data['client_id'] = client_id
        await connection.put(json.dumps(data))

    async def subscribe(self, callback, *args) -> AsyncGenerator[str, None]:
        client_id = random.getrandbits(128).to_bytes(16, 'little').hex()
        connection = asyncio.Queue()
        state = (connection, callback, args)
        self.connections[client_id] = state
        try:
            yield json.dumps({'client_id': client_id})
            await self._send_data_for_single_client(client_id, state)
            while True:
                yield await connection.get()
        finally:
            self.logger.info("Cleaning up from connection broker")
            del self.connections[client_id]
