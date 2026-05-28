import logging
from collections import defaultdict
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ChatMemberHandler,
    ContextTypes,
    filters,
)

TOKEN = "8835471195:AAGG_9uNfZosE1Ah9_ZmcZuRySE_QdCCXxQ"

WELCOME_TEXT = """
🎉 {name} 님 환영합니다 🎉

♛ BLACK CROWN 자유홍보방 ♛

📌 하루 홍보 가능 횟수 : 3회
📌 동일 도배 / 반복홍보 금지
📌 과도한 홍보 시 자동 삭제됩니다

즐거운 활동 되시길 바랍니다 👑
"""

WELCOME_IMAGE = "https://i.imgur.com/4M34hi2.png"

user_ads = defaultdict(list)
user_messages = defaultdict(list)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member

    if result.new_chat_member.status in ["member", "restricted"]:
        user = result.new_chat_member.user

        try:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=WELCOME_IMAGE,
                caption=WELCOME_TEXT.format(name=user.first_name)
            )
        except Exception as e:
            print(e)

async def check_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_id = update.message.from_user.id
    text = update.message.text.strip()

    user_messages[user_id].append(text)

    same_count = user_messages[user_id].count(text)

    if same_count >= 3:
        try:
            await update.message.delete()

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"⚠️ {update.message.from_user.first_name} 님 동일한 글 반복으로 삭제되었습니다."
            )

        except Exception as e:
            print(e)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        ChatMemberHandler(
            welcome,
            ChatMemberHandler.CHAT_MEMBER
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            check_spam
        )
    )

    print("봇 실행중...")

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
