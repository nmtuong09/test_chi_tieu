
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackContext
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

# B1: Cấu hình Telegram bot trên telegram và lấy token để khai báo ở đây
TELEGRAM_BOT_TOKEN ="7702193644:AAGopapZ-awNmcKrEMaVjX6HuilrJbXToP0"
# B2: Cấu hình Webhook của google app scrip và khai báo tại đây
WEEBHOOK_URL ="https://script.google.com/macros/s/AKfycbwPxksbBxn-GWocQO71UdXOBm3RJpHTPQ26CjzTh3LWmQNhX5X9d6c4Ms2efyHnzygz-A/exec"

# Lệnh /start
def start(update:Update, context: CallbackContext):
    update.message.reply_text("Chào bạn! Gửi tin nhắn theo định dạng sau:\n\n<Nội dung> - <Số tiền>\n\nVD: Cà phê - 50000")
# xử lý tin nhắn chi tiêu
def xu_ly_tin(update: Update, context: CallbackContext):
    try:
        text = update.message.text
        content, amount = [x.strip() for x in text.split("-")]

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # gửi dữ liệu vào google apps scrip webhook
        payload = {"date": current_time, "content": content,"amount": amount}
        response = requests.post(WEEBHOOK_URL, json = payload)

        if response.text == "Success":
            update.message.reply_text("Ghi nhận chi tiêu thành công!")
        else:
            update.message.reply_text("Error: check lại dữ liệu!")
    except Exception as e:
        logging.error(e)
        update.message.reply_text("Sai định dạng. Vui lòng gửi tin nhắn theo định dạng:\n<Nội dung> - <Số tiền>")
# Tạo bot Telegram
def main():
    update = Updater(TELEGRAM_BOT_TOKEN, use_context = True)
    dispatcher = update.dispatcher
    dispatcher.add_handler(CommandHandler("start",start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, xu_ly_tin))

    update.start_polling()
    update.idle()
if __name__ == '__main__':
    main()
