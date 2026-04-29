import os
import sys

# 尝试加载本地.env文件（本地开发用）
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # GitHub Actions环境下可能没有dotenv

# RSS源配置
RSS_SOURCES = {
    "economist": {
        "name": "The Economist",
        "url": "https://www.economist.com/rss",
        "category": "finance"
    },
    "nytimes": {
        "name": "The New York Times",
        "url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "category": "news"
    },
    "guardian": {
        "name": "The Guardian",
        "url": "https://www.theguardian.com/world/rss",
        "category": "news"
    },
    "bbc": {
        "name": "BBC News",
        "url": "http://feeds.bbci.co.uk/news/world/rss.xml",
        "category": "news"
    }
}

# 邮箱配置
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.qq.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# RSS源选择
RSS_SOURCE = os.getenv("RSS_SOURCE", "all")


def validate_config(test_mode: bool = False) -> bool:
    """
    验证配置是否完整

    Args:
        test_mode: 是否为测试模式

    Returns:
        配置有效返回True
    """
    if test_mode:
        return True

    missing = []
    if not SENDER_EMAIL:
        missing.append("SENDER_EMAIL")
    if not SENDER_PASSWORD:
        missing.append("SENDER_PASSWORD")
    if not RECEIVER_EMAIL:
        missing.append("RECEIVER_EMAIL")

    if missing:
        print(f"错误: 缺少必要配置: {', '.join(missing)}")
        print("\n请通过以下方式之一配置:")
        print("  1. 本地开发: 创建 .env 文件")
        print("  2. GitHub Actions: 在仓库 Settings > Secrets 中配置")
        return False

    return True
