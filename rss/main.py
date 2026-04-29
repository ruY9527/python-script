import argparse
import sys
from rss_fetcher import fetch_from_source, fetch_from_all_sources
from content_parser import fetch_article_content
from email_sender import send_article_email
from config import RSS_SOURCE, validate_config


def main():
    parser = argparse.ArgumentParser(description="RSS外刊邮件推送工具")
    parser.add_argument(
        "--source", "-s",
        type=str,
        default=RSS_SOURCE,
        help="指定RSS源 (e.g., economist, nytimes, guardian, bbc)"
    )
    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="测试模式，不发送邮件"
    )

    args = parser.parse_args()

    # 验证配置
    if not validate_config(args.test):
        sys.exit(1)

    print("=" * 50)
    print("RSS外刊邮件推送工具")
    print("=" * 50)

    # 获取文章
    if args.source == "all":
        print("\n正在从所有RSS源获取最新文章...")
        articles = fetch_from_all_sources()
        if not articles:
            print("错误: 无法从任何RSS源获取文章")
            sys.exit(1)
        article = articles[0]  # 使用第一篇
    else:
        print(f"\n正在从 {args.source} 获取最新文章...")
        article = fetch_from_source(args.source)
        if not article:
            print(f"错误: 无法从 {args.source} 获取文章")
            sys.exit(1)

    print(f"\n✓ 成功获取文章: {article['title']}")
    print(f"  来源: {article['source']}")
    print(f"  作者: {article['author']}")
    print(f"  发布时间: {article['published']}")
    print(f"  链接: {article['link']}")

    # 获取文章正文
    print("\n正在获取文章正文内容...")
    content = fetch_article_content(article["link"])

    if content:
        article["content"] = content
        print("✓ 成功获取文章正文")
    else:
        print("警告: 无法获取文章正文，将使用RSS摘要")
        article["content"] = article["summary"]

    # 测试模式
    if args.test:
        print("\n[测试模式] 邮件内容预览:")
        print(f"  主题: 外刊精读 | {article['title']}")
        print(f"  收件人: (未发送)")
        print("\n✓ 测试完成，邮件未发送")
        return

    # 发送邮件
    print("\n正在发送邮件...")
    success = send_article_email(article)

    if success:
        print("\n✓ 任务完成！")
    else:
        print("\n✗ 邮件发送失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
