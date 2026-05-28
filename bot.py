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

logging.basicConfig(level=logging.INFO)

messages = defaultdict(list)

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.chat_member.new_chat_member.user

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=WELCOME_TEXT.format(name=user.first_name)
        )
    except:
        pass

async def spam_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        user_id = update.message.from_user.id

        messages[user_id].append(text)

        if messages[user_id].count(text) >= 3:
            await update.message.delete()

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⚠️ 동일한 글 반복으로 삭제되었습니다."
            )
    except:
        pass

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
        spam_check
    )
)

print("봇 실행중...")

app.run_polling()
