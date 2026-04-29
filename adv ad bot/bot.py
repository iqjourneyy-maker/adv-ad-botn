from telegram.ext import (

    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters

)

from config import BOT_TOKEN

from handlers.start import start
from handlers.buttons import buttons
from handlers.messages import handle_message
from handlers.admin import admin_broadcast

from scheduler import start_scheduler


async def on_startup(app):

    # Start scheduler after loop starts
    start_scheduler()

    print("✅ Scheduler Started")


app = ApplicationBuilder()\
    .token(BOT_TOKEN)\
    .post_init(on_startup)\
    .build()


app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler(
        "broadcast",
        admin_broadcast
    )
)

app.add_handler(
    CallbackQueryHandler(buttons)
)

app.add_handler(
    MessageHandler(
        filters.ALL,
        handle_message
    )
)


print("🚀 Advanced Bot Running...")


app.run_polling()