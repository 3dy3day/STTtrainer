import requests
import json
import time

# define stuffs
# Don"t forget to add quotations
URL="URL"+"/v1"
API_KEY="API_KEY"

PATH_TO_CORPUS=r"PATH_TO_CORPUS"
PATH_TO_WORDS=r"PATH_TO_WORDS"
PATH_TO_AUDIO = r"PATH_TO_AUDIO"

#this will be automaticaly filled
CUSTOMIZATION_ID=""

# get custom id
def getCustomId():
    name = input("Custom name: ")
    description = input("Custome description: ")
    req_header = {
        "Content-Type": "application/json",
    }
    data = {
        "name": name,
        "base_model_name": "ja-JP_NarrowbandModel",
        "description": description
    }
    result = requests.post(URL+"/customizations", auth=("apikey", API_KEY), headers=req_header, data=json.dumps(data))
    try:
        customization_id = json.loads(result.text)["customization_id"]
        print("your custom_id is:",customization_id)
        return customization_id
    except:
        print(json.loads(result.text))
        return

# add corpus
def addCorpus():
    CORPORA_NAME = input("Name the corpora: ")
    print("adding corpus...")
    req_header = {
            "Content-Type": "text/plain",
        }
    with open(PATH_TO_CORPUS, "r", encoding="UTF-8") as corpus:
        corpus = corpus.read()
        response = requests.post(URL+"/customizations/"+CUSTOMIZATION_ID+"/corpora/"+CORPORA_NAME+"?allow_overwrite=true", auth=("apikey", API_KEY), headers=req_header, data=corpus.encode("utf-8"))
        print(response.text)
    time.sleep(30)
    return

# add words
def addWords():
    print("adding words...")
    req_header = {
            "Content-Type": "application/json",
        }
    with open(PATH_TO_WORDS, "r", encoding="UTF-8") as word:
        word = word.read()
        response = requests.post(URL+"/customizations/"+CUSTOMIZATION_ID+"/words?allow_overwrite=true", auth=("apikey", API_KEY), headers=req_header, data=word.encode("utf-8"))
        print(response.text)
    time.sleep(30)
    return

# train
def train():
    _ = requests.post(URL+"/customizations/"+CUSTOMIZATION_ID+"/train?strict=false&customization_weight=1", auth=("apikey", API_KEY))
    print("training has started...")
    return

# check status
def checkStatusAll():
    r = requests.get(URL+"/customizations", auth=("apikey", API_KEY))
    status = json.loads(r.text)
    print(r.text)
    return status

def checkStatus():
    r = requests.get(URL+"/customizations/"+CUSTOMIZATION_ID, auth=("apikey", API_KEY))
    status = json.loads(r.text)["status"]
    print(r.text)
    return status

# delete customization
def deleteCustom():
    r = requests.delete(URL+"/customizations/"+CUSTOMIZATION_ID, auth=("apikey", API_KEY))
    status = json.loads(r.text)
    print(r.text)
    return status

# send Audio
def sendAudio():
    req_header = {
            "Content-Type": "audio/flac",
        }
    with open(PATH_TO_AUDIO, "rb") as audio: # +"&customization_weight=1"
        response = requests.post(URL+"/recognize?model=ja-JP_NarrowbandModel&language_customization_id="+CUSTOMIZATION_ID, auth=("apikey", API_KEY), headers=req_header, data=audio)
        print(response.text)

# check if input is int
def inputCheck(input):
    try:
        int_input = int(input)
        return int_input
    except:
        print("\nERROR: Only integers are allowed\n")
        return

def main():
    global CUSTOMIZATION_ID

    case = input("\nWelcom to IBM Cloud STT Trainer!\n0.Create New Custom\n1.Check Status\n2.Send Audio\n3.Delete Custom\n4.Exit\nInput: ")
    case = inputCheck(case)

    if case == 0: # 0.Create New Custom
        
        time_start = time.time()
        CUSTOMIZATION_ID = getCustomId()
        addCorpus()
        addWords()
        train()
        while checkStatus() != "available":
            time.sleep(10)
            print("time elapsed:", time.time() - time_start)    
        print("training has completed!")

    elif case == 1:
        print("\n\n\n")
        status_case = input("0.Check All\n1.Check Specifec\nInput: ")
        status_case = inputCheck(status_case)
        if status_case == 0:
            checkStatusAll()
        elif status_case == 1:
            CUSTOMIZATION_ID = input("Input Customization ID: ")
            checkStatus()

    elif case == 2: # 2.Send Audio
        print("\n\n\n")
        CUSTOMIZATION_ID = input("Input Customization ID: ")
        sendAudio()
    
    elif case == 3: #3.Delete Custom
        print("\n\n\n")
        CUSTOMIZATION_ID = input("Input Customization ID: ")
        deleteCustom()

        pass

    elif case == 4: # 4.Exit
        print("bye!")
        pass

    else:
        print("Invalid Input")


if __name__ == "__main__":
    main()
