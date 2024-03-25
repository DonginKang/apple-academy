import requests
import json

# Flask 서버의 URL 설정
url = 'http://localhost:8080/basic'
#url = 'http://localhost:8080/specific'

input_data = {
    "items": "20",
    "gender": "남자",
    "destination": "도쿄",
    "start_month": "6",
    "start_day": "10",
    "days": "5",
    "activities": "수영, 등산"
}

# input_data = {
#     "items": "10",
#     "requirements": "4살된 아기도 같이 여행 갑니다"
# }
 

# POST 요청을 보내고 응답 받기
response = requests.post(url, json=input_data)

# 서버로부터 받은 응답 출력
print("Status Code:", response.status_code)
print("Response Content:", response.json())

