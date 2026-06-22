import json

from requests.auth import AuthBase
from .encrypt import encrypt
from .sign import sign


class Authenticator(AuthBase):
    def __init__(self,token_manager):
        self.token_manager = token_manager
        self._need_encrypt = True
        self._need_sign = True
        self._need_token = True


    def __call__(self, r):

        # 获取本次请求的加密加签加token情况
        need_encrypt = self._need_encrypt
        need_token = self._need_token
        need_sign = self._need_sign

        # 恢复默认值
        self._need_encrypt = True
        self._need_sign = True
        self._need_token = True

        # 仅在请求有body且为POST PUT PATCH时处理加密加签（先加密，再加签）
        if r.body and r.method.upper() in {'POST', 'PUT', 'PATCH'}:
            # 解析原始 Body（requests 中 r.body 是 bytes，需解码）
            body_dict = json.loads(r.body.decode('utf-8'))

            #判断是否需要加密
            if need_encrypt:
                encrypt(body_dict)


            # 判断是否需要加签
            if need_sign:
                sign(body_dict)


            #将加密加签的数据重新放回body里面（重新编码为 bytes）
            r.body= json.dumps(body_dict, ensure_ascii=False).encode('utf-8')

        # 单独处理token
        if need_token:
            token = self.token_manager.get_token()  # 从 TokenManager 拿最新 Token
            r.headers['Authorization'] = f'Bearer {token}'

        return r
