import pandas as pd
import random


class Shiritori():
    word_dict = {}
    used_words = []

    com_word = ""
    user_word = ""

    def __init__(self, com_word):
        self.word_dict = self.create_word_dict()

        self.com_word = com_word
        self.used_words.append(com_word)

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

    # ユーザーのプレイ
    def type_by_user(self):
        last_chr = self.correct(self.com_word)

        while True:
            user_word = input(f"「{last_chr}」からはじまることばを入力してください：")
            if user_word != "":
                if user_word[0] == last_chr :
                    break

        if last_chr == user_word[0] and self.judge_last_char(user_word):
            self.user_word = user_word
            self.used_words.append(user_word)
        else:
            self.user_word = ""


if __name__ == "__main__":
    print("COM「対戦宜しくおねがいします」")
    print("COM「しりとり」")
    shiritori = Shiritori("しりとり")
    cnt = 1

    while True:
        # ユーザー
        shiritori.type_by_user()
        if shiritori.user_word != "":
            print(f"{cnt}：ユーザー「{shiritori.user_word}」")
            cnt += 1
        else:
            print("YOU LOSE笑")
            break

        # コンピューター
        shiritori.type_by_computer()
        if shiritori.com_word != "":
            print(f"{cnt}：COM「{shiritori.word_dict[shiritori.com_word]}({shiritori.com_word})」")
            cnt += 1
        else:
            print("YOU WIN!")
            break
