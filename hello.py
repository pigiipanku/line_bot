import csv

csv_file = open("voc_list_kiso_kansei.csv", "r", encoding="ms932", errors="", newline="" )
f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
used_list = {0:""}

def siritori(a,count) :
    last_word = a[-1]
    if last_word == "ー":
        last_word = a[-2]
    if last_word == "ん":
        print("You lose")
        return  "私の負けです"
    else:
        for x in f:
            library_word = x[3]
            if library_word[0] == last_word and library_word[-1] != "ん" and library_word not in used_list:
                print(library_word)
                count += 1
                used_list[count] = library_word
                count += 1
                used_list[count] = input_word
                return library_word
            else:
                continue
        return "私の負けです"

if __name__ == "__main__":
        input_word = input("：")
        library_word = siritori(input_word,0ひらがなで入力してください)
        cnt = 3
        while library_word != "私の負けです" :
            library_last_word = library_word[-1]
            if library_last_word == "ー":
                library_last_word = library_word[-2]
            input_word = input(library_last_word+"、からはじまる言葉をひらがなで入力してね：")
            if input_word[0] != library_last_word or input_word in used_list:
                 print(library_last_word+ "、からでないひらがなが入力されているか同じ言葉を使用してます")
                 continue
            else :
                library_word = siritori(input_word,cnt)
