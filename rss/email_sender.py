import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from jinja2 import Environment, FileSystemLoader
from typing import Dict


def render_email_template(article_data: Dict) -> str:
    """
    渲染邮件HTML模板

    Args:
        article_data: 文章数据字典

    Returns:
        渲染后的HTML字符串
    """
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("email.html")

    html = template.render(
        title=article_data.get("title", "无标题"),
        source=article_data.get("source", "未知来源"),
        published=article_data.get("published", "未知时间"),
        author=article_data.get("author", "Unknown"),
        summary=article_data.get("summary", "无摘要"),
        content=article_data.get("content", "无内容"),
        link=article_data.get("link", "#")
    )

    return html


def send_email(html_content: str, subject: str) -> bool:
    """
    发送HTML邮件

    Args:
        html_content: HTML邮件内容
        subject: 邮件主题

    Returns:
        发送成功返回True，否则返回False
    """
    from config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL

    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
        print("错误: 邮箱配置不完整，请检查 .env 文件")
        return False

    try:
        # 创建邮件
        msg = MIMEMultipart("alternative")
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = Header(subject, "utf-8")

        # 添加HTML内容
        html_part = MIMEText(html_content, "html", "utf-8")
        msg.attach(html_part)

        # 连接SMTP服务器并发送
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

        print(f"✓ 邮件已成功发送到 {RECEIVER_EMAIL}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("错误: SMTP认证失败，请检查邮箱账号和授权码")
        return False
    except smtplib.SMTPException as e:
        print(f"错误: SMTP发送失败 - {e}")
        return False
    except Exception as e:
        print(f"错误: 发送邮件时出错 - {e}")
        return False


def send_article_email(article_data: Dict) -> bool:
    """
    发送文章邮件

    Args:
        article_data: 文章数据字典

    Returns:
        发送成功返回True，否则返回False
    """
    # 渲染邮件模板
    html_content = render_email_template(article_data)

    # 生成邮件主题
    subject = f"外刊精读 | {article_data.get('title', '今日推荐')}"

    # 发送邮件
    return send_email(html_content, subject)
