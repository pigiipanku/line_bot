import os
import random
import json
import pickle

import jaconv
import pandas as pd
from flask import Flask, request, abort
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


# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


json_open_2 = open("new_dict_2.json", "r")
word_dict_3 = json.load(json_open_2)
alpha_list = ["Ａ","Ｂ","Ｃ","Ｄ","Ｅ","Ｆ","Ｇ","Ｈ","Ｉ","Ｊ","Ｋ","Ｌ","Ｍ","Ｎ","Ｏ","Ｐ","Ｑ",
              "Ｒ","Ｓ","Ｔ","Ｕ","Ｖ","Ｗ","Ｘ","Ｙ","Ｚ","ａ","ｂ","ｃ","ｄ","ｅ","ｆ","ｇ","ｈ",
              "ｉ","ｊ","ｋ","ｌ","ｍ","ｎ","ｏ","ｐ","ｑ","ｒ","ｓ","ｔ","ｕ","ｖ","ｗ","ｘ","ｙ","ｚ",
              "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V"
              ,"W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s"
              ,"t","u","v","w","x","y","z"]

class Shiritori():
    word_dict = {}
    used_words = []

    com_word = ""
    user_word = ""

    def __init__(self, user_word):

        self.user_word = user_word
        self.used_words.append(user_word)

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
        if word[-1] != "ん" and (word not in self.used_words) :
            for i in list(word) :
                if i in alpha_list :
                    return False
            return True
        else:
            return False

    # 修正する
    @staticmethod
    def correct(input_word):
        input_word = jaconv.kata2hira(input_word)
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
        for com_word in word_dict_3.keys():
            if last_chr == com_word[0] and self.judge_last_char(com_word):
                com_words.append(com_word)

        if com_words:
            com_random_word = random.choice(com_words)
            self.com_word = com_random_word
            self.used_words.append(com_random_word)
        else:
            self.com_word = ""

    # ユーザーのプレイ
    def type_by_user(self, user_word):
        user_word = jaconv.kata2hira(user_word)
        last_chr = self.correct(self.com_word)
        if last_chr == user_word[0] and self.judge_last_char(user_word):
            self.user_word = user_word
            self.used_words.append(user_word)
        else:
            self.user_word = ""


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
    user_id = event.source.user_id
    try:
        with open(f'{user_id}.pickle', 'rb') as f:
            shiritori = pickle.load(f)
        shiritori.type_by_user(user_word=event.message.text)
    except FileNotFoundError:
        shiritori = Shiritori(user_word=event.message.text)

    if shiritori.user_word == "":
        response_text = "あなた弱いのね。私の勝ち☆"
    else:
        shiritori.type_by_computer()
        if shiritori.com_word != "":
            com_last_char = Shiritori.correct(shiritori.com_word)
            response_text = f"{word_dict_3[shiritori.com_word]}({shiritori.com_word})\n「{com_last_char}」から始まる言葉で入力するのよ。"
        else:
            response_text = "や、やるじゃない...あなたの勝ちよ。"

    if response_text in ["あなた弱いのね。私の勝ち☆", "や、やるじゃない...あなたの勝ちよ。"]:
        shiritori.used_words = []

    with open(f'{user_id}.pickle', 'wb') as f:
        pickle.dump(shiritori, f)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response_text))


if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
