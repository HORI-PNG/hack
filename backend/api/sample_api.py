from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from ..utils.analyzer import analyze_survey_data # 分離したロジックをインポート

app = Flask(__name__,
            template_folder='../../templates',
            static_folder='../../assets',
            static_url_path='/static')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'ファイルが見つかりません'}), 400
    
    file = request.files['file']
    try:
        # 計算ロジックを呼び出し
        data = analyze_survey_data(file, file.filename)
        return jsonify({'status': 'success', **data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)