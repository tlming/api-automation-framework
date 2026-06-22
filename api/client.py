import logging

import requests

from api.auth.authenticator import Authenticator
from api.auth.token_manager import TokenManager

logger = logging.getLogger('__name__')


class ApiClient:

    def __init__(self, base_url, timeout, token_manager: TokenManager) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        self.timeout = timeout
        # 给session绑定认证器，可用于发送请求前进行拦截，然后进行加密加签，加token
        self.authenticator = Authenticator(token_manager)
        self.session.auth = self.authenticator

    def without_sign(self):
        '''
        关闭加签
        '''
        self.authenticator._need_sign = False
        return self

    def without_encrypt(self):
        '''
        关闭加密
        '''
        self.authenticator._need_encrypt = False
        return self

    def without_token(self):
        '''
        关闭token
        '''
        self.authenticator._need_token = False
        return self

    def get(self, path: str, params: dict = None, **kwargs):
        return self._request(method='GET', path=path, params=params, **kwargs)

    def post(self, path: str, json: dict = None, **kwargs):
        return self._request(method='POST', path=path, json=json, **kwargs)

    def put(self, path: str, json: dict = None, **kwargs):
        return self._request(method='PUT', path=path, json=json, **kwargs)

    def patch(self, path: str, json: dict = None, **kwargs):
        return self._request(method='PATCH', path=path, json=json, **kwargs)

    def delete(self, path: str, **kwargs):
        return self._request(method='DELETE', path=path, **kwargs)

    def _request(self, method: str, path: str, **kwargs):
        url = self.base_url + path
        logger.info(f'{method}:{url}')
        logger.debug(f'request kwargs:{kwargs}')
        try:
            resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
            # 根据状态码分类记录日志
            if 200 <= resp.status_code < 300:
                logger.info(f"请求成功: {resp.status_code}")  # 绿
            elif 400 <= resp.status_code < 500:
                logger.warning(f"客户端错误（请求参数/权限问题）: {resp.status_code}")  # 黄
            elif resp.status_code >= 500:
                logger.error(f"服务器内部错误: {resp.status_code}")  # 红
            return resp
        except requests.exceptions.RequestException as e:
            logger.error(f"请求出错: {e}")  # 打日志
            raise  # 重新抛出异常，让调用者处理
