// グラフオブジェクトを保持する変数
let charts = {};

/**
 * 指定されたキャンバスに棒グラフを描画する
 * @param {string} canvasId - HTMLのcanvasタグのID
 * @param {string} label - データセットのラベル
 * @param {Array} labels - X軸のラベル
 * @param {Array} data - 表示するデータ数値
 */
export function renderChart(canvasId, label, labels, data) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    // すでにグラフが存在する場合は破棄（再描画のため）
    if (charts[canvasId]) {
        charts[canvasId].destroy();
    }

    charts[canvasId] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}