import pandas as pd


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
            word_dict[row[3]] = row[2]
        return word_dict

    # 最後が「ん」もしくはすでに使っていたワードだったらアウト
    def judge_last_char(self, word):
        if word[-1] != "ん" and (word not in self.used_words):
            return True
        else:
            return False

    # コンピューターのプレイ
    def type_by_computer(self):
        for com_word in self.word_dict.keys():
            if self.user_word[-1] == com_word[0] and self.judge_last_char(com_word):
                self.com_word = com_word
                self.used_words.append(com_word)
                break
        else:
            self.com_word = ""

    # ユーザーのプレイ
    def type_by_user(self):
        user_word = input(f"「{self.com_word[-1]}」からはじまることばを入力してください：")
        if self.com_word[-1] == user_word[0] and self.judge_last_char(user_word):
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
