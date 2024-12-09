import asyncio
import datetime as dt

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import sandbox_activity


@workflow.defn
class SandboxWorkflow:
    @workflow.run
    async def run(self, local: bool) -> None:
        print(f"{workflow.now()} (Workflow) Starting, local={local}")
        coros = [
            (workflow.start_local_activity if local else workflow.start_activity)(
                sandbox_activity,
                n,
                start_to_close_timeout=dt.timedelta(seconds=100),
                cancellation_type=workflow.ActivityCancellationType.WAIT_CANCELLATION_COMPLETED,
            )
            for n in range(2)
        ]
        tasks = [coro for coro in coros]
        print(f"{workflow.now()} (Workflow) Waiting for first completed activity")
        await workflow.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        print(f"{workflow.now()} (Workflow) Got first completed activity, cancelling others and exiting")
        for coro in coros:
            coro.cancel()
        print(f"{workflow.now()} (Workflow) Exiting")
