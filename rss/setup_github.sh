#!/bin/bash

# GitHub Secrets 配置脚本
# 使用前请先安装 GitHub CLI: https://cli.github.com/

echo "=========================================="
echo "GitHub Secrets 配置工具"
echo "=========================================="
echo ""

# 检查 gh 是否安装
if ! command -v gh &> /dev/null; then
    echo "错误: 未安装 GitHub CLI"
    echo "请先安装: https://cli.github.com/"
    echo ""
    echo "安装命令:"
    echo "  brew install gh    # macOS"
    echo "  winget install gh  # Windows"
    exit 1
fi

# 检查是否已登录
if ! gh auth status &> /dev/null; then
    echo "请先登录 GitHub CLI:"
    gh auth login
fi

# 获取仓库信息
echo "请输入 GitHub 仓库 (格式: owner/repo):"
read REPO

if [ -z "$REPO" ]; then
    echo "错误: 仓库名称不能为空"
    exit 1
fi

echo ""
echo "请输入以下配置信息:"
echo ""

# SMTP服务器
echo "SMTP服务器 (默认: smtp.qq.com):"
read SMTP_SERVER
SMTP_SERVER=${SMTP_SERVER:-smtp.qq.com}

# SMTP端口
echo "SMTP端口 (默认: 465):"
read SMTP_PORT
SMTP_PORT=${SMTP_PORT:-465}

# 发件人邮箱
echo "发件人QQ邮箱:"
read SENDER_EMAIL

# QQ邮箱授权码
echo "QQ邮箱授权码 (不是QQ密码):"
read -s SENDER_PASSWORD
echo ""

# 收件人邮箱
echo "收件人邮箱:"
read RECEIVER_EMAIL

echo ""
echo "=========================================="
echo "配置摘要"
echo "=========================================="
echo "仓库: $REPO"
echo "SMTP服务器: $SMTP_SERVER"
echo "SMTP端口: $SMTP_PORT"
echo "发件人: $SENDER_EMAIL"
echo "收件人: $RECEIVER_EMAIL"
echo ""
echo "确认配置? (y/n)"
read CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "已取消"
    exit 0
fi

echo ""
echo "正在配置 GitHub Secrets..."

# 设置 Secrets
gh secret set SMTP_SERVER -b "$SMTP_SERVER" -R "$REPO"
gh secret set SMTP_PORT -b "$SMTP_PORT" -R "$REPO"
gh secret set SENDER_EMAIL -b "$SENDER_EMAIL" -R "$REPO"
gh secret set SENDER_PASSWORD -b "$SENDER_PASSWORD" -R "$REPO"
gh secret set RECEIVER_EMAIL -b "$RECEIVER_EMAIL" -R "$REPO"

echo ""
echo "=========================================="
echo "✓ 配置完成！"
echo "=========================================="
echo ""
echo "接下来:"
echo "1. 进入仓库 Actions 页面"
echo "2. 启用 Workflows"
echo "3. 点击 'RSS外刊邮件推送' > 'Run workflow' 测试"
echo ""
echo "自动运行时间: 每天北京时间 08:00"
