# 🖊️ zh-writing-trainer — 中文寫作訓練（小六考試程度）

中文作文資料係**章節精華＋必考元素**。本 app 整合所有教過嘅寫作元素：訓練、提醒、AI 批改。

## 三大模式
| 模式 | 功能 |
|------|------|
| 📖 技巧操練 | 寫作元素 MCQ（描寫方法／修辭／層遞／襯托／首尾呼應／標點／錯別字／記敘文六要素），每題附「記得用」提醒 |
| 🧰 寫作工具箱 | 8 大寫作元素速查（規則＋例句＋提醒＋常見錯誤）＋ 中文作文 Checklist |
| ✍️ 作文任務 | 寫短文（150-250 字）→ AI 按評分準則批改：元素檢查／錯別字標點／評語／升級示範／分數（內容 30%、結構 25%、描寫修辭 25%、標點字詞 20%） |

## 寫作元素（必考）
描寫方法（動作/外貌/語言/心理）｜修辭（比喻/排比/設問/反問）｜層遞｜襯托｜
首尾呼應｜標點符號（對話）｜錯別字（用字義判斷字形）｜記敘文六要素＋段落結構

## 執行
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 測試
```bash
python3 _smoke_test.py
```

## AI 批改配置（Settings → Secrets）
```toml
OPENAI_API_KEY = "..."
OPENAI_MODEL_NAME = "qwen3.8-flash"
OPENAI_API_BASE = "https://api.silra.cn/v1"
```
