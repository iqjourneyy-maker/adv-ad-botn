from states import user_state

from broadcaster import (
    start_broadcast,
    cancel_broadcast
)

from scheduler import (
    add_schedule,
    remove_schedule
)

from database import (
    remove_account,
    get_logs
)

import asyncio


async def buttons(update, context):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # LOGIN
    if query.data == "login":

        user_state[user_id] = "PHONE"

        await query.message.reply_text(
            "Send phone number"
        )

    # SET MESSAGE
    elif query.data == "setmsg":

        user_state[user_id] = "MESSAGE"

        await query.message.reply_text(
            "Send message text"
        )

    # SET MEDIA
    elif query.data == "setmedia":

        user_state[user_id] = "MEDIA"

        await query.message.reply_text(
            "Send photo/video/file"
        )

    # START BROADCAST
    elif query.data == "broadcast":

        await query.message.reply_text(
            "🚀 Broadcast started"
        )

        asyncio.create_task(
            start_broadcast(
                user_id,
                context
            )
        )

    # SCHEDULE ADS
    elif query.data == "schedule":

        user_state[user_id] = "SCHEDULE"

        await query.message.reply_text(
            "Send time in minutes\nExample: 60"
        )

    # STOP SCHEDULE
    elif query.data == "stop_schedule":

        remove_schedule(user_id)

        await query.message.reply_text(
            "🛑 Schedule stopped"
        )

    # REMOVE ACCOUNT
    elif query.data == "remove_account":

        remove_account(user_id)

        remove_schedule(user_id)

        await query.message.reply_text(
            "❌ Account removed successfully"
        )

    # CANCEL BROADCAST
    elif query.data == "cancel_broadcast":

        cancel_broadcast(user_id)

        await query.message.reply_text(
            "🛑 Broadcast stopping..."
        )

    # VIEW LOGS
    elif query.data == "view_logs":

        logs = get_logs(user_id)

        if not logs:

            await query.message.reply_text(
                "No logs found"
            )

            return

        text = "📜 Last Broadcast Logs:\n\n"

        for log in logs:

            total, sent, failed, start, end = log

            text += (
                f"Total: {total}\n"
                f"Sent: {sent}\n"
                f"Failed: {failed}\n"
                f"Start: {start}\n"
                f"End: {end}\n\n"
            )

        await query.message.reply_text(text)