# 游戏点赞量监控系统

自动监控游戏网站的点赞量变化，并通过微信推送每日和每周的TOP10增长游戏。

## 功能特点

- 🕷️ **自动爬取**: 使用Selenium自动抓取游戏点赞数据
- 📊 **数据分析**: 计算每日和每周的点赞增长量
- 📱 **微信推送**: 通过企业微信机器人推送报告
- ⏰ **定时执行**: 使用GitHub Actions每天早上7点自动运行
- 📈 **排行榜**: 自动生成TOP10增长游戏排行榜

## 监控网站

- https://azgames.io/new-games
- 可以轻松添加更多网站

## 快速开始

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd game_Statistics
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并填入你的配置:

```bash
cp .env.example .env
```

编辑 `.env` 文件:

```env
WECHAT_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY_HERE
```

### 4. 获取企业微信机器人Webhook

1. 在企业微信群中添加机器人
2. 获取Webhook URL
3. 将URL填入 `.env` 文件

详细步骤: [企业微信机器人配置文档](https://developer.work.weixin.qq.com/document/path/91770)

### 5. 本地测试

```bash
python main.py
```

## GitHub Actions 配置

### 1. 设置Secrets

在GitHub仓库中设置以下Secrets:

- `WECHAT_WEBHOOK_URL`: 企业微信机器人的Webhook URL

设置路径: `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`

### 2. 启用Actions

1. 进入仓库的 `Actions` 标签页
2. 启用GitHub Actions
3. 工作流将在每天北京时间早上7点自动运行

### 3. 手动触发

在 `Actions` 标签页中，选择 `游戏点赞量每日监控` 工作流，点击 `Run workflow` 可以手动触发。

## 项目结构

```
game_Statistics/
├── .github/
│   └── workflows/
│       └── daily_monitor.yml    # GitHub Actions工作流
├── data/                         # 数据存储目录（自动创建）
│   ├── history.json             # 历史数据
│   ├── daily_stats.json         # 每日统计
│   └── weekly_stats.json        # 每周统计
├── scraper.py                   # 爬虫模块
├── data_manager.py              # 数据管理模块
├── wechat_notifier.py           # 微信通知模块
├── main.py                      # 主程序
├── requirements.txt             # Python依赖
├── .env.example                 # 环境变量示例
├── .gitignore                   # Git忽略文件
└── README.md                    # 项目文档
```

## 数据说明

### 历史数据 (history.json)

存储最近30天的所有抓取记录，每条记录包含:
- 时间戳
- 游戏列表（名称、URL、点赞数）

### 统计数据

- `daily_stats.json`: 每日TOP10增长游戏
- `weekly_stats.json`: 每周TOP10增长游戏

## 报告格式

### 每日报告

每天早上7点发送，包含:
- 📊 当日TOP10增长游戏
- 当前点赞数
- 昨日点赞数
- 增长量

### 每周报告

每周一早上7点发送，包含:
- 📊 本周TOP10增长游戏
- 当前点赞数
- 7天前点赞数
- 增长量

## 添加新网站

编辑 `main.py` 文件，在 `urls` 列表中添加新的网站URL:

```python
urls = [
    'https://azgames.io/new-games',
    'https://example.com/games',  # 添加新网站
]
```

## 自定义配置

### 修改执行时间

编辑 `.github/workflows/daily_monitor.yml` 文件中的 cron 表达式:

```yaml
schedule:
  # 当前: 每天北京时间早上7点 (UTC 23点)
  - cron: '0 23 * * *'
  
  # 示例: 每天北京时间早上8点 (UTC 0点)
  # - cron: '0 0 * * *'
```

### 修改TOP数量

编辑 `main.py` 文件中的切片数量:

```python
daily_top10 = daily_increases[:10]  # 改为 [:20] 获取TOP20
```

## 故障排除

### 1. 爬虫无法获取数据

- 检查网站是否可访问
- 检查网站结构是否发生变化
- 查看Chrome浏览器是否正确安装

### 2. 微信通知发送失败

- 检查Webhook URL是否正确
- 检查机器人是否被移除
- 查看企业微信机器人配置

### 3. GitHub Actions失败

- 查看Actions日志
- 检查Secrets是否正确配置
- 确认仓库有写入权限

## 技术栈

- **Python 3.10+**
- **Selenium**: 网页自动化
- **Chrome WebDriver**: 浏览器驱动
- **企业微信机器人**: 消息推送
- **GitHub Actions**: 定时任务

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request!

## 联系方式

如有问题，请提交Issue或联系维护者。
