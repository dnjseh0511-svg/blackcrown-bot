from collections import defaultdict
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = "8835471195:AAGG_9uNfZosE1Ah9_ZmcZuRySE_QdCCXxQ"

WELCOME_TEXT = """
🎉 환영합니다 🎉

♛ BLACK CROWN 자유홍보방 ♛

📌 하루 홍보 가능 횟수 : 3회
📌 동일 도배 / 반복홍보 금지
📌 과도한 홍보 시 자동 삭제됩니다
"""

messages = defaultdict(list)

async def spam_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text
    user_id = update.message.from_user.id

    messages[user_id].append(text)

    if messages[user_id].count(text) >= 3:
        await update.message.delete()

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ 동일한 글 반복으로 삭제되었습니다."
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        spam_check
    )
)

print("봇 실행중...")

app.run_polling()
