# PTT Job Alert Bot 🚀

這是一個基於 Python 開發的自動化求職追蹤工具。它能自動爬取 PTT 特定看板（如 Tech_Job, Soft_Job）的最新職缺，並透過 LINE Messaging API 將符合關鍵字的資訊即時推送到你的手機。

## 專案特色

- **自動化翻頁**：具備智慧翻頁邏輯，可自定義追蹤過去 N 天內的所有文章。
- **精準過濾**：自動識別並過濾 PTT 置頂公告，避免無效資訊干擾。
- **日期校正**：針對 PTT 缺乏年份的日期格式，實作了跨年日期修正邏輯。
- **物件導向設計 (OOP)**：採用類別封裝，結構清晰，易於擴充其他平台（如 Dcard, 104）。
- **資安防護**：使用環境變數（`.env`）管理 API 金鑰，符合業界開發規範。
- **即時通知**：整合 LINE Messaging API，職缺資訊不漏接。

##  函式庫

- **語言**: Python 3.x
- **套件**: 
  - `Requests`: 處理網路請求
  - `BeautifulSoup4`: 解析 HTML DOM 結構
  - `Pandas`: 資料結構化與 CSV 匯出
  - `Line-bot-sdk`: 串接 LINE 官方帳號 API
  - `Python-dotenv`: 環境變數管理

## 📋 安裝與使用步驟

1. **複製專案**
   ```bash
   git clone [https://github.com/ArnoldRan/python_ptt_job_scraper.git](https://github.com/ArnoldRan/python_ptt_job_scraper.git)

2. **建立虛擬環境並安裝套件**
   ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

4. **設定環境變數** 
    建立一個 .env 檔案並填入你的 LINE API 資訊：
    ```plaintext
        LINE_CHANNEL_ACCESS_TOKEN=你的代碼
        LINE_USER_ID=你的用戶ID

6. **執行程式**
   ```bash
    python3 main.py

## 專案結構

.
├── main.py              # 程式主邏輯 (包含 Scraper 與 Notifier 類別)
├── .env                 # 敏感資訊 (不推送到 Git)
├── .gitignore           # 排除不需要的文件
├── requirements.txt     # 套件清單
└── README.md            # 專案說明文件
