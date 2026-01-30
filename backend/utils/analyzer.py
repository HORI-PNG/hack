import pandas as pd
import numpy as np

def analyze_survey_data(file, filename):
    if filename.endswith('.csv'):
        df = pd.read_csv(file)
    elif filename.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file, sheet_name='フォームの回答 1')
    else:
        raise ValueError("対応していないファイル形式です")

    # 数値変換（エラーはNaNになる）
    df['本日の説明会の満足度を教えてください'] = pd.to_numeric(df['本日の説明会の満足度を教えてください'], errors='coerce')
    df['説明時間はいかがでしたか。'] = pd.to_numeric(df['説明時間はいかがでしたか。'], errors='coerce')

    # NaNを0に置換する補助関数
    def clean_val(val):
        # pd.isna() は NaN や None を判定できる
        return float(val) if pd.notna(val) else 0.0

    # 属性ごとのデータ抽出
    student_df = df[df['0'] == '新入生ご本人様']
    parent_df = df[df['0'] == '保護者様']

    res_data = {
        'students_total': int(len(student_df)),
        'parents_total': int(len(parent_df)),
        
        # 全体平均
        'satisfaction': clean_val(df['本日の説明会の満足度を教えてください'].mean()),
        'fell_time': clean_val(df['説明時間はいかがでしたか。'].mean()),
        
        # 新入生平均
        'satisfaction_students': clean_val(student_df['本日の説明会の満足度を教えてください'].mean()),
        'fell_time_students': clean_val(student_df['説明時間はいかがでしたか。'].mean()),
        
        # 保護者平均
        'satisfaction_parents': clean_val(parent_df['本日の説明会の満足度を教えてください'].mean()),
        'fell_time_parents': clean_val(parent_df['説明時間はいかがでしたか。'].mean()),
    }
    
    return res_data