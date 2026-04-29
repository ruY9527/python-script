# RSS外刊邮件推送工具

自动抓取优质外刊最新文章，渲染成精美HTML邮件，推送到指定邮箱。

## 功能特性

- 支持多个RSS源（经济学人、纽约时报、卫报、BBC）
- 自动提取文章正文内容
- 精美HTML邮件模板
- 支持GitHub Actions定时自动推送
- 支持本地运行和手动触发

## 快速开始

### 方式一：GitHub Actions（推荐）

1. **Fork或上传项目到GitHub**

2. **配置GitHub Secrets**

   进入仓库 `Settings` > `Secrets and variables` > `Actions`，添加以下Secrets：

   | Secret名称 | 说明 | 示例 |
   |-----------|------|------|
   | `SMTP_SERVER` | SMTP服务器 | `smtp.qq.com` |
   | `SMTP_PORT` | SMTP端口 | `465` |
   | `SENDER_EMAIL` | 发件人邮箱 | `your@qq.com` |
   | `SENDER_PASSWORD` | QQ邮箱授权码 | `xxxxxxxxxx` |
   | `RECEIVER_EMAIL` | 收件人邮箱 | `receiver@example.com` |

3. **获取QQ邮箱授权码**

   - 登录QQ邮箱 > 设置 > 账户
   - 开启POP3/SMTP服务
   - 生成授权码（不是QQ密码）

4. **启用GitHub Actions**

   进入仓库 `Actions` 页面，点击 `I understand my workflows, go ahead and enable them`

5. **运行方式**

   - **自动运行**：每天北京时间08:00自动推送
   - **手动运行**：Actions > RSS外刊邮件推送 > Run workflow

### 方式二：本地运行

1. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

2. **配置环境变量**

   ```bash
   cp .env.example .env
   ```

   编辑 `.env` 文件，填入邮箱配置

3. **运行脚本**

   ```bash
   # 测试模式（不发送邮件）
   python main.py --test

   # 发送邮件
   python main.py

   # 指定RSS源
   python main.py --source guardian
   ```

## RSS源列表

| 键名 | 名称 | 分类 |
|------|------|------|
| `economist` | The Economist | 财经 |
| `nytimes` | The New York Times | 新闻 |
| `guardian` | The Guardian | 新闻 |
| `bbc` | BBC News | 新闻 |

## 自定义配置

### 修改定时时间

编辑 `.github/workflows/rss-email.yml`：

```yaml
schedule:
  # 每天北京时间08:00（UTC 0点）
  - cron: '0 0 * * *'

  # 每周一北京时间08:00
  - cron: '0 0 * * 1'
```

### 添加RSS源

编辑 `config.py`，在 `RSS_SOURCES` 中添加：

```python
RSS_SOURCES = {
    # 现有源...
    "new_source": {
        "name": "Source Name",
        "url": "https://example.com/rss",
        "category": "news"
    }
}
```

## 项目结构

```
rss/
├── main.py              # 主程序入口
├── config.py            # 配置管理
├── rss_fetcher.py       # RSS抓取模块
├── content_parser.py    # 内容解析模块
├── email_sender.py      # 邮件发送模块
├── templates/
│   └── email.html       # HTML邮件模板
├── requirements.txt     # 依赖包
├── .env.example         # 环境变量示例
└── .github/
    └── workflows/
        └── rss-email.yml  # GitHub Actions配置
```

## 常见问题

### Q: 为什么某些RSS源获取不到文章？

A: 部分RSS源可能需要代理或有访问限制，脚本会自动跳过并尝试其他源。

### Q: 如何修改邮件模板？

A: 编辑 `templates/email.html` 文件，使用Jinja2模板语法。

### Q: GitHub Actions运行失败怎么办？

A: 检查Actions日志，确认Secrets配置正确，特别是授权码是否过期。

## License

MIT
