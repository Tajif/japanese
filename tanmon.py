<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>現代文 F.O.R. トレーナー</title>
    <style>
        :root {
            --primary: #4f46e5;
            --success: #16a34a;
            --danger: #dc2626;
            --bg: #f3f4f6;
        }
        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            background-color: var(--bg);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .container {
            width: 100%;
            max-width: 500px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
            padding: 20px;
            box-sizing: border-box;
        }
        h1 { font-size: 1.2rem; text-align: center; color: #1f2937; margin-top: 0; }
        .mode-select { display: flex; gap: 10px; margin-bottom: 20px; }
        button {
            padding: 10px 16px; border: none; border-radius: 8px;
            font-weight: bold; cursor: pointer; font-size: 0.9rem; transition: 0.2s;
        }
        .btn-mode { background: #e5e7eb; color: #374151; width: 100%; }
        .btn-mode.active { background: var(--primary); color: white; }
        
        .card {
            border: 2px solid #e5e7eb; border-radius: 12px;
            padding: 30px 20px; min-height: 150px;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            text-align: center; margin-bottom: 20px; position: relative;
        }
        .card-meta { position: absolute; top: 10px; left: 10px; font-size: 0.8rem; color: #9ca3af; }
        .question { font-size: 1.15rem; font-weight: bold; color: #111827; line-height: 1.5; }
        .answer { font-size: 1.1rem; color: var(--primary); font-weight: bold; margin-top: 20px; display: none; line-height: 1.5; }
        
        .action-area { display: flex; flex-direction: column; gap: 10px; }
        .btn-main { background: var(--primary); color: white; padding: 14px; font-size: 1rem; width: 100%; }
        .judge-buttons { display: none; gap: 10px; width: 100%; }
        .btn-wrong { background: var(--danger); color: white; width: 100%; padding: 14px; }
        .btn-correct { background: var(--success); color: white; width: 100%; padding: 14px; }
        
        .progress { text-align: center; font-size: 0.85rem; color: #6b7280; margin-top: 15px; }
    </style>
</head>
<body>

<div class="container">
    <h1>現代文 F.O.R. トレーナー</h1>
    
    <div class="mode-select">
        <button class="btn-mode active" id="mode-all" onclick="changeMode('all')">全問出題</button>
        <button class="btn-mode" id="mode-wrong" onclick="changeMode('wrong')">✕のみ復習 (<span id="wrong-count">0</span>)</button>
    </div>

    <div class="card">
        <div class="card-meta" id="card-meta">基礎レベル</div>
        <div class="question" id="question-text">質問がここに表示されます</div>
        <div class="answer" id="answer-text">回答がここに表示されます</div>
    </div>

    <div class="action-area">
        <button class="btn-main" id="btn-show" onclick="showAnswer()">答えを見る</button>
        <div class="judge-buttons" id="judge-block">
            <button class="btn-wrong" onclick="handleJudge(false)">✕ あやしい</button>
            <button class="btn-correct" onclick="handleJudge(true)">◯ 覚えた</button>
        </div>
    </div>

    <div class="progress" id="progress-text">0 / 0問</div>
</div>

<script>
// 全111問のうち、まずは基礎レベル（15問）のデータを格納
const allQuestions = [
    { id: 1, cat: "【しかし／だが】", q: "「しかし」「だが」を見たら？", a: "逆説。前と後ろで逆の内容。" },
    { id: 2, cat: "【しかし／だが】", q: "前と後ろ、どっちが重要？", a: "後ろ。" },
    { id: 3, cat: "【しかし／だが】", q: "それはなぜか？", a: "後ろが筆者の主張、言いたいことだから。" },
    { id: 4, cat: "【しかし／だが】", q: "手はどう動かす？", a: "後ろの1文に線を引く。" },
    { id: 5, cat: "【なぜなら】", q: "「なぜなら」「というのも」を見たら？", a: "因果関係。" },
    { id: 6, cat: "【なぜなら】", q: "前と後ろ、どっちに「理由」が書いてある？", a: "後ろ。" },
    { id: 7, cat: "【なぜなら】", q: "何の理由？", a: "直前の文（または傍線部）の理由。" },
    { id: 8, cat: "【なぜなら】", q: "文末はどんな言葉で終わる？", a: "「〜から。」「〜ため。」" },
    { id: 9, cat: "【たとえば】", q: "「たとえば」を見たら？", a: "例示（具体例）の始まり。" },
    { id: 10, cat: "【たとえば】", q: "筆者の「言いたいこと（抽象論）」は前と後ろどっち？", a: "直前の文。" },
    { id: 11, cat: "【たとえば】", q: "では、具体例を読む目的は？", a: "直前の難しいまとめを、分かりやすく理解するため。" },
    { id: 12, cat: "【これ／それ】", q: "「これ」「それ」などの指示語を見たら？", a: "指示内容を指す。" },
    { id: 13, cat: "【これ／それ】", q: "指している内容は、原則として前と後ろどっち？", a: "前。" },
    { id: 14, cat: "【これ／それ】", q: "前のどれくらいの範囲？", a: "直前の1〜2文。" },
    { id: 15, cat: "【これ／それ】", q: "探した後はどうやって確かめる？", a: "指示語の場所にその言葉を当てはめて、意味が通るか読む。" }
];

let currentQuestions = [];
let currentIndex = 0;
let currentMode = 'all'; // 'all' or 'wrong'

// ローカルストレージから×のリストを取得（なければ空の配列）
let wrongList = JSON.parse(localStorage.getItem('for_wrong_list')) || [];

function updateWrongCountDisplay() {
    document.getElementById('wrong-count').innerText = wrongList.length;
}

function initGame() {
    updateWrongCountDisplay();
    if (currentMode === 'all') {
        // 全問をシャッフル
        currentQuestions = [...allQuestions].sort(() => Math.random() - 0.5);
    } else {
        // ✕のIDに一致する問題だけをフィルターしてシャッフル
        currentQuestions = allQuestions.filter(q => wrongList.includes(q.id)).sort(() => Math.random() - 0.5);
    }
    
    currentIndex = 0;
    if (currentQuestions.length === 0) {
        document.getElementById('question-text').innerText = "対象の問題がありません";
        document.getElementById('answer-text').style.display = "none";
        document.getElementById('btn-show').style.display = "none";
        document.getElementById('judge-block').style.display = "none";
        document.getElementById('progress-text').innerText = "0 / 0問";
    } else {
        showQuestion();
    }
}

function showQuestion() {
    const q = currentQuestions[currentIndex];
    document.getElementById('card-meta').innerText = q.cat;
    document.getElementById('question-text').innerText = q.q;
    document.getElementById('answer-text').innerText = q.a;
    
    document.getElementById('answer-text').style.display = "none";
    document.getElementById('btn-show').style.display = "block";
    document.getElementById('judge-block').style.display = "none";
    document.getElementById('progress-text').innerText = `${currentIndex + 1} / ${currentQuestions.length}問`;
}

function showAnswer() {
    document.getElementById('answer-text').style.display = "block";
    document.getElementById('btn-show').style.display = "none";
    document.getElementById('judge-block').style.display = "flex";
}

function handleJudge(isCorrect) {
    const currentId = currentQuestions[currentIndex].id;
    
    if (isCorrect) {
        // ◯なら✕リストから削除
        wrongList = wrongList.filter(id => id !== currentId);
    } else {
        // ✕ならリストに追加（重複なし）
        if (!wrongList.includes(currentId)) {
            wrongList.push(currentId);
        }
    }
    
    // ストレージに保存
    localStorage.setItem('for_wrong_list', JSON.stringify(wrongList));
    updateWrongCountDisplay();
    
    // 次の問題へ
    currentIndex++;
    if (currentIndex < currentQuestions.length) {
        showQuestion();
    } else {
        alert("すべての問題を終了しました！最初に戻ります。");
        initGame();
    }
}

function changeMode(mode) {
    currentMode = mode;
    document.getElementById('mode-all').classList.toggle('active', mode === 'all');
    document.getElementById('mode-wrong').classList.toggle('active', mode === 'wrong');
    initGame();
}

// 起動時に実行
initGame();
</script>

</body>
</html>
