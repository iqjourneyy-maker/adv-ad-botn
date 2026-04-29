from apscheduler.schedulers.asyncio import AsyncIOScheduler

from broadcaster import start_broadcast

scheduler = AsyncIOScheduler()

user_jobs = {}


def start_scheduler():

    scheduler.start()


def add_schedule(
    user_id,
    minutes,
    context
):

    seconds = minutes * 60

    # Remove old schedule if exists

    if user_id in user_jobs:

        user_jobs[user_id].remove()

    job = scheduler.add_job(

        start_broadcast,

        "interval",

        seconds=seconds,

        args=[user_id, context]

    )

    user_jobs[user_id] = job


def remove_schedule(user_id):

    if user_id in user_jobs:

        user_jobs[user_id].remove()

        del user_jobs[user_id]