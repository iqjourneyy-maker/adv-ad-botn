from config import FORCE_CHANNEL

async def check_force_join(
    user_id,
    context
):

    try:

        member = await context.bot.get_chat_member(
            FORCE_CHANNEL,
            user_id
        )

        return member.status in [
            "member",
            "administrator",
            "creator"
        ]

    except:
        return False