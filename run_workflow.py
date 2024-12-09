import sys
import asyncio

from get_client import get_client
from workflows import SandboxWorkflow


async def main():
    client = await get_client()
    use_sleep = sys.argv[-1] == "-s"
    result = await client.execute_workflow(
        SandboxWorkflow.run,
        use_sleep,
        id="sandbox-workflow",
        task_queue="sandbox-queue",
    )
    print(f"Workflow result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
