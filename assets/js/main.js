import { renderChart } from './charts.js';

async function uploadData() {
    const fileInput = document.getElementById('select_file');
    const file = fileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.status === 'success') {
            // 数値表示の更新
            document.getElementById('display_students_total').innerText = data.students_total;
            document.getElementById('display_parents_total').innerText = data.parents_total;

            // 分離した関数を使ってグラフを描画
            renderChart('chart1', '全体満足度', ['平均'], [data.satisfaction]);
            renderChart('chart2', '新入生満足度', ['平均'], [data.satisfaction_students]);
            renderChart('chart3', '保護者満足度', ['平均'], [data.satisfaction_parents]);
            renderChart('chart4', '全体所要時間', ['平均'], [data.fell_time]);
            renderChart('chart5', '新入生所要時間', ['平均'], [data.fell_time_students]);
            renderChart('chart6', '保護者所要時間', ['平均'], [data.fell_time_parents]);
        }
    } catch (error) {
        console.error('通信エラー：', error);
    }
}

// HTMLのonclickから呼び出せるようにグローバルスコープに登録
window.uploadData = uploadData;