from flask import Flask, render_template, request, jsonify
import lotto11  # 로또 번호 생성 로직이 포함된 파일

app = Flask(__name__)

@app.route('/')
def index():
    # 기본 페이지
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate_lotto_numbers():
    # 로또 번호 생성
    lotto_numbers = lotto11.generate_lotto_numbers(1)
    
    # JSON 형태로 결과 반환
    return jsonify(lotto_numbers=lotto_numbers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
