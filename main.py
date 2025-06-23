from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 環境変数からトークン・シークレット取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ユーザーごとの履歴を保存する辞書（必要なら）
chat_history = {}

@app.route("/callback", methods=["POST"])
def callback():
    # LINEからの署名ヘッダー取得
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text

    # 履歴の初期化（オプション）
    if user_id not in chat_history:
        chat_history[user_id] = []

    chat_history[user_id].append(user_message)

    # ✅ ダミー応答を返す部分（ここを自由に変更してもOK）
    reply_text = f"（ダミー応答）「{user_message}」を受け取りました！"

    # LINEに返答を送信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    # Render環境では PORT が必要
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
