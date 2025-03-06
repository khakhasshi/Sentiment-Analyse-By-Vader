# Reddit 貼文情緒分析工具

## 簡介

本專案是一個 Python 工具，可自動從 Reddit 指定的 Subreddit 中搜尋相關貼文，提取其評論，並使用 VADER 情緒分析工具對評論進行分析，最終輸出分析結果並進行可視化。

## 主要功能

- 搜尋包含特定關鍵字的 Reddit 貼文
- 過濾符合時間條件的貼文（2025 年 3 月 1 日之後發佈的貼文）
- 提取貼文的評論
- 使用 VADER 進行評論情緒分析（Bullish、Neutral、Bearish）
- 將結果保存為 CSV 文件
- 繪製柱狀圖可視化評論情緒分類結果

## 安裝與環境設置

### 1. 安裝 Python

請確保您的環境已安裝 Python 3.7 及以上版本。

### 2. 安裝必要的 Python 套件

使用以下指令安裝所需的 Python 套件：

```sh
pip install praw pandas matplotlib tqdm vaderSentiment
```

## 使用方法

### 1. 配置 Reddit API 憑證

請在 `REDDIT_CLIENT_ID`、`REDDIT_CLIENT_SECRET` 和 `REDDIT_USER_AGENT` 中填入您的 Reddit API 憑證。

### 2. 執行程式碼

直接運行 Python 腳本：

```sh
python reddit_sentiment_analysis.py
```

### 3. 結果輸出

執行後，程式將：

- 抓取符合條件的 Reddit 貼文
- 提取評論並分析情緒
- 生成 CSV 檔案，範例如下：

| Author | Comment                 | Upvotes | Sentiment_Label | Post_ID | Post_URL                   |
| ------ | ----------------------- | ------- | --------------- | ------- | -------------------------- |
| user1  | NVDA 近期表現非常強勁！ | 10      | 1               | abc123  | https://www.reddit.com/... |
| user2  | 我不太看好 NVDA 的未來  | 5       | -1              | abc123  | https://www.reddit.com/... |

- 顯示評論情緒分佈的柱狀圖：
  - `-1` 表示 Bearish（看跌）
  - `0` 表示 Neutral（中性）
  - `1` 表示 Bullish（看漲）

## 可能遇到的錯誤與解決方法

### 1. API 訪問被限制

Reddit API 有頻率限制，若遇到 `429 Too Many Requests`，請稍後再試，或降低請求頻率。

### 2. 貼文或評論無法獲取

可能原因：

- 貼文被刪除或設定為私密
- API 權限不足

請檢查 API 憑證是否正確，或嘗試不同的 Subreddit。

### 3. Matplotlib 中文顯示問題

若在 macOS 上中文無法正常顯示，請安裝 `Arial Unicode MS` 字體，或修改 `plt.rcParams["font.sans-serif"]` 設置。

## 版權與許可

本專案僅供學術與研究使用，請遵守 Reddit API 的使用條款。
