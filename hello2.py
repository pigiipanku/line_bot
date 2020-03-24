import pandas as pd

word_csv = pd.read_csv('./voc_list_kiso_kansei.csv', encoding="SHIFT-JIS", header=None)

# word_csvをいい感じに読み込む
word_dict = {}
for index, row in word_csv.iterrows():
    if row[4] == "名詞" :
        word_dict[row[3]] = row[2]



# 最後が「ん」もしくはすでに使っていたワードだったらアウト
def judge_last_char(word, used_word_list):
    if word[-1] != "ん" and (word not in used_word_list):
        return True
    else:
        return False





# コンピューターのプレイ
def type_by_computer(input_word, used_word_list):
    for com_word in word_dict.keys():
        if input_word[-1] == com_word[0] and judge_last_char(com_word, used_word_list):
            used_word_list.append(com_word)
            return com_word, used_word_list
    return "", used_word_list


# ユーザーのプレイ
def type_by_user(input_word, used_word_list):
    last_word = input_word[-1]
    if last_word == "ー":
        last_word = input_word[-2]
    elif last_word == "ゃ" or "ゅ" or "ょ" or "ぁ" or "ぃ" or "ぅ" or "ぇ" or "ぉ" :
        last_word.upper()
    user_word = input(f"「{last_word}」からはじまることばを入力してください：")

    if last_word == user_word[0] and judge_last_char(user_word, used_word_list):
        used_word_list.append(user_word)
        return user_word, used_word_list
    else:
        return "", used_word_list




if __name__ == "__main__":
    cnt = 1
    used_words = []
    print("COM「対戦宜しくおねがいします」")
    print("COM「しりとり」")

    shiritori_word, used_words = type_by_user("しりとり", used_words)

    if shiritori_word == "" :
        print("You Lose笑")
    else :
        print(f"{cnt}：ユーザー「{shiritori_word}」")
        cnt += 1
        while True:
            # コンピューター
            shiritori_word, used_words = type_by_computer(shiritori_word, used_words)
            if shiritori_word != "":
                print(f"{cnt}：COM「{word_dict[shiritori_word]}({shiritori_word})」")
                cnt += 1
            else:
                print("YOU WIN!")
                break


            # ユーザー
            shiritori_word, used_words = type_by_user(shiritori_word, used_words)
            if shiritori_word != "" :
                print(f"{cnt}：ユーザー「{shiritori_word}」")
                cnt += 1
            else:
                print("YOU LOSE笑")
                break

