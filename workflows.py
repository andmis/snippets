import asyncio
import datetime as dt

from temporalio import workflow
from temporalio.exceptions import ActivityError

with workflow.unsafe.imports_passed_through():
    from activities import sandbox_activity


@workflow.defn
class SandboxWorkflow:
    @workflow.run
    async def run(self, use_sleep: bool) -> None:
        print(f"{workflow.now()} (Workflow) Starting, use_sleep={use_sleep}")
        coro = workflow.start_activity(
            sandbox_activity,
            use_sleep,
            start_to_close_timeout=dt.timedelta(seconds=100),
        )
        await asyncio.sleep(1)  # Give the activity a chance to start.
        print(f"{workflow.now()} (Workflow) Cancelling activity")
        coro.cancel()

        # Try to cleanly wait for the activity to be cancelled.
        try:
            await coro
        except ActivityError:
            print(f"{workflow.now()} (Workflow) Activity cancelled")

        print(f"{workflow.now()} (Workflow) Exiting")
