#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🖊️ 中文寫作訓練 — 作文技巧操練・工具箱・AI 批改（小六考試程度）

中文作文資料係章節精華（必考元素）：描寫方法、修辭手法（比喻/排比/設問/反問）、
層遞、襯托、首尾呼應、標點符號、錯別字、記敘文六要素。

三種模式：
  📖 技巧操練 — 寫作元素 MCQ（附「記得用」提醒）
  🧰 寫作工具箱 — 寫作元素速查 + 中文作文 Checklist
  ✍️ 作文任務 — 寫短文 → AI 按評分準則批改＋評語
"""

import os
import json
import re
import random
import requests
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "zh_writing_bank.json"), encoding="utf-8") as f:
    QUESTION_BANK = json.load(f)

st.set_page_config(page_title="🖊️ 中文寫作訓練", page_icon="🖊️", layout="wide")

if hasattr(st, "secrets") and len(st.secrets) > 0:
    for k in st.secrets.keys():
        os.environ[k] = str(st.secrets[k])

def get_api_config():
    base = os.environ.get("OPENAI_API_BASE", "").rstrip("/")
    key = os.environ.get("OPENAI_API_KEY", "") or os.environ.get("SILRA_API_KEY", "")
    model = os.environ.get("OPENAI_MODEL_NAME", "") or os.environ.get("MODEL_NAME", "qwen3.8-flash")
    if not base:
        silra_url = os.environ.get("SILRA_API_URL", "")
        if silra_url:
            base = silra_url.replace("/chat/completions", "").rstrip("/")
    if not base:
        base = "https://api.silra.cn/v1"
    return base, key, model

def silra_chat(messages, max_tokens=2000):
    base, key, model = get_api_config()
    if not key:
        return None
    try:
        resp = requests.post(
            f"{base}/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0.5},
            timeout=120,
        )
        try:
            return resp.json()["choices"][0]["message"]["content"]
        except Exception:
            body = (resp.text or "").strip()[:200]
            st.error(f"❌ API 回應格式錯誤（HTTP {resp.status_code}）：{body or '（空回應）'}")
            st.caption("💡 常見原因：API key 無效／API 地址或模型名稱唔啱（Settings → Secrets）")
            return None
    except Exception as e:
        st.error(f"❌ 連接出錯：{e}")
        return None

# ===== 寫作元素工具箱（章節精華＝必考）=====
TOOLS = [
    {
        "id": "describe",
        "name": "🎭 描寫方法四式",
        "rule": "動作描寫（坐、跑、撿等動詞）、外貌描寫（頭髮灰白、一臉慈祥）、語言描寫（對白）、心理描寫（內心想法）。睇描寫方法 → 推性格特點。",
        "examples": [
            "動作：他低頭道歉，決定改過。→ 知錯能改",
            "外貌＋語言：「頭髮灰白、一臉慈祥」＋「不要着急」→ 友善",
            "心理：他心想一定要堅持下去。→ 堅毅",
        ],
        "remind": "✏️ 寫作提醒：寫人最少用兩種描寫方法（例：外貌＋語言＋動作）。",
        "mistake": "⚠️ 常見錯誤：淨係敘事冇描寫；描寫方法同性格對唔上",
    },
    {
        "id": "rhetoric",
        "name": "✨ 修辭手法",
        "rule": "比喻（甲似乙）、排比（三句或以上結構相似）、設問（自問自答）、反問（問嘅形式表肯定/否定，唔使答）。",
        "examples": [
            "比喻：他的笑容像陽光一樣溫暖。",
            "排比：下課了，同學們有的跑步，有的跳繩，有的踢球。",
            "設問：誰是最可愛的人？是我們的白衣天使。",
            "反問：我們怎能忘記老師的恩情呢？（= 不能忘記）",
        ],
        "remind": "✏️ 寫作提醒：最少用兩種修辭，令文章生動。",
        "mistake": "⚠️ 常見錯誤：設問 vs 反問混淆（設問自答；反問唔使答）；比喻本體喻體唔似",
    },
    {
        "id": "climax",
        "name": "🪜 層遞",
        "rule": "三句或以上按程度、次序遞增或遞減排列。",
        "examples": [
            "下課了，操場先是響起零落的掌聲，隨後掌聲此起彼落，最後全場掌聲如雷。",
            "他先學會在水中漂浮，然後練習雙腳打水，最後能獨自游一小段距離。",
        ],
        "remind": "✏️ 寫作提醒：寫場面/過程用層遞令層次分明（首先→隨後→最後）。",
        "mistake": "⚠️ 常見錯誤：兩句唔算層遞（要三句以上）；次序混亂",
    },
    {
        "id": "contrast",
        "name": "🌗 襯托",
        "rule": "用其他事物對比突出主角特點；以景襯人、以人襯人。",
        "examples": [
            "以景襯人：寒風呼嘯，他依然站得筆直。（突出堅守）",
            "以人襯人：旁人紛紛走避，只有他逆行而上。（突出勇敢）",
        ],
        "remind": "✏️ 寫作提醒：寫人嘅精神面貌，用環境/旁人反襯。",
        "mistake": "⚠️ 常見錯誤：襯托對象同主旨無關",
    },
    {
        "id": "echo",
        "name": "🔁 首尾呼應",
        "rule": "結尾回應開頭嘅內容或句子，令結構完整。",
        "examples": [
            "開頭：「又是一個下雨天。」結尾：「雨停了，那個下雨天的溫暖，我永遠記得。」",
        ],
        "remind": "✏️ 寫作提醒：結尾重提開頭嘅物件/場景/句子。",
        "mistake": "⚠️ 常見錯誤：結尾離題；首尾唔呼應",
    },
    {
        "id": "punct",
        "name": "🔣 標點符號（對話）",
        "rule": "對話要用冒號、引號；提示語可放前/中/後；「說」後用逗號或冒號。",
        "examples": [
            "他說：「我一定會做到。」",
            "「不要着急，」他安慰道，「慢慢來。」",
            "「謝謝你！」她感激地說。",
        ],
        "remind": "✏️ 寫作提醒：對白記住引號；感嘆/疑問用相應標點。",
        "mistake": "⚠️ 常見錯誤：漏引號；「說」後標點錯；全篇冇標點",
    },
    {
        "id": "typo",
        "name": "🔤 錯別字（用字義判斷字形）",
        "rule": "同音錯字（走投無路、川流不息）、形近錯字（璧≠壁、苟≠荀）、成語典故（鍥而不捨）。",
        "examples": [
            "玉璧→璧、牆壁→壁（用字義判斷字形）",
            "走投無路（投）唔係走頭無路；川流不息（川）唔係穿流不息",
        ],
        "remind": "✏️ 寫作提醒：寫完檢查成語同易錯字。",
        "mistake": "⚠️ 常見錯誤：再接再厲（厲）、興高采烈（采）、全神貫注（貫）",
    },
    {
        "id": "structure",
        "name": "🏗️ 記敘文六要素＋段落結構",
        "rule": "六要素：時間、地點、人物、起因、經過、結果。結構：開頭點題 → 中間寫經過（描寫＋修辭）→ 結尾感受/道理（首尾呼應）。",
        "examples": [
            "開頭點題 → 經過（描寫+修辭）→ 結尾：這件事讓我明白…（道理/感受）",
        ],
        "remind": "✏️ 寫作提醒：檢查六要素齊唔齊；結尾要有感受或道理。",
        "mistake": "⚠️ 常見錯誤：漏地點/起因；結尾冇感受；流水帳冇描寫",
    },
]

DRILLS = [
    ("「下課了，操場先是響起零落的掌聲，隨後掌聲此起彼落，最後全場掌聲如雷。」呢句用咗咩修辭？", ["層遞", "比喻", "反問", "排比"], "層遞", "climax", "✏️ 三句按程度遞增（零落→此起彼落→如雷）＝層遞"),
    ("「他的笑容像陽光一樣溫暖。」呢句用咗咩修辭？", ["比喻", "誇張", "設問", "反問"], "比喻", "rhetoric", "甲似乙＝比喻（笑容似陽光）"),
    ("「我們怎能忘記老師的恩情呢？」呢句係邊種修辭？", ["反問", "設問", "疑問", "比喻"], "反問", "rhetoric", "⚠️ 反問＝問嘅形式表「不能忘記」，唔使答；設問係自問自答"),
    ("「誰是最可愛的人？是我們的白衣天使。」呢句用咗咩修辭？", ["設問", "反問", "比喻", "排比"], "設問", "rhetoric", "自問自答＝設問"),
    ("「他心想：一定要堅持下去。」屬於咩描寫？", ["心理描寫", "動作描寫", "外貌描寫", "語言描寫"], "心理描寫", "describe", "「心想」＝內心想法＝心理描寫"),
    ("「頭髮灰白、一臉慈祥」屬於咩描寫？", ["外貌描寫", "動作描寫", "語言描寫", "心理描寫"], "外貌描寫", "describe", "描寫樣貌特徵＝外貌描寫"),
    ("「他低頭道歉，決定改過。」反映佢邊種性格？", ["知錯能改", "貪玩", "暴躁", "好奇"], "知錯能改", "describe", "動作＋決定 → 知錯能改（描寫方法→性格特點）"),
    ("「下課了，同學們有的跑步，有的跳繩，有的踢球。」呢句用咗咩修辭？", ["排比", "比喻", "層遞", "設問"], "排比", "rhetoric", "三句結構相似並列＝排比（⚠️ 係排比唔係層遞——冇程度遞進）"),
    ("首尾呼應嘅作用係咩？", ["令文章結構完整", "令字數增加", "令描寫生動", "令對話清晰"], "令文章結構完整", "echo", "結尾回應開頭 → 結構完整、主題突出"),
    ("對話「他說＿我一定會做到＿」嘅標點係？", ["他說：「我一定會做到。」", "他說「我一定會做到」。", "他說，我一定會做到。", "他說：我一定會做到。"], "他說：「我一定會做到。」", "punct", "「說」後用冒號＋引號包對話"),
    ("下列詞語邊個寫錯咗？", ["走頭無路", "走投無路", "再接再厲", "興高采烈"], "走頭無路", "typo", "⚠️ 正確係「走投無路」（投奔無路）；用字義判斷字形"),
    ("「完壁歸趙」邊個字錯？正確寫法係？", ["壁 → 璧", "趙 → 棹", "完 → 元", "冇錯"], "壁 → 璧", "typo", "玉璧→璧（玉石），牆壁→壁；用字義判斷"),
    ("記敘文六要素唔包括邊項？", ["修辭手法", "時間", "地點", "人物"], "修辭手法", "structure", "六要素：時間、地點、人物、起因、經過、結果（修辭係技巧唔係要素）"),
    ("記敘文嘅結尾應該有咩？", ["感受或道理", "長長嘅對話", "新的人物", "問答題"], "感受或道理", "structure", "結尾要有感受/道理，最好首尾呼應"),
    ("以「寒風呼嘯，他依然站得筆直」突出人物堅守，係咩手法？", ["襯托", "比喻", "排比", "設問"], "襯托", "contrast", "以景襯人＝襯托（環境反襯人物精神）"),
    ("「先學會漂浮，然後練習打水，最後能獨自游水」呢種寫法係？", ["層遞", "排比", "比喻", "反問"], "層遞", "climax", "按次序遞進（先→然後→最後）＝層遞"),
    ("寫人嘅作文，最少應該用幾多種描寫方法？", ["兩種或以上", "一種", "不用描寫", "只用對話"], "兩種或以上", "describe", "例：外貌＋語言＋動作，人物先立體"),
    ("「他說：「不要着急，」他安慰道，「慢慢來。」」呢句提示語喺邊度？", ["中間", "開頭", "結尾", "冇提示語"], "中間", "punct", "提示語（他安慰道）可以放對話中間，前後都要引號"),
]

TASKS = [
    {
        "id": "narrative",
        "name": "📖 命題記敘文：難忘的一件事",
        "prompt": "題目：難忘的一件事\n請寫一篇記敘文（150-250 字），記述一件令你難忘的事。",
        "must": ["六要素齊備（時間、地點、人物、起因、經過、結果）", "最少 2 種描寫方法（外貌/動作/語言/心理）", "最少 2 種修辭（比喻/排比/設問/反問/層遞）", "首尾呼應", "結尾有感受或道理", "書面語、標點正確"],
    },
    {
        "id": "picture",
        "name": "🖼️ 睇圖作文",
        "prompt": "根據你見到/想像嘅畫面寫一篇短文（150-250 字）：圖中人物做緊乜？點解？結果點？（可用你自己嘅圖片情境，例：雨中讓傘、比賽跌倒再起、幫助長者）",
        "must": ["六要素齊備", "最少 2 種描寫方法", "最少 1 種修辭", "場面描寫用層遞或襯托", "結尾有感受", "書面語、標點正確"],
    },
    {
        "id": "person",
        "name": "👤 寫人：我最敬佩的人",
        "prompt": "題目：我最敬佩的人\n請寫你最敬佩嘅人（150-250 字），通過事件反映佢嘅性格。",
        "must": ["用事件反映性格（唔好淨係口頭讚）", "最少 2 種描寫方法", "用襯托突出人物特點", "首尾呼應", "結尾有感受", "書面語、標點正確"],
    },
]

def ai_review(task, text):
    must = "；".join(task["must"])
    prompt = (
        "你是小六中文寫作老師。請批改以下中文作文（小六程度，書面語）。\n"
        f"任務：{task['name']}\n要求元素：{must}\n\n學生作文：\n{text}\n\n"
        "請按以下格式用書面語廣東話回覆：\n"
        "【元素檢查】逐項列出要求元素 ✅/❌\n"
        "【錯別字和標點】列出錯誤（原句 → 改正）\n"
        "【內容與結構評語】2-3 句總評（做得好＋要改善）\n"
        "【升級示範】揀 1-2 句改寫成更好版本（用上教過嘅修辭/描寫）\n"
        "【分數】按內容 30%、結構 25%、描寫修辭 25%、標點字詞 20% 評分，滿分 100 分"
    )
    return silra_chat([{"role": "user", "content": prompt}], max_tokens=2000)

# ===== Sidebar =====
with st.sidebar:
    st.header("⚙️ 模式")
    mode = st.radio("揀模式", ["📖 技巧操練", "🧰 寫作工具箱", "✍️ 作文任務（AI 批改）"], key="zw_mode")

st.title("🖊️ 中文寫作訓練")
st.caption("小六作文考試 — 章節精華元素（描寫方法／修辭／層遞／襯托／首尾呼應／標點／錯別字／記敘文六要素）")

def _norm_zh(s):
    """正規化：去空白標點，用嚟寬鬆比對答案"""
    if s is None:
        return ""
    s = re.sub(r"[\s，。、；：！？「」『』（）()…—…]+", "", str(s))
    return s.strip()

def _match_option(ans, opts):
    """模糊比對答案同選項：正規化一致優先，再退 A/B/C/D 代號、單向包含（選項≥2字）"""
    na = _norm_zh(ans)
    if not na:
        return None
    for o in opts:
        if _norm_zh(o) == na:
            return o
    if na.upper() in ("A", "B", "C", "D") and len(opts) == 4:
        return opts["ABCD".index(na.upper())]
    for o in opts:
        no = _norm_zh(o)
        if len(no) >= 2 and no in na:
            return o
    return None

def ai_generate_drills(topics, count):
    """✨ AI 生成新題：根據所選 topic 嘅寫作元素生成書面語題目（含主旨辨析 1-2 小段題型）"""
    base, key, model = get_api_config()
    if not key:
        st.error("⚠️ 未偵測到 API key — 請設定 OPENAI_API_KEY（app Settings → Secrets）")
        return []
    topic_desc = "；".join(f"{QUESTION_BANK[t]['name']}" for t in topics)
    prompt = (
        "你是小六中文寫作科出題老師。根據以下寫作元素範疇出題："
        f"{topic_desc}\n\n"
        "要求：\n"
        "1. 全部題目必須用**正式書面語（繁體中文）**，唔准用口語（嘅/喺/咗/係/唔/啲/佢/嘢）。\n"
        "2. 題型：四選一選擇題（type=mcq）。如果範疇係「主旨辨析」，題目要包含 1-2 小段文字（用【段落】開頭），考學生分辨主題；其他範疇就出常規知識題。\n"
        "3. 每題 4 個選項：1 個正確 + 3 個「似層層」干擾項（同範疇、常見混淆，唔好太易排除）。\n"
        "4. answer 必須同其中一個 options **字面完全一樣**（原字照抄，唔准加 A/B/C/D 前綴）。\n"
        "5. 答案唔准直接出現喺題目文字入面（主旨辨析題：主旨詞唔可以喺段落度寫出）。\n"
        "6. 每題附 hint（審題技巧：教學生點樣分析、搵關鍵句）同 trap（指出常見陷阱／誤導位）。\n"
        "7. 單一答案鐵律：每題只有一個正確答案；有兩個合理答案就要改題目。\n"
        "8. 只准用教材已有嘅寫作知識點，唔可以作新事實。\n\n"
        "輸出格式（只輸出 JSON array，唔好有其他文字）：\n"
        '[{"type":"mcq","question":"...","options":["...","...","...","..."],"answer":"...","hint":"...","trap":"..."}]'
    )
    out = silra_chat([{"role": "user", "content": prompt}], max_tokens=3000)
    if not out:
        return []
    m = re.search(r"\[.*\]", out, re.S)
    if not m:
        return []
    try:
        data = json.loads(m.group(0))
    except Exception:
        return []
    if not isinstance(data, list):
        return []
    valid = []
    for item in data:
        q = str(item.get("question") or "").strip()
        opts = [str(o).strip() for o in (item.get("options") or []) if str(o).strip()]
        ans = str(item.get("answer") or "").strip()
        hint = str(item.get("hint") or "").strip()
        trap = str(item.get("trap") or "").strip()
        if len(opts) != 4 or not q:
            continue
        matched = _match_option(ans, opts)
        if matched is None:
            continue
        # 答案唔准漏喺題目
        if len(matched) >= 2 and _norm_zh(matched) in _norm_zh(q):
            continue
        # 統一 5 元組格式 [q, opts, ans, tid, hint]（同教材題一致，render 先啱）
        valid.append([q, opts, matched, "ai", hint + ("｜" + trap if trap else "")])
    # 答案多樣性
    n_distinct = len({v[2] for v in valid})
    max_repeat = max(1, -(-count // n_distinct)) if n_distinct else 1
    used = {}
    out_q = []
    for v in valid:
        if len(out_q) >= count:
            break
        a = v[2]
        if used.get(a, 0) < max_repeat:
            used[a] = used.get(a, 0) + 1
            out_q.append(v)
    return out_q[:count]

def build_drill_round(topics, count):
    """由所選 topic 題庫 + 常設 DRILLS 抽題；答案詞去重，優先覆蓋唔同詞"""
    pool = []
    for t in topics:
        for item in QUESTION_BANK[t]["questions"]:
            _, q, ans, opts, hint = item
            pool.append([q, list(opts), ans, t, hint])
    pool += DRILLS
    random.shuffle(pool)
    # 答案多樣性：同一答案詞最多 ceil(count/唔同詞數) 次
    n_distinct = len({p[2] for p in pool})
    max_repeat = max(1, -(-count // n_distinct)) if n_distinct else 1
    used = {}
    out = []
    for p in pool:
        if len(out) >= count:
            break
        a = p[2]
        if used.get(a, 0) < max_repeat:
            used[a] = used.get(a, 0) + 1
            out.append(p)
    return out[:count]

if mode == "📖 技巧操練":
    if "zw_q" not in st.session_state:
        st.session_state.zw_q = []
        st.session_state.zw_checked = False
    gen_mode = st.radio("生成模式", ["📖 教材原題（即時）", "✨ AI 生成新題（書面語）"], key="zw_genmode")
    st.markdown("**揀 Topic（可多選；教材模式會自動加入常設綜合題）：**")
    topics = st.multiselect(
        "Topic",
        list(QUESTION_BANK.keys()),
        format_func=lambda k: QUESTION_BANK[k]["name"],
        default=list(QUESTION_BANK.keys())[:4],
        key="zw_topics",
        label_visibility="collapsed",
    )
    count = st.slider("每輪題數", 5, 20, 10, key="zw_count")
    if st.button("🎲 生成操練題", type="primary"):
        if not topics:
            st.warning("⚠️ 請揀至少一個 Topic")
        elif gen_mode.startswith("✨"):
            with st.spinner("✨ AI 生成緊書面語新題…（約 10–30 秒）"):
                qs = ai_generate_drills(topics, count)
            if qs:
                st.session_state.zw_q = qs
                st.session_state.zw_checked = False
                st.rerun()
            else:
                st.error("❌ AI 生成唔到合格題目 — 再試一次？")
        else:
            st.session_state.zw_q = build_drill_round(topics, count)
            st.session_state.zw_checked = False
            st.rerun()
    qs = st.session_state.zw_q
    if not qs:
        st.info("👈 揀 Topic → 㩒「生成操練題」開始！每題附「記得用」提醒。")
    else:
        for i, (q, opts, ans, tid, hint) in enumerate(qs):
            st.markdown(f"**{i+1}.** {q}")
            st.radio(" ", opts, key=f"zw_a{i}", index=None, label_visibility="collapsed")
        if not st.session_state.zw_checked:
            if st.button("✅ 檢查答案", type="primary"):
                st.session_state.zw_checked = True
                st.rerun()
        else:
            correct = 0
            for i, (q, opts, ans, tid, hint) in enumerate(qs):
                user = st.session_state.get(f"zw_a{i}")
                ok = user == ans
                if ok:
                    correct += 1
                    st.success(f"**{i+1}.** ✅ {user}")
                else:
                    st.error(f"**{i+1}.** ❌ 你答：「{user or '（未作答）'}」　正確答案：**{ans}**")
                st.caption(f"💡 {hint}")
            st.metric("🏆 得分", f"{correct} / {len(qs)}")

elif mode == "🧰 寫作工具箱":
    st.subheader("🧰 寫作元素速查（寫作前睇一次）")
    for t in TOOLS:
        with st.expander(t["name"]):
            st.markdown(f"**規則：** {t['rule']}")
            for e in t["examples"]:
                st.markdown(f"- {e}")
            st.info(t["remind"])
            st.caption(t["mistake"])
    st.subheader("✅ 中文作文 Checklist")
    for item in ["六要素齊備（時間、地點、人物、起因、經過、結果）", "開頭點題", "最少 2 種描寫方法", "最少 2 種修辭",
                 "首尾呼應", "結尾有感受或道理", "書面語（唔用口語）", "標點正確（對白引號）", "檢查錯別字"]:
        st.checkbox(item, key=f"zck_{item}")

else:  # ✍️ 作文任務
    task_names = [t["name"] for t in TASKS]
    choice = st.selectbox("揀作文任務", task_names, key="zw_task")
    task = next(t for t in TASKS if t["name"] == choice)
    st.subheader(task["name"])
    st.markdown(task["prompt"])
    st.markdown("**📋 必用元素：** " + "｜".join(task["must"]))
    text = st.text_area("✍️ 你嘅作文：", height=260, placeholder="請用書面語寫作（150-250 字）")
    chars = len(re.sub(r"\s", "", text))
    st.caption(f"字數：{chars}（目標 150-250）")
    if st.button("🤖 AI 批改", type="primary"):
        if chars < 40:
            st.warning("⚠️ 作文太短，寫長少少先批改（建議 150 字以上）")
        else:
            with st.spinner("🤖 AI 批改緊…"):
                out = ai_review(task, text)
            if out:
                st.subheader("📝 批改結果")
                st.markdown(out)
