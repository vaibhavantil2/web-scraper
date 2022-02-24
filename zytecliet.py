# Python 3 example using requests library.
import requests


def get_html(url):
   API_URL = "https://api.zyte.com/v1/extract"
   API_KEY = "76ddd993eca94faeb719024fa1fade82"
   response = requests.post(API_URL, auth=(API_KEY, ''), json={
      "url": url,
      "browserHtml": True
   })
   data = response.json()
   # data['browserHtml'] con
   return data
