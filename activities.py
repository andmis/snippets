import asyncio
import datetime as dt
import random

from temporalio import activity


@activity.defn
async def sandbox_activity(use_sleep: bool) -> None:
    try:
        print(f"{dt.datetime.now()} (Activity) Running sandbox_activity")
        await asyncio.sleep(random.uniform(5, 10))
        activity.heartbeat()
        if use_sleep:
            await asyncio.sleep(0.1)
        print(f"{dt.datetime.now()} (Activity) Completing sandbox_activity")
    except asyncio.CancelledError:
        print(f"{dt.datetime.now()} (Activity) Cancelling sandbox_activity")
        raise
