import asyncio
import datetime as dt

from temporalio import workflow
from temporalio.exceptions import ActivityError

with workflow.unsafe.imports_passed_through():
    from activities import sandbox_activity


@workflow.defn
class SandboxWorkflow:
    @workflow.run
    async def run(self, use_sleep: bool, use_wait: bool) -> None:
        print(f"{workflow.now()} (Workflow) Starting, use_sleep={use_sleep} use_wait={use_wait}")
        coro = workflow.start_activity(
            sandbox_activity,
            use_sleep,
            start_to_close_timeout=dt.timedelta(seconds=100),
            cancellation_type=(
                workflow.ActivityCancellationType.WAIT_CANCELLATION_COMPLETED
                if use_wait
                else workflow.ActivityCancellationType.TRY_CANCEL
            ),
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
