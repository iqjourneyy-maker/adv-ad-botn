from telethon import TelegramClient
from telethon.sessions import StringSession

from telethon.errors import (
    SessionPasswordNeededError
)

from config import (
    API_ID,
    API_HASH
)

from database import (
    save_session,
    save_message,
    save_media,
    save_schedule
)

from scheduler import add_schedule

from states import user_state


async def handle_message(update, context):

    user_id = update.effective_user.id

    ################################
    # PHONE LOGIN
    ################################

    if user_state.get(user_id) == "PHONE":

        phone = update.message.text

        try:

            client = TelegramClient(
                StringSession(),
                API_ID,
                API_HASH
            )

            await client.connect()

            await client.send_code_request(
                phone
            )

            context.user_data["client"] = client

            user_state[user_id] = "OTP"

            await update.message.reply_text(
                "📩 Send OTP code"
            )

        except Exception as e:

            await update.message.reply_text(
                f"❌ Failed to send OTP\n{str(e)}"
            )

    ################################
    # OTP LOGIN
    ################################

    elif user_state.get(user_id) == "OTP":

        code = update.message.text

        client = context.user_data.get("client")

        try:

            await client.sign_in(code=code)

        except SessionPasswordNeededError:

            user_state[user_id] = "PASSWORD"

            await update.message.reply_text(
                "🔐 Send your 2FA password"
            )

            return

        except Exception as e:

            await update.message.reply_text(
                f"❌ Login failed\n{str(e)}"
            )

            return

        try:

            session = client.session.save()

            save_session(
                user_id,
                session
            )

            await client.disconnect()

            user_state[user_id] = None

            await update.message.reply_text(
                "✅ Account added successfully"
            )

        except Exception as e:

            await update.message.reply_text(
                f"❌ Session save failed\n{str(e)}"
            )

    ################################
    # PASSWORD LOGIN
    ################################

    elif user_state.get(user_id) == "PASSWORD":

        password = update.message.text

        client = context.user_data.get("client")

        try:

            await client.sign_in(
                password=password
            )

        except Exception as e:

            await update.message.reply_text(
                f"❌ Password incorrect\n{str(e)}"
            )

            return

        try:

            session = client.session.save()

            save_session(
                user_id,
                session
            )

            await client.disconnect()

            user_state[user_id] = None

            await update.message.reply_text(
                "✅ Account added successfully"
            )

        except Exception as e:

            await update.message.reply_text(
                f"❌ Session save failed\n{str(e)}"
            )

    ################################
    # SAVE MESSAGE
    ################################

    elif user_state.get(user_id) == "MESSAGE":

        try:

            message_text = update.message.text

            save_message(
                user_id,
                message_text
            )

            user_state[user_id] = None

            await update.message.reply_text(
                "✅ Message saved"
            )

        except Exception as e:

            await update.message.reply_text(
                f"❌ Failed to save message\n{str(e)}"
            )

    ################################
    # SAVE MEDIA
    ################################

    elif user_state.get(user_id) == "MEDIA":

        file_id = None

        try:

            if update.message.photo:

                file_id = update.message.photo[-1].file_id

            elif update.message.video:

                file_id = update.message.video.file_id

            elif update.message.document:

                file_id = update.message.document.file_id

            if file_id:

                save_media(
                    user_id,
                    file_id
                )

                user_state[user_id] = None

                await update.message.reply_text(
                    "✅ Media saved"
                )

            else:

                await update.message.reply_text(
                    "❌ Send photo/video/file"
                )

        except Exception as e:

            await update.message.reply_text(
                f"❌ Media save failed\n{str(e)}"
            )

    ################################
    # SCHEDULE INTERVAL
    ################################

    elif user_state.get(user_id) == "SCHEDULE":

        try:

            minutes = int(update.message.text)

            if minutes <= 0:

                await update.message.reply_text(
                    "❌ Send valid minutes (>0)"
                )

                return

            save_schedule(
                user_id,
                minutes
            )

            add_schedule(
                user_id,
                minutes,
                context
            )

            user_state[user_id] = None

            await update.message.reply_text(
                f"⏰ Auto broadcast every {minutes} minutes started"
            )

        except ValueError:

            await update.message.reply_text(
                "❌ Send number only"
            )

        except Exception as e:

            await update.message.reply_text(
                f"❌ Schedule failed\n{str(e)}"
            )