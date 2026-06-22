# api-automation-framework

JSONPlaceholder API 自动化测试框架。基于 pytest + requests + allure + Jenkins。

## 技术栈

- pytest —— Python 测试框架
- requests —— HTTP 客户端
- allure —— 测试报告
- Jenkins —— CI/CD

## 快速开始

\`\`\`bash
### 拉取项目
git clone https://github.com/tlming/api-automation-framework.git
cd api-automation-framework

### 创建虚拟环境
python -m venv venv

### Windows 激活
venv\Scripts\activate
### Linux / macOS 激活
source venv/bin/activate

### 安装运行时依赖
pip install -r requirements.txt

### 跑测试
pytest
\`\`\`

## 目录结构

\`\`\`
api-automation-framework/
├── api/                  # API 客户端
│   ├── client.py
│   └── endpoints/
├── tests/                # 测试用例
│   └── test_smoke.py
├── utils/                # 工具
├── config/               # 配置
│   └── .env.example
├── reports/              # 测试报告（gitignore）
├── logs/                 # 日志（gitignore）
├── conftest.py
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── .gitignore
├── LICENSE
└── README.md
\`\`\`

## Roadmap

- [x] Day 1: scaffold
- [ ] Day 2: HTTP client
- [ ] Day 3: test cases
- [ ] Day 4: Allure
- [ ] Day 5: CI
- [ ] Day 6: docs
- [ ] Day 7: demo