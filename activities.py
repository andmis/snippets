import asyncio
import datetime as dt
import random

from temporalio import activity


@activity.defn
async def sandbox_activity(n: int) -> None:
    try:
        print(f"{dt.datetime.now()} (Activity {n}) Running sandbox_activity")
        await asyncio.sleep(random.uniform(1, 10))

        if not activity.info().is_local:
            # Check for cancellation. This doesn't seem to work correctly
            # without the sleep.
            activity.heartbeat()
            await asyncio.sleep(0.1)

        print(f"{dt.datetime.now()} (Activity {n}) Exiting sandbox_activity")
    except asyncio.CancelledError:
        print(f"{dt.datetime.now()} (Activity {n}) Cancelling sandbox_activity")
        raise
