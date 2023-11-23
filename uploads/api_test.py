import requests
import json






url = "http://127.0.0.1:8000/imagesearch/"
response = requests.post(url=url, data={"image_path": 'apple.jpg'},)
print((response.content))

# url = "http://127.0.0.1:8000/textsearch/"
# response = requests.post(url=url, data={"text": 'motorcycle'},)
# print((response.content))