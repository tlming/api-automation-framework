import logging

import requests

logger = logging.getLogger('__name__')


class ApiClient:

    def __init__(self, base_url, timeout) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        self.timeout = timeout

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
            resp.raise_for_status()
            # 只要上面没报错，说明请求成功，直接在这里返回
            return resp
        except requests.exceptions.RequestException as e:
            logger.error(f"请求出错: {e}")  # 打日志
            return None  # 失败时返回空
