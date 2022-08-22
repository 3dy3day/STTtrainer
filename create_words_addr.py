import numpy as np
import json
import unicodedata

fukui = [r"PATH_OOMOJI", r"PATH_KOMOJI"]
shiga = [r"PATH_OOMOJI", r"PATH_KOMOJI"]
kyouto = [r"PATH_OOMOJI", r"PATH_KOMOJI"]
osaka = [r"PATH_OOMOJI", r"PATH_KOMOJI"]
hyogo = [r"PATH_OOMOJI", r"PATH_KOMOJI"]
nara = [r"PATH_OOMOJI", r"PATH_KOMOJI"]
waka = [r"PATH_OOMOJI", r"PATH_KOMOJI"]


address_list = [fukui, shiga, kyouto, osaka, hyogo, nara, waka]
address_words = open("address_words.json", "w", encoding='UTF-8')
words = {"words": []}
cities_added = set()
excepttion = []

for file in address_list:
    datas = np.loadtxt(file[0], delimiter=",", skiprows=1, encoding="utf-8", dtype="unicode")
    smallchar_data = np.loadtxt(file[1], delimiter=",", skiprows=1, encoding="utf-8", dtype="unicode")
    
    # print(data[:,7])
    for i in range(len(datas)):
        town = str(datas[i][8]).strip('"')
        town_sound = unicodedata.normalize('NFKC', str(datas[i][5]).strip('"'))
        town_sound_sc = unicodedata.normalize('NFKC', str(smallchar_data[i][5]).strip('"'))

        city = str(datas[i][7]).strip('"')
        city_sound = unicodedata.normalize('NFKC',str(datas[i][4]).strip('"'))
        city_sound_sc = unicodedata.normalize('NFKC', str(smallchar_data[i][4]).strip('"'))
    
        if "以下に掲載がない場合" in town or "（" in town or "）" in town or "、" in town:
            excepttion.append(city+town)
            continue

        if town_sound != town_sound_sc:
            sounds = [town_sound, town_sound_sc]
        else:
            sounds = [town_sound]

        word = {
            "word": town,
            "sounds_like": sounds,
            "display_as": town
        }
        words["words"].append(word)
# ################################################################
        if city_sound != city_sound_sc:
            sounds = [city_sound, city_sound_sc]
        else:
            sounds = [city_sound]

        word = {
            "word": city,
            "sounds_like": sounds,
            "display_as": city
        }
        if city not in cities_added:
            words["words"].append(word)
            cities_added.add(city)


print(cities_added)
json.dump(words, address_words, ensure_ascii=False)
address_words.close()

with open("exception_words.txt", "w", encoding="utf-8") as f:
    for line in excepttion:
        f.write(line+"\n")