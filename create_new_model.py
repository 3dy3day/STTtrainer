from urllib import response
import requests
import json
import time

# define stuffs
# Don't forget to add quotations
URL="URL"+"/v1/customizations/"
API_KEY="API_KEY"

PATH_TO_CORPUS=r"PATH_TO_CORPUS"
PATH_TO_WORDS=r"PATH_TO_WORDS"
CORPORA_NAME=""

#this will be automaticaly filled
CUSTOMIZATION_ID=""

# get custom id
def getCustomId():
    req_header = {
        'Content-Type': 'application/json',
    }
    data = {
        "name": "name goes here",
        "base_model_name": "ja-JP_NarrowbandModel",
        "description": "description goes here"
    }
    result = requests.post(URL, auth=('apikey', API_KEY), headers=req_header, data=json.dumps(data))
    try:
        customization_id = json.loads(result.text)["customization_id"]
        print("your custom_id is:",customization_id)
        return customization_id
    except:
        print(json.loads(result.text))
        return

# add corpus
def addCorpus():
    req_header = {
            'Content-Type': 'text/plain',
        }
    with open(PATH_TO_CORPUS, 'r', encoding='UTF-8') as corpus:
        corpus = corpus.read()
        response = requests.post(URL+CUSTOMIZATION_ID+"/corpora/"+CORPORA_NAME+"?allow_overwrite=true", auth=('apikey', API_KEY), headers=req_header, data=corpus.encode("utf-8"))
        print(response.text)
    time.sleep(30)
    print("adding corpus...")
    return

# add words
def addWords():
    req_header = {
            'Content-Type': 'application/json',
        }
    with open(PATH_TO_WORDS, 'r', encoding='UTF-8') as word:
        word = word.read()
        response = requests.post(URL+CUSTOMIZATION_ID+"/words?allow_overwrite=true", auth=('apikey', API_KEY), headers=req_header, data=word.encode("utf-8"))
        print(response.text)
    time.sleep(30)
    print("adding words...")
    return

# train
def train():
    _ = requests.post(URL+CUSTOMIZATION_ID+"/train?strict=false", auth=('apikey', API_KEY))
    print("training has started...")
    return

# check status
def checkStatus():
    r = requests.get(URL+CUSTOMIZATION_ID, auth=('apikey', API_KEY))
    status = json.loads(r.text)["status"]
    print(r.text)
    return status

def main():
    global CUSTOMIZATION_ID
    time_start = time.time()
    CUSTOMIZATION_ID = id = getCustomId()
    addCorpus(id)
    addWords(id)
    train(id)
    while checkStatus(id) != "available":
        time.sleep(10)
        print("time elapsed:", time.time() - time_start)
    
    print("training has completed!")

if __name__ == "__main__":
    main()
