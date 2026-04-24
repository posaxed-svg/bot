import os
import requests
from telegram.ext import Updater, CommandHandler

# Token Railway'den alınacak
TOKEN = os.getenv("TELEGRAM_TOKEN")

def analyze(symbol):
    url = f"https://fapi.binance.com/fapi/v1/ticker/24hr?symbol={symbol}USDT"
    data = requests.get(url).json()

    price = float(data["lastPrice"])
    change = float(data["priceChangePercent"])

    if change > 0:
        direction = "LONG"
    else:
        direction = "SHORT"

    return f"{symbol} | {direction}\nFiyat: {price}\n24h değişim: {change}%"

def btc(update, context):
    update.message.reply_text(analyze("BTC"))

def eth(update, context):
    update.message.reply_text(analyze("ETH"))

def coin(update, context):
    try:
        symbol = context.args[0].upper()
        update.message.reply_text(analyze(symbol))
    except:
        update.message.reply_text("Kullanım: /coin btc")

def start(update, context):
    update.message.reply_text("Hazırım.\n/btc\n/eth\n/coin btc")

updater = Updater(TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("btc", btc))
dp.add_handler(CommandHandler("eth", eth))
dp.add_handler(CommandHandler("coin", coin))

updater.start_polling()
updater.idle()
