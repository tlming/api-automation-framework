from api.response import APIResponse


class BaseAPI(object):
    def __init__(self, client):
        self.client = client

    def _request(self, method, path, need_encrypt: bool = True, need_sign: bool = True, need_token: bool = True,
                 need_decrypt: bool = True, **kwargs):
        """
               统一的请求入口，负责：
               1. 根据开关拼装 client 链（without_token / with_encrypt 等）
               2. 调用底层 client 发送请求
               3. 将响应转换为统一的 APIResponse
        """
        client = self.client
        if not need_encrypt:
            client.without_encrypt()
        if not need_sign:
            client.without_sign()
        if not need_token:
            client.without_token()

        resp = getattr(client, method.lower())(path, **kwargs)
        return APIResponse.from_response(resp,need_decrypt=need_decrypt)

    def _get(self, path, **kwargs):
        return self._request("GET", path, **kwargs)

    def _post(self, path, **kwargs):
        return self._request("POST", path, **kwargs)

    def _put(self, path, **kwargs):
        return self._request("PUT", path, **kwargs)

    def _patch(self, path, **kwargs):
        return self._request("PATCH", path, **kwargs)

    def _delete(self, path, **kwargs):
        return self._request("DELETE", path, **kwargs)
