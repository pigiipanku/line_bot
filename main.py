from flask import Flask, request, abort
import os

import pandas as pd
import random

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# shiritoris = {"yutaro": Shiritori(i)}

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

class Shiritori():
    word_dict = {}
    used_words = []

    com_word = ""
    user_word = ""

    def __init__(self, user_word, used_words):
        self.word_dict = self.create_word_dict()
        self.user_word = user_word
        self.used_words = used_words

    @staticmethod
    def create_word_dict():
        word_csv = pd.read_csv('./voc_list_kiso_kansei.csv', encoding="SHIFT-JIS", header=None)

        # word_csvをいい感じに読み込む
        word_dict = {}
        for index, row in word_csv.iterrows():
            if row[4] == "名詞":
                word_dict[row[3]] = row[2]
        return word_dict

    # 最後が「ん」もしくはすでに使っていたワードだったらアウト
    def judge_last_char(self, word):
        if word[-1] != "ん" and (word not in self.used_words):
            return True
        else:
            return False

    # 修正する
    @staticmethod
    def correct(input_word):
        last_chr = input_word[-1]
        fail_list = ["ー", "）"]
        mini_dict = {"ゃ": "や", "ゅ": "ゆ", "ょ": "よ", "ぁ": "あ", "ぃ": "い", "ぅ": "う", "ぇ": "え", "ぉ": "お"}
        if last_chr in fail_list:
            last_chr = input_word[-2]
        if last_chr in mini_dict.keys():
            last_chr = mini_dict[last_chr]
        return last_chr

    # コンピューターのプレイ
    def type_by_computer(self):
        com_words = []
        last_chr = self.correct(self.user_word)
        for com_word in self.word_dict.keys():
            if last_chr == com_word[0] and self.judge_last_char(com_word):
                com_words.append(com_word)

        if com_words:
            com_random_word = random.choice(com_words)
            self.com_word = com_random_word
            self.used_words.append(com_random_word)
        else:
            self.com_word = ""


@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    profile = line_bot_api.get_profile(event.source.user_id)

    # if アカウント名 in shiritoris:
    #     shiritori = shiritoris[あくんと名]
    # else:
    #     shiritoris.pop(あくんと名)
    shiritori = Shiritori(user_word=event.message.text, used_words=[])
    shiritori.type_by_computer()

    response_text = f"{profile.display_name}\n"
    if shiritori.com_word != "":
        response_text = shiritori.com_word
    else:
        response_text = "YOU WIN!"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response_text))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)