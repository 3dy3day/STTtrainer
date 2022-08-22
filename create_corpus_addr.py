import numpy as np

fukui = [r"PATH_OOMOJI", r"PATH_KOMOJI"]
shiga = [r"PATH_OOMOJI", r"PATH_KOMOJI"]
kyouto = [r"PATH_OOMOJI", r"PATH_KOMOJI"]
osaka = [r"PATH_OOMOJI", r"PATH_KOMOJI"]
hyogo = [r"PATH_OOMOJI", r"PATH_KOMOJI"]
nara = [r"PATH_OOMOJI", r"PATH_KOMOJI"]
waka = [r"PATH_OOMOJI", r"PATH_KOMOJI"]

address_list = [fukui, shiga, kyouto, osaka, hyogo, nara, waka]
cities_added = set()
excepttion = []

with open("exception.txt", "w", encoding="utf-8") as f:
    for line in excepttion:
        f.write(line+"\n")

address_corpus = open('address_corpus.txt', 'w', encoding='UTF-8')
for file in address_list:
    datas = np.loadtxt(file[0], delimiter=",", skiprows=1, encoding="utf-8", dtype="unicode")
    for data in datas:
        town = str(data[8]).strip('"')
        city = str(data[7]).strip('"')
        prefecture = str(data[6]).strip('"')

        if "以下に掲載がない場合" in town or "（" in town or "）" in town or "、" in town:
            continue
        address_corpus.write(town+"\n")
        address_corpus.write(city+town+"\n")
        address_corpus.write(prefecture+city+town+"\n")

address_corpus.close()

with open("exception_corpus.txt", "w", encoding="utf-8") as f:
    for line in excepttion:
        f.write(line+"\n")