from flask import Flask, jsonify, request

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

# 모든 아이템 조회
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data)

# 특정 아이템 조회
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in data["items"] if item["id"] == item_id), None)
    return jsonify(item) if item else ('', 404)

# 아이템 추가
@app.route('/items', methods=['POST'])
def add_item():
    item = request.json
    data["items"].append(item)
    return jsonify(item), 201

# 서버 실행
if __name__ == '__main__':
    app.run(debug=True, port=8080)
