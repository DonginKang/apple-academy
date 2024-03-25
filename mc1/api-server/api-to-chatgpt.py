from flask import Flask, jsonify, request
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseOutputParser
from langchain.prompts import PromptTemplate, ChatPromptTemplate
import json

class CommaOutputParser(BaseOutputParser):
    """콤마로 구분된 문자열을 파싱하는 클래스."""
    def parse(self, text):
        items = text.strip().split(",")
        return list(map(str.strip, items))

def convert_list_to_string(activity_list):
    """리스트를 쉼표로 구분된 문자열로 변환하는 함수."""
    return ', '.join(activity_list)


template = ChatPromptTemplate.from_messages(
    [
        ("system", 
        """
        비행기를 타고 해외 여행을 갈때 필요한 짐을 알려주세요.
        답변은 아래 요구사항을 참고하세요.
        1. 아래 표기된 각 항목별로 {items} 개 이상의 짐을 말해주세요.
        2. 한국어로만 답변해 주세요.
        3. 데이터를 가공하기 쉽도록 Dictionaly 형태로 만들어 주세요. 예를들어 Key 값은 필수 항목이 될거고 Value 값은 List 형태가 되어야 합니다.
        4. 중복된 짐은 제거해주세요
        - 필수 항목: 해외 여행을 갈때 꼭 챙겨가야할 것. 예시=여권 및 비자, 항공권, 숙박 예약 확인서, 국제 운전 면허증, 여행자 보험, 현금 및 신용카드/체크카드
        - 옷: 여행 목적지의 날씨에 따라 옷을 추천 해줘야 함. 예시=긴 양말, 속옷, 재킷, 후드티
        - 세면 도구: 예시=콘택트 렌즈, 렌즈 세척액, 칫솔, 치약, 빗, 치실, 면도기, 쉐이빙젤, 면봉
        - 활동: 여행 중 즐길 거리에 대한 짐 예시=수영복, 선글라스, 자외선 차단제, 등산 스틱
        - 날씨: 여행 일정에 맞게 날씨 정보를 상세하게 말해준다. 예시= 목적지의 1월 1일 부터 1월 5일까지의 날씨는 평균적으로 최저기온 -2도, 최고기온 5도가 될 예정입니다.
        """),
        # 여기서부터 실제 사용자의 입력을 처리합니다.
        (
            "human",
            """
            저는 {gender}이고, {destination}으로 해외 여행을 갈 예정입니다. \
            {start_month}월 {start_day}일에 출발해서 {days}일 동안 머물 예정입니다. \
            여행 중에는 {activities}를 즐길 계획입니다. \
            위 사항을 참고하여 체크리스트 항목을 만들어주세요.
            """
        ),
    ]
)


app = Flask(__name__)

# 예시 데이터
data = {
    "items": [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"}
    ]
}

# 루트 엔드포인트
@app.route('/')
def index():
    return "Welcome to the Flask REST API!"

# # 모든 아이템 조회
# @app.route('/items', methods=['GET'])
# def get_items():
#     return jsonify(data)

# # 특정 아이템 조회
# @app.route('/items/<int:item_id>', methods=['GET'])
# def get_item(item_id):
#     item = next((item for item in data["items"] if item["id"] == item_id), None)
#     return jsonify(item) if item else ('', 404)

# 기본 품목 생성 
@app.route('/basic', methods=['POST'])
def get_basic_items():

    data = request.json
   
    items = data.get('items')
    gender = data.get('gender')
    destination = data.get('destination')
    start_month = data.get('start_month')
    start_day = data.get('start_day')
    days = data.get('days')
    activities = data.get('activities')

    # items = "2"
    # gender = "남자"
    # destination = "서울"
    # start_month = "1"
    # start_day = "10"
    # days = "5"
    # activities = "수영, 등산"

    input_data = {
        "items": items,
        "gender": gender,
        "destination": destination,
        "start_month": start_month,
        "start_day": start_day,
        "days": days,
        "activities": activities
    }

    chat = ChatOpenAI(
    temperature=0.1,
    )
    
    chain = template | chat #| CommaOutputParser()
    # Invoke the chain with the input
    output = chain.invoke(input_data)
    print(output)
    response_data = json.loads(output.content)

    return jsonify(response_data), 201

# 서버 실행
if __name__ == '__main__':
    app.run(debug=True, port=8080)
