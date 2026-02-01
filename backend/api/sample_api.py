from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np # NaN判定をより確実にするために追加

app = Flask(__name__,
            template_folder='../../templates',
            static_folder='../../assets',
            static_url_path='/static'
            )
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'ファイルが見つかりません'}), 400
    file = request.files['file']
    filename = file.filename
    if filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif filename.endswith(('.xls', '.xlsx')):
            # シート名を指定。openpyxlがインストールされている必要があります
            df = pd.read_excel(file, sheet_name='フォームの回答 1')
        else:
            return jsonify({'error': 'ファイル形式が違います。CSVまたはExcelファイルをアップロードしてください。'}), 400
        
        print("読み込まれた列名一覧:", df.columns.tolist())
        
        df['本日の説明会の満足度を教えてください'] = pd.to_numeric(df['本日の説明会の満足度を教えてください'], errors='coerce')

        # 計算処理
        data_sum = 8
        students_total = (df['0'] == '新入生ご本人様').sum()
        parents_total = (df['0'] == '保護者様').sum()
        
        satisfaction = df['本日の説明会の満足度を教えてください'].mean()
        satisfaction_students = df[df['0'] == '新入生ご本人様']['本日の説明会の満足度を教えてください'].mean()
        satisfaction_parents = df[df['0'] == '保護者様']['本日の説明会の満足度を教えてください'].mean()
        
        time_labels = ['短い', 'ちょうど良い', '長い']
        good_point_labels = [
            '大学生協のご説明',
            '九工大生の一日（通学編）', 
            '九工大生の一日（講義編）',
            '九工大生の一日（昼食編）',
            '九工大生の一日（学外編）',
            '九工大での4年間',
        ]

        # 2. 全体、新入生、保護者それぞれのカウント関数
        def time_get_counts(target_df):
            counts = target_df['説明時間はいかがでしたか。'].value_counts().to_dict()
            # 短い・ちょうど良い・長いが0件でも必ずリストに含まれるように整理
            return [int(counts.get(label, 0)) for label in time_labels]
        
        # 2. カンマ区切りのデータをバラバラにしてカウントする関数
        def good_point_get_counts(target_df):
            # 列名が正しいか確認してください
            col_name = 'よかった、ためになった説明を教えてください'
            if col_name not in target_df.columns:
                return [0] * len(good_point_labels)

            # ① 該当列を取得し、空行を除外して文字列型に変換
            series = target_df[col_name].dropna().astype(str)
            
            # ② カンマ（とそれに続く空白）で分割して、各要素を独立した行に展開(explode)
            # 正規表現 r',\s*' を使うことで、「,」のみの場合と「, 」（カンマ＋スペース）の両方に対応できます
            all_answers = series.str.split(r',\s*').explode()
            
            # ③ 前後の余計な空白を削除してから集計し、辞書形式にする
            counts = all_answers.str.strip().value_counts().to_dict()
            
            # 定義した labels の順番に数値を並べてリストを返す
            return [int(counts.get(label, 0)) for label in good_point_labels]
         # 新入生と保護者のデータフレームを分割
        
        students_df = df[df['0'] == '新入生ご本人様']
        parents_df = df[df['0'] == '保護者様']
        
        # NaN（未回答）を0に置き換える処理（修正・補完）
        # .item() を使うとnumpy型からPython標準型へ安全に変換できます
        return jsonify ({
            'status': 'success',
            'time_labels': time_labels,
            'time_data_all': time_get_counts(df),
            'time_data_students': time_get_counts(students_df),
            'time_data_parents': time_get_counts(parents_df),
            'good_point_labels': good_point_labels,
            'good_point_data_all': good_point_get_counts(df),
            'good_point_data_students': good_point_get_counts(students_df),
            'good_point_data_parents': good_point_get_counts(parents_df),
            'students_total': int(students_total) if pd.notna(students_total) else 0,
            'parents_total': int(parents_total) if pd.notna(parents_total) else 0,
            'satisfaction': float(satisfaction) if pd.notna(satisfaction) else 0.0,
            'satisfaction_students': float(satisfaction_students) if pd.notna(satisfaction_students) else 0.0,
            'satisfaction_parents': float(satisfaction_parents) if pd.notna(satisfaction_parents) else 0.0,
            'data_sum': int(data_sum),
            'file_name': filename
        })
        
    except Exception as e:
        # ターミナルに詳細なエラーを出すための追記
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)