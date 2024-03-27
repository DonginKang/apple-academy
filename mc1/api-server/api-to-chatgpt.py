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
        1. 한국어로만 답변해 주세요.
        2. 데이터를 가공하기 쉽도록 Dictionaly 형태로 만들어 주세요. 예를들어 Key 값은 필수 항목이 될거고 Value 값은 List 형태가 되어야 합니다.
        3. 중복된 값은 제거 해주세요
        4. 아래 표기된 각 항목별로 {items} 개 이상의 짐을 말해주세요.
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

custom_template = ChatPromptTemplate.from_messages(
    [
        ("system", 
        """
        비행기를 타고 해외 여행을 가려고 합니다. 기본적인 짐은 이미 챙겼습니다. 사용자는 아래와 같이 질문을 할 예정 입니다.
        "4살된 아기와 함께 여행을 가는데, 어떤 짐을 챙겨야 할까요?" 
        답변은 아래 요구사항을 참고하세요.
        1. 한국어로만 답변해 주세요.
        2. 데이터를 가공하기 쉽도록 Dictionaly 형태로 만들어 주세요. 예를들어 Key 값은 아기 항목이 될거고 Value 값은 List 형태가 되어야 합니다.
        3. 중복된 짐은 제거해주세요
        4. 아래 표기된 각 항목별로 {items} 개 이상의 짐을 말해주세요.
        - 아기: 4살된 아기와 함께 여행을 가려고 합니다. 예시=아기용 기저귀, 물티슈, 기저귀 크림, 아기 옷, 아기 물병, 아기 약품, 아기 여권 및 비자, 아기 장난감, 아기 수면 용품, 아기 그림 도구
        """),
        # 여기서부터 실제 사용자의 입력을 처리합니다.
        (
            "human",
            """
            {requirements}
            이미 필수적인 짐들은 다 챙겼습니다. 제 질문에 맞는 특정 항목에 대한 짐만 알려주세요.
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

    # Print the output
    result = output.content
    result_json = json.loads(result)


    """
    output.content is string and content is below

    {
    "필수 항목": ["여권 및 비자", "항공권", "숙박 예약 확인서", "여행자 보험", "현금", "신용카드/체크카드", "휴대폰 및 충전기", "여행 일정 및 숙소 정보", "약 및 의료 보험 카드", "도시락 또는 간식", "여행용 가방", "언어 사전 또는 번역 앱", "여행용 충전 변환기", "소독제", "마스크", "손 세정제", "여행용 우산", "여행용 스마트폰 앱 설치", "긴급 연락처 목록", "여행용 보조 배터리"],
    "옷": ["반팔 티셔츠", "반바지", "양말", "수영복", "비치웨어", "모자", "스니커즈", "슬리퍼", "가벼운 재킷", "반바지", "속옷", "파자마", "손수건", "햇", "바람막이 옷", "운동화", "가디건", "정장", "넥타이", "정장용 신발"],
    "세면 도구": ["칫솔", "치약", "면도기", "면도 크림", "샴푸", "린스", "바디워시", "클렌징 폼", "화장솜", "선크림", "립밤", "헤어 드라이기", "고데기", "헤어 스프레이", "향수", "샤워 타월", "면봉", "헤어 브러쉬", "렌즈 케이스", "렌즈 액"],
    "활동": ["수영복", "수경", "비치백", "비치타월", "스노클링 장비", "등산화", "등산 모자", "등산 지팡이", "등산 장갑", "등산 가방", "등산 압박대", "등산 안대", "등산 양말", "등산 바지", "등산 긴팔티", "등산 배낭", "등산 악세사리", "등산 보조 배터리", "등산 약", "등산 음식"],
    "날씨": "도쿄의 6월 10일부터 6월 15일까지의 날씨는 평균 최저기온 18도, 최고기온 25도로 따뜻한 날씨가 예상됩니다."
     }

    """

    # result = jsonify(result_json)
    print(result_json)
    # print(type(result))
    return result_json, 201

# 특정 품목 생성 
@app.route('/specific', methods=['POST'])
def get_specific_items():

    data = request.json
   
    items = data.get('items')
    requirements = data.get('requirements')

    input_data = {
        "items": items,
        "requirements": requirements
    }

    chat = ChatOpenAI(
    temperature=0.1,
    )
    
    chain = custom_template | chat #| CommaOutputParser()
    # Invoke the chain with the input
    output = chain.invoke(input_data)

    # Print the output
    result = output.content

    return result, 201


# 서버 실행
if __name__ == '__main__':
    app.run(debug=True, port=8080)
