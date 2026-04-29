from config import ADMIN_ID
from database import get_all_users


async def admin_broadcast(
    update,
    context
):

    if update.effective_user.id != ADMIN_ID:
        return

    msg = " ".join(context.args)

    users = get_all_users()

    sent = 0

    for user in users:

        try:

            await context.bot.send_message(
                user[0],
                msg
            )

            sent += 1

        except:
            pass

    await update.message.reply_text(
        f"Sent to {sent} users"
    )