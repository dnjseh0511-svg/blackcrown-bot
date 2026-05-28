from telegram.ext import Updater, MessageHandler, Filters, ChatMemberHandler
from collections import defaultdict

TOKEN = "8835471195:AAGG_9uNfZosE1Ah9_ZmcZuRySE_QdCCXxQ"

WELCOME_TEXT = """
🎉 {name} 님 환영합니다 🎉

♛ BLACK CROWN 자유홍보방 ♛

📌 하루 홍보 가능 횟수 : 3회
📌 동일 도배 / 반복홍보 금지
📌 과도한 홍보 시 자동 삭제됩니다

즐거운 활동 되시길 바랍니다 👑
"""

messages = defaultdict(list)

def welcome(update, context):
    try:
        user = update.chat_member.new_chat_member.user

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=WELCOME_TEXT.format(name=user.first_name)
        )
    except:
        pass

def spam_check(update, context):
    try:
        text = update.message.text
        user_id = update.message.from_user.id

        messages[user_id].append(text)

        if messages[user_id].count(text) >= 3:
            update.message.delete()

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⚠️ 동일한 글 반복으로 삭제되었습니다."
            )
    except:
        pass

updater = Updater(TOKEN, use_context=True)

dp = updater.dispatcher

dp.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))
dp.add_handler(MessageHandler(Filters.text, spam_check))

print("봇 실행중...")

updater.start_polling()
updater.idle()
