import asyncio

from temporalio.worker import Worker

from activities import sandbox_activity
from get_client import get_client
from workflows import SandboxWorkflow


async def main():
    client = await get_client()
    worker = Worker(
        client,
        task_queue="sandbox-queue",
        workflows=[
            SandboxWorkflow,
        ],
        activities=[
            sandbox_activity,
        ],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
