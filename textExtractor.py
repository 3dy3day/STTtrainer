from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
import time

text_file = open('page_DOM.txt', 'w', encoding='UTF-8')

def getText(url):
  global url_file
  print("hoge: ",url)
  html=requests.get(str(url)).text
  soup=BeautifulSoup(html,"html.parser")
  for script in soup(["script", "style"]):
      script.decompose()

  text=soup.get_text()

  lines=[]
  for line in text.splitlines():
    lines.append(line.strip())

  text="\n".join(line for line in lines if line)
  # print(text)
  text_file.write(text)

def main():
  global text_file
  with open('./url_list.txt', "r", encoding='UTF-8') as f:
    for line in f:
      if line != "\n":
        # print("This", line.strip())
        time.sleep(1)
        getText(line.strip())
  text_file.close()

if __name__ == "__main__":
    main()