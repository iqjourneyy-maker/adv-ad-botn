import asyncio
import datetime

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError

from config import (
    API_ID,
    API_HASH,
    RATE_DELAY
)

from database import (
    get_user_data,
    save_log
)

# Store cancel flags
cancel_flags = {}


def cancel_broadcast(user_id):

    cancel_flags[user_id] = True


async def start_broadcast(
    user_id,
    context
):

    cancel_flags[user_id] = False

    data = get_user_data(user_id)

    if not data:
        return

    session, message, media = data

    client = TelegramClient(
        StringSession(session),
        API_ID,
        API_HASH
    )

    await client.start()

    dialogs = []

    async for dialog in client.iter_dialogs():
        dialogs.append(dialog)

    total = len(dialogs)

    sent = 0
    failed = 0

    start_time = datetime.datetime.now()

    for dialog in dialogs:

        # Check cancel
        if cancel_flags.get(user_id):

            await context.bot.send_message(
                user_id,
                "🛑 Broadcast Cancelled"
            )

            break

        try:

            if media:

                await client.send_file(
                    dialog.id,
                    media,
                    caption=message
                )

            else:

                await client.send_message(
                    dialog.id,
                    message
                )

            sent += 1

            if sent % 10 == 0:

                await context.bot.send_message(
                    user_id,
                    f"Progress: {sent}/{total}"
                )

            await asyncio.sleep(
                RATE_DELAY
            )

        except FloodWaitError as e:

            await asyncio.sleep(
                e.seconds
            )

        except:

            failed += 1

    await client.disconnect()

    end_time = datetime.datetime.now()

    # Save log
    save_log(
        user_id,
        total,
        sent,
        failed,
        str(start_time),
        str(end_time)
    )

    await context.bot.send_message(
        user_id,
        "✅ Broadcast Finished"
    )