# python-script

Python 脚本工具集合，包含日常开发中常用的模块和脚本。

## 项目结构

| 模块名字     | 模块作用                  | 备注说明             |
| ------------ | ------------------------- | -------------------- |
| basic        | Python 基础语法学习       | 多线程、网络、GUI 等 |
| datafiles    | 数据文件读写处理          | PDF、Word、Excel 等  |
| db           | 数据库操作                | MySQL、Hive、Kafka   |
| flask        | Flask Web 框架示例        | REST API 开发        |
| geo          | 地理空间操作              | 城市经纬度数据       |
| images       | 图片处理                  | 图片下载、处理       |
| jenkins      | Jenkins CI/CD 操作        |                      |
| pandas       | Pandas 数据分析           |                      |
| pdf          | PDF 文件处理              | PDF 转 Markdown 等   |
| ppt          | PPT 文件处理              |                      |
| reptile      | 网络爬虫                  |                      |
| ai_chat      | AI 聊天接口               | 通义千问、OpenAI     |

## 独立脚本

| 文件                    | 功能描述                                       |
| ----------------------- | ---------------------------------------------- |
| `excel_to_json.py`      | Excel 转 JSON，支持条件过滤                    |
| `xml_dependency_parser.py` | 解析 Maven pom.xml，提取依赖并生成报告       |

## 快速使用

### Excel 转 JSON

```python
from excel_to_json import excel_to_json_with_filter

# 简单过滤
data = excel_to_json_with_filter('data.xlsx', filter_conditions={'状态': '有效'})

# 函数过滤
data = excel_to_json_with_filter('data.xlsx', filter_conditions={'金额': lambda x: x > 1000})
```

### Maven 依赖解析

```bash
# 解析指定目录的 pom.xml
python xml_dependency_parser.py /path/to/project -o output.txt -j output.json
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 依赖说明

依赖已按功能分组管理，详见 `requirements.txt`：
- 数据处理（pandas, numpy, openpyxl 等）
- 数据库（pymysql, SQLAlchemy 等）
- 中间件（kafka-python, redis）
- Web 框架（flask）
- PDF/Office 文档处理
- 网络请求与爬虫
- NLP 与 AI

## 许可证

MIT License