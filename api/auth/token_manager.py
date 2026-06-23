import threading
import time

import requests


class TokenManager:
    '''
    token管理器，涉及自动刷新和并发控制
    '''

    def __init__(self, login_url, username, password, token_buffer_seconds):
        self.login_url = login_url
        self.username = username,
        self.password = password,
        self.token_buffer_seconds = token_buffer_seconds  # token过期时间

        self._token = None  # 储存token
        self._expires_date = None  # 过期时间
        self._lock = threading.Lock()  # 锁

        # 预刷新token
        self._refresh_token()

    def _refresh_token(self):

        try:
            resp = requests.post(url=self.login_url, username=self.username, password=self.password, timeout=10)
            data = resp.json()
            new_token = data.get('token')  # 使用字典的get方法，若是无token字段会返回None。若是直接data['token']，无token字段则会报错
            expires_in = data.get('expires_in', 3600)  # expires_in指的是token的有效期，3600是默认值（根据真实的开发动态可变）
            if not new_token:
                raise ValueError("登录接口返回的数据中没有 access_token 字段")
            self._token = new_token
            # 计算token过期时间
            self._expires_date = time.time() + expires_in - self.token_buffer_seconds
        except requests.exceptions.RequestException as e:
            # 这里不吞掉异常，让上层（测试用例）知道鉴权挂了
            raise RuntimeError("无法连接鉴权服务器，请检查网络") from e
        except Exception as e:
            raise RuntimeError("Token 刷新失败，请检查登录接口返回格式") from e

    def get_token(self) -> str:
        # token未过期，直接返回
        if self._is_expired() and self._token is not None:
            return self._token
        # token过期，加锁，用于并发
        with self._lock:
            # 再判断一次token是否过期，因为若是ABC三个线程都在排队，若是A进来时过期，则A会去获取token，当B进来时再判断一下，没过期就直接返回，效率快
            if self._is_expired() and self._token is not None:
                return self._token

            self._refresh_token()
            # 4. 保险起见的最终防御（理论上走不到这里，但防止 _refresh 异常被吞）
            if self._token is None:
                raise RuntimeError("Token 刷新失败，access_token 仍为 None")

            return self._token

    def _is_expired(self) -> bool:
        '''
        通过比较当前时间和self._expires_date查看token是否过期
        '''
        return self._expires_date < time.time()
