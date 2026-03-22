import asyncio

# حل مشكلة Python 3.14
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, MessageHandler, filters, ContextTypes

API_ID = 37958812
API_HASH = "6708b877322843a5fdfbece240f2f3c7"
BOT_TOKEN = "8202025752:AAE3gqA5fXsvaIz9pzVXHv1ji3RbclFGsNs"

OWNER_ID = 6154260595

message_text = ""
target_chat = ""
running = False
mode = None

user_app = Client("my_session", api_id=API_ID, api_hash=API_HASH)

def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📩 حط الرسالة", callback_data="msg")],
        [InlineKeyboardButton("🎯 حط الايدي", callback_data="chat")],
        [InlineKeyboardButton("🚀 تشغيل", callback_data="run")],
        [InlineKeyboardButton("🛑 إيقاف", callback_data="stop")]
    ])

async def sender():
    global running

    await user_app.start()
    print("✅ الحساب جاهز")

    while True:
        if running and message_text and target_chat:
            try:
                await user_app.send_message(target_chat, message_text)
                print("📤 تم الإرسال")
            except Exception as e:
                print("❌", e)

            await asyncio.sleep(25)
        else:
            await asyncio.sleep(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    await update.message.reply_text("🔥 تحكم بالبوت", reply_markup=menu())

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running, mode

    query = update.callback_query
    await query.answer()

    if query.from_user.id != OWNER_ID:
        return

    if query.data == "msg":
        mode = "msg"
        await query.message.reply_text("✍️ أرسل الرسالة")

    elif query.data == "chat":
        mode = "chat"
        await query.message.reply_text("📌 أرسل ID القروب")

    elif query.data == "run":
        running = True
        await query.message.reply_text("🚀 بدأ الإرسال")

    elif query.data == "stop":
        running = False
        await query.message.reply_text("🛑 توقف")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global message_text, target_chat, mode

    if update.effective_user.id != OWNER_ID:
        return

    if mode == "msg":
        message_text = update.message.text
        mode = None
        await update.message.reply_text("✅ تم حفظ الرسالة")

    elif mode == "chat":
        target_chat = int(update.message.text)
        mode = None
        await update.message.reply_text("✅ تم حفظ الايدي")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.COMMAND, start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("✅ البوت شغال...")

    # تشغيل المرسل بالخلفية
    asyncio.create_task(sender())

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
