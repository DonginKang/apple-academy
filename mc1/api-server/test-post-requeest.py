import requests
import json

# Flask 서버의 URL 설정
url = 'http://localhost:8080/basic'

input_data = {
    "items": "2",
    "gender": "man",
    "destination": "Seoul",
    "start_month": "1",
    "start_day": "1",
    "days": "5",
    "activities": "수영, 등산"
}

# POST 요청을 보내고 응답 받기
response = requests.post(url, json=input_data)
# JSON 응답을 읽기 쉬운 형태로 변환하여 출력
response_data = response.json()
print(json.dumps(response_data, indent=2, ensure_ascii=False))

# 서버로부터 받은 응답 출력
print(response.text)
