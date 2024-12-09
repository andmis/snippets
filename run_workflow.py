import sys
import asyncio

from get_client import get_client
from workflows import SandboxWorkflow


async def main():
    client = await get_client()
    use_sleep = "-s" in sys.argv
    use_wait = "-w" in sys.argv
    result = await client.execute_workflow(
        SandboxWorkflow.run,
        (use_sleep, use_wait),
        id="sandbox-workflow",
        task_queue="sandbox-queue",
    )
    print(f"Workflow result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
