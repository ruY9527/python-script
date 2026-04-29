import feedparser
from datetime import datetime
from typing import Optional, Dict, List


def fetch_latest_article(source_key: str, source_config: Dict) -> Optional[Dict]:
    """
    从指定RSS源获取最新一篇文章

    Args:
        source_key: RSS源的键名
        source_config: RSS源配置

    Returns:
        包含文章信息的字典，失败返回None
    """
    try:
        feed = feedparser.parse(source_config["url"])

        if not feed.entries:
            print(f"警告: {source_config['name']} 没有可用的文章")
            return None

        entry = feed.entries[0]

        # 解析发布日期
        published_date = None
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            published_date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d %H:%M")
        elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
            published_date = datetime(*entry.updated_parsed[:6]).strftime("%Y-%m-%d %H:%M")

        # 获取作者
        author = getattr(entry, "author", "Unknown")

        # 获取摘要
        summary = ""
        if hasattr(entry, "summary"):
            summary = entry.summary
        elif hasattr(entry, "description"):
            summary = entry.description

        return {
            "title": entry.title,
            "link": entry.link,
            "author": author,
            "published": published_date,
            "summary": summary,
            "source": source_config["name"]
        }

    except Exception as e:
        print(f"错误: 无法从 {source_config['name']} 获取文章 - {e}")
        return None


def fetch_from_all_sources() -> List[Dict]:
    """
    从所有RSS源获取最新文章

    Returns:
        文章列表
    """
    from config import RSS_SOURCES

    articles = []
    for key, config in RSS_SOURCES.items():
        article = fetch_latest_article(key, config)
        if article:
            articles.append(article)

    return articles


def fetch_from_source(source_key: str) -> Optional[Dict]:
    """
    从指定的RSS源获取最新文章

    Args:
        source_key: RSS源的键名

    Returns:
        文章信息字典，失败返回None
    """
    from config import RSS_SOURCES

    if source_key not in RSS_SOURCES:
        print(f"错误: 未知的RSS源 '{source_key}'")
        print(f"可用的RSS源: {', '.join(RSS_SOURCES.keys())}")
        return None

    return fetch_latest_article(source_key, RSS_SOURCES[source_key])
