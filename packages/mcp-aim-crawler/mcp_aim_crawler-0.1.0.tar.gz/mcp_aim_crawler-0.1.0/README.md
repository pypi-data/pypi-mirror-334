# MCP Aim Crawler

这是一个基于MCP协议的网站爬虫项目。

## 项目结构

```
mcp_aim_crawler/
├── tests/                # 测试用例目录
└── mcp_aim_crawler/     # 主要源代码目录
    ├── crawler.py       # 爬虫核心逻辑
    └── logger.py        # 日志配置
```

## 环境要求

- Python 3.12.9
- Poetry
- pyenv

## 安装方法

1. 使用pyenv安装Python 3.12.9:
```bash
pyenv install 3.12.9
pyenv local 3.12.9
```

2. 安装项目依赖:
```bash
poetry install
```

## 运行方法

```bash
poetry run python -m mcp_aim_crawler
```

## 环境变量

在项目根目录创建 `.env` 文件，包含以下配置:

- `WEBSITE_URL`: 目标网站URL
- `USERNAME`: 登录用户名
- `PASSWORD`: 登录密码
- `MCP_TOKEN`: MCP令牌 