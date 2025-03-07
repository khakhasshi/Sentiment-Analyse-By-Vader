import praw
import prawcore
import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tqdm import tqdm
import platform  # Detect operating system
import time
import datetime  # 处理时间

# === Reddit API Configuration ===
REDDIT_CLIENT_ID = ""
REDDIT_CLIENT_SECRET = ""
REDDIT_USER_AGENT = ""

# === Initialize Sentiment Analyzer ===
analyzer = SentimentIntensityAnalyzer()

# === Fix Matplotlib Font Issues (for macOS) ===
if platform.system() == "Darwin":  # macOS
    plt.rcParams["font.sans-serif"] = ["Arial Unicode MS"]  # Use macOS-compatible font
else:  # Windows/Linux
    plt.rcParams["font.sans-serif"] = ["Arial"]
plt.rcParams["axes.unicode_minus"] = False  # Ensure minus signs display correctly

# 设置时间限制（2025年3月1日 00:00 UTC）
TIME_THRESHOLD = datetime.datetime(2025, 1,5).timestamp()

def fetch_posts_by_keywords(subreddit_name, keywords, max_posts=500, search_limit=1000):
    """ 通过多个关键词搜索符合时间范围的帖子（2025年3月1日后） """
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
        )

        post_urls = set()
        with tqdm(total=max_posts, desc="🔍 搜索符合时间要求的帖子") as pbar:
            for keyword in keywords:
                count = 0  # 统计符合条件的帖子数量
                for submission in reddit.subreddit(subreddit_name).search(keyword, limit=search_limit):
                    # 过滤掉时间小于2025年3月1日的帖子
                    if submission.created_utc >= TIME_THRESHOLD and submission.url.startswith("https://www.reddit.com/r/"):
                        post_urls.add(submission.url)
                        count += 1
                        pbar.update(1)

                    if len(post_urls) >= max_posts:
                        break  # 达到 300 条帖子，停止搜索
                
                if len(post_urls) >= max_posts:
                    break  # 达到 300 条帖子，停止搜索
                
                time.sleep(0.1)  # 防止 API 速率限制

        print(f"\n✅ 共获取 {len(post_urls)} 个符合时间要求的帖子")
        return list(post_urls)

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return []

def fetch_post_and_comments(post_url):
    """ 获取 Reddit 帖子及其评论 """
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
        )

        submission = reddit.submission(url=post_url)

        # 打印帖子信息
        print(f"\n📥 处理帖子: {submission.title}")
        print(f"👤 作者: {submission.author} | 👍 {submission.score} | 💬 {submission.num_comments} 条评论")

        submission.comments.replace_more(limit=0)
        comments_data = []

        for comment in submission.comments.list():
            if comment.body:
                comments_data.append([comment.author, comment.body, comment.score])

        if not comments_data:
            print("⚠️ 没有可用评论")
            return None

        df = pd.DataFrame(comments_data, columns=["Author", "Comment", "Upvotes"])
        return df, submission.id

    except prawcore.exceptions.NotFound:
        print("❌ 帖子未找到或已删除")
    except prawcore.exceptions.Forbidden:
        print("❌ 无权限访问该帖子（可能是私密帖子）")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
    return None

def analyze_sentiment(comment):
    """ 计算情绪得分并分类 """
    sentiment_score = analyzer.polarity_scores(str(comment))["compound"]
    if sentiment_score >= 0.4:
        return 1  # Bullish
    elif sentiment_score <= -0.4:
        return -1  # Bearish
    else:
        return 0  # Neutral

def process_multiple_posts(post_urls):
    """ 处理多个帖子，分析评论情绪并可视化 """
    all_data = []

    with tqdm(total=len(post_urls), desc="📊 处理帖子") as pbar:
        for post_url in post_urls:
            result = fetch_post_and_comments(post_url)
            if result:
                df, post_id = result
                tqdm.pandas(desc=f"🔄 分析情绪 {post_id}")
                df["Sentiment_Label"] = df["Comment"].progress_apply(analyze_sentiment)
                df["Post_ID"] = post_id
                df["Post_URL"] = post_url
                all_data.append(df)
            pbar.update(1)

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        filename = "reddit_nvda_sentiment_analysis_2025_mar.csv"
        final_df.to_csv(filename, index=False, encoding="utf-8")
        print(f"\n✅ 所有帖子分析完成，结果已保存到 {filename}")

        # 统计情绪分析结果
        sentiment_counts = final_df["Sentiment_Label"].value_counts().sort_index()

        # 可视化结果
        plt.figure(figsize=(6, 4))
        plt.bar(sentiment_counts.index, sentiment_counts.values, tick_label=["Bearish (-1)", "Neutral (0)", "Bullish (1)"])
        plt.xlabel("Sentiment Category")
        plt.ylabel("Number of Comments")
        plt.title("NVDA 相关情绪分析 (2025年3月之后)")
        plt.show()

# === 运行代码 ===
if __name__ == "__main__":
    subreddit_name = "NvidiaStock"  # 你可以修改为其他 Subreddit
    keywords = ["NVDA", "nvidia", "Nvidia", "NVIDIA"]
    
    post_urls = fetch_posts_by_keywords(subreddit_name, keywords, max_posts=300, search_limit=1000)
    process_multiple_posts(post_urls)
