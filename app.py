
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = '8141940089:AAFk8lh0Hq6ltUFGAXB79v9TcxFtjhG68vk'
OPENAI_API_KEY = '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'

def ask_gpt_botz(message):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "system",
                "content": "شما یک تحلیلگر حرفه‌ای بازار ارزهای دیجیتال هستید که بر پایه استراتژی BOTZ تحلیل می‌کنید. همیشه تحلیل دقیق، با ساختار مشخص، و سیگنال‌های قوی ارائه می‌دهید. اگر احتمال موفقیت سیگنال زیر ۷۰٪ باشد، فقط پیشنهاد صبر بده."
            },
            {
                "role": "user",
                "content": message
            }
        ],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.json
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    try:
        reply = ask_gpt_botz(text)
    except Exception as e:
        reply = "مشکلی در پاسخ‌دهی وجود دارد. لطفاً دوباره تلاش کنید."

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(telegram_url, json={"chat_id": chat_id, "text": reply})

    return "ok"

@app.route("/")
def home():
    return "BOTZ Telegram GPT is running."

if __name__ == "__main__":
    app.run(port=5000)
