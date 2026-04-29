from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from force_join import check_force_join
from config import FORCE_CHANNEL


def main_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🔐 Login",
                callback_data="login"
            )
        ],

        [
            InlineKeyboardButton(
                "📝 Set Message",
                callback_data="setmsg"
            )
        ],

        [
            InlineKeyboardButton(
                "📎 Set Media",
                callback_data="setmedia"
            )
        ],

        [
            InlineKeyboardButton(
                "📢 Broadcast",
                callback_data="broadcast"
            )
        ],

        [
    InlineKeyboardButton(
        "❌ Remove Account",
        callback_data="remove_account"
           )
        ],

        [
    InlineKeyboardButton(
        "🛑 Cancel Broadcast",
        callback_data="cancel_broadcast"
    )
],

[
    InlineKeyboardButton(
        "📜 View Logs",
        callback_data="view_logs"
    )
],

        [
            InlineKeyboardButton(
                "⏰ Schedule Ads",
                callback_data="schedule"
            )
        ]

    ]

    return InlineKeyboardMarkup(keyboard)


async def start(update, context):

    user_id = update.effective_user.id

    if not await check_force_join(
        user_id,
        context
    ):

        keyboard = [

            [
                InlineKeyboardButton(
                    "Join The Main Channel",
                    url=f"https://t.me/{FORCE_CHANNEL[1:]}"
                )
            ]

        ]

        await update.message.reply_text(

            "Join Our Main Channel To Use The Bot",

            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

        return

    await update.message.reply_text(
        "Welcome To The Bot 🚀 The Most Advanced Telegram Ad Bot!",
        reply_markup=main_menu()
    )