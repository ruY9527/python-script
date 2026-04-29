import requests
from bs4 import BeautifulSoup
from typing import Optional


def fetch_article_content(url: str) -> Optional[str]:
    """
    从文章URL获取正文内容

    Args:
        url: 文章URL

    Returns:
        清理后的正文HTML，失败返回None
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # 移除不需要的标签
        for tag in soup.find_all(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        # 尝试找到正文内容
        content = None

        # 常见的正文容器选择器
        selectors = [
            "article",
            '[role="main"]',
            ".article-content",
            ".post-content",
            ".entry-content",
            ".story-body",
            "#article-body",
            ".article-body",
            "main"
        ]

        for selector in selectors:
            content = soup.select_one(selector)
            if content:
                break

        if not content:
            # 如果没找到特定容器，使用body
            content = soup.find("body")

        if not content:
            return None

        # 清理内容
        html_content = clean_content(content)
        return html_content

    except Exception as e:
        print(f"错误: 无法获取文章内容 - {e}")
        return None


def clean_content(element) -> str:
    """
    清理和格式化HTML内容

    Args:
        element: BeautifulSoup元素

    Returns:
        清理后的HTML字符串
    """
    # 移除图片（可选，邮件中可能不显示）
    for img in element.find_all("img"):
        img.decompose()

    # 移除广告和无关内容
    for ad in element.find_all(class_=lambda x: x and ("ad" in x.lower() or "advertisement" in x.lower())):
        ad.decompose()

    # 转换为字符串
    html = str(element)

    # 简单的清理
    html = html.replace("\n", " ")
    html = " ".join(html.split())

    return html


def extract_text_summary(html_content: str, max_length: int = 200) -> str:
    """
    从HTML内容提取纯文本摘要

    Args:
        html_content: HTML内容
        max_length: 摘要最大长度

    Returns:
        纯文本摘要
    """
    soup = BeautifulSoup(html_content, "lxml")
    text = soup.get_text(separator=" ", strip=True)

    if len(text) > max_length:
        text = text[:max_length] + "..."

    return text
