import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests
from datetime import datetime

# Cấu hình Telegram bot
TELEGRAM_BOT_TOKEN = "7702193644:AAGopapZ-awNmcKrEMaVjX6HuilrJbXToP0"
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwPxksbBxn-GWocQO71UdXOBm3RJpHTPQ26CjzTh3LWmQNhX5X9d6c4Ms2efyHnzygz-A/exec"


# Lệnh /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Chào bạn! Gửi tin nhắn theo định dạng sau:\n\n<Nội dung> - <Số tiền>\n\nVD: Cà phê - 50000"
    )

# Xử lý tin nhắn chi tiêu
async def xu_ly_tin(update: Update, context: CallbackContext):
    try:
        # Lấy nội dung tin nhắn
        text = update.message.text
        content, amount = [x.strip() for x in text.split("-")]

        # Lấy thời gian hiện tại
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Gửi dữ liệu vào webhook
        payload = {"date": current_time, "content": content, "amount": amount}
        response = requests.post(WEBHOOK_URL, json=payload)

        if response.text == "Success":
            await update.message.reply_text("Ghi nhận chi tiêu thành công!")
        else:
            await update.message.reply_text("Error: kiểm tra lại dữ liệu!")
    except Exception as e:
        logging.error(e)
        await update.message.reply_text(
            "Sai định dạng. Vui lòng gửi tin nhắn theo định dạng:\n<Nội dung> - <Số tiền>"
        )

# Tạo bot Telegram
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    # application = application.sync_dispatcher
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, xu_ly_tin))

    application.run_polling()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
