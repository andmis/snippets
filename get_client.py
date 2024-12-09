import asyncio

from temporalio.client import Client

CLIENTS = {}


async def get_client() -> Client:
    loop = asyncio.get_event_loop()
    if loop not in CLIENTS:
        CLIENTS[loop] = await Client.connect("localhost:7233", namespace="default")
    return CLIENTS[loop]
