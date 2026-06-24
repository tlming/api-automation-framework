# api-automation-framework

基于 **pytest + requests** 的企业级 REST API 自动化测试框架。采用四层架构设计，集成认证安全管线、多进程并发执行、数据驱动测试、Allure 报告及 Jenkins CI/CD 全流程闭环。

## 技术栈

| 类别 | 技术 |
|------|------|
| 测试框架 | pytest 9.x |
| HTTP 客户端 | requests |
| 数据校验 | Pydantic v2 |
| 测试报告 | Allure |
| 数据驱动 | YAML + @pytest.mark.parametrize |
| 并发执行 | pytest-xdist + filelock |
| CI/CD | Jenkins |
| 消息通知 | ServerChan（企微） |

## 架构

采用**四层架构设计**，各层职责清晰、可独立迭代：

```
tests/                  ← 测试用例层：编写业务场景用例
    │
api/endpoints/          ← 业务封装层：PostsAPI / TodoAPI / UserAPI
    │
api/client.py           ← HTTP 客户端层：封装 requests.Session
    │
api/auth/               ← 认证安全层：Token / 加密 / 签名
```

**请求链路：**

```
测试用例
   → PostsAPI.create(...)          # 业务封装
   → BaseAPI._request()            # 开关控制（加密/签名/Token）
   → ApiClient.post()              # HTTP 调用
   → Authenticator.__call__()      # 拦截器：加密 → 签名 → 附 Token
   → requests.Session.request()    # 真实网络请求
   → APIResponse.from_response()   # 统一响应封装（可选解密）
```

## 核心特性

### 可插拔安全管线
基于 `requests.auth.AuthBase` 实现请求拦截器，在请求发出前依次执行加密、签名、附加 Token。各能力支持**链式调用按需开关**：

```python
# 跳过加密和签名，但保留 Token
client.without_encrypt().without_sign().post("/posts", json={...})
```

### Token 自动管理
- **主动刷新**：Token 过期前自动重新登录获取，避免请求因 Token 过期而失败
- **Double-Checked Locking**：过期判断采用双重检查锁定模式，减少锁竞争

### 多进程并发支持
- 单进程使用 `threading.Lock` 内存锁
- 多进程（pytest-xdist）通过 `filelock` + 共享 JSON 文件实现跨进程 Token 同步
- 文件读取失败自动重试，保障高并发下数据一致性

### 数据驱动测试
- YAML 文件管理测试数据
- `@pytest.mark.parametrize` 动态注入用例
- Pydantic v2 模型编译期校验请求/响应数据结构

### CI/CD 闭环
- Jenkins 自动触发执行
- 多进程并发回归，耗时降低 60%+
- Allure 报告聚合
- ServerChan 企微通知推送

## 快速开始

```bash
# 克隆项目
git clone https://github.com/tlming/api-automation-framework.git
cd api-automation-framework

# 创建虚拟环境
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行全部测试
pytest

# 运行指定测试文件
pytest tests/test_users.py -v

# 多进程并发执行（4进程）
pytest -n 4
```

## 项目结构

```
api-automation-framework/
├── api/                        # API 层
│   ├── auth/                   # 认证与安全模块
│   │   ├── token_manager.py    # Token 管理器（自动刷新 + 并发控制）
│   │   ├── authenticator.py    # 请求拦截器（AuthBase）
│   │   ├── encrypt.py          # 加密（可扩展）
│   │   ├── decrypt.py          # 解密（可扩展）
│   │   └── sign.py             # 签名（可扩展）
│   ├── endpoints/              # 业务端点
│   │   ├── base.py             # BaseAPI 基类
│   │   ├── posts.py            # /posts CRUD
│   │   ├── todos.py            # /todos CRUD
│   │   └── users.py            # /users CRUD
│   ├── client.py               # ApiClient（封装 requests.Session）
│   └── response.py             # 统一响应封装
├── models/                     # Pydantic 数据模型
│   └── user.py                 # User 请求/响应/用例模型
├── tests/                      # 测试用例
│   ├── test_smoke.py           # 冒烟测试
│   ├── test_posts.py           # Posts CRUD（9 条）
│   ├── test_todos.py           # Todos CRUD（7 条，数据驱动）
│   └── test_users.py           # Users CRUD（9 条，Pydantic + 数据驱动）
├── test_data/                  # 测试数据（YAML）
│   ├── todo.yaml
│   └── user.yaml
├── utils/                      # 工具模块
│   ├── config.py               # 配置加载（.env）
│   ├── logger.py               # 日志配置
│   ├── notification.py         # ServerChan 消息推送
│   └── jenkins_utils.py        # Jenkins 环境检测
├── conftest.py                 # pytest 全局 fixtures
├── pytest.ini                  # pytest 配置
├── requirements.txt            # 运行时依赖
└── requirements-dev.txt        # 开发依赖
```

## 配置

通过 `.env.test` 文件配置运行参数：

```ini
BASE_URL=https://jsonplaceholder.typicode.com
TIMEOUT=10
LOGIN_URL=your_login_url
USERNAME=your_username
PASSWORD=your_password
TOEKN_BUFFER_SECONDS=120
```

## 测试覆盖

| 资源 | 文件 | 用例数 | 覆盖维度 |
|------|------|--------|----------|
| Posts | test_posts.py | 9 | CRUD + 边界（不存在/超长） |
| Todos | test_todos.py | 7 | CRUD + 数据驱动参数化 |
| Users | test_users.py | 9 | CRUD + Pydantic 校验 + 参数化 |

覆盖 HTTP 方法：**GET / POST / PUT / PATCH / DELETE**

## CI/CD

在 Jenkins 中运行时会自动检测环境，执行完成后通过 ServerChan 推送测试结论与 Allure 报告链接到企业微信。

```bash
# Jenkins 构建命令
pytest -n 4 --alluredir=reports/allure
```

Jenkins 环境变量：`JENKINS_HOME`、`BUILD_NUMBER`、`JOB_NAME` 等。

## 开发依赖

```bash
pip install -r requirements-dev.txt
```

- black —— 代码格式化
- flake8 —— 代码检查
- pytest-cov —— 覆盖率

## License

MIT