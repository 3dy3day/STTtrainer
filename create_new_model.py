import requests
import json
import time

# define stuffs
# Don't forget to add quotations
URL="URL"
API_KEY="API_KEY"

PATH_TO_CORPUS="PATH_TO_CORPUS"
PATH_TO_WORDS="PATH_TO_WORDS"
CORPORA_NAME="CORPORA_NAME"


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
    result = requests.post(URL+"/v1/customizations", auth=('apikey', API_KEY), headers=req_header, data=data)
    customization_id = json.loads(result.text)["customization_id"]
    return customization_id

# add corpus
def addCorpus(CUSTOMIZATION_ID):
    with open(PATH_TO_CORPUS, 'r') as f:
        data = f.read()
    _ = requests.post(URL+"/v1/customizations/"+CUSTOMIZATION_ID+"/corpora/"+CORPORA_NAME, auth=('apikey', API_KEY), data=data)
    return

# add words
def addWords(CUSTOMIZATION_ID):
    with open(PATH_TO_CORPUS, 'r') as f:
        data = f.read()
    req_header = {
        'Content-Type': 'application/json',
    }
    _ = requests.post(URL+"/v1/customizations/"+CUSTOMIZATION_ID+"/words", auth=('apikey', API_KEY), headers=req_header, data=data)
    return

# train
def train(CUSTOMIZATION_ID):
    "apikey:%SPEECH_TO_TEXT_APIKEY%" "%SPEECH_TO_TEXT_URL%/v1/customizations/%CUSTOMIZATION_ID%/train?strict=false"
    _ = requests.get(URL+"/v1/customizations/"+CUSTOMIZATION_ID+"/train?strict=false", auth=('apikey', API_KEY))
    return

# check status
def checkStatus(CUSTOMIZATION_ID):
    r = requests.get(URL+"/v1/customizations/"+CUSTOMIZATION_ID, auth=('apikey', API_KEY))
    status = json.loads(r.text)["status"]
    return status

def main():
    id = getCustomId()
    addCorpus(id)
    # addWords(id)
    train(id)
    while checkStatus(id) != "available":
        time.sleep(5)
    print("Training has completed!")

if __name__ == "__main__":
    main()
