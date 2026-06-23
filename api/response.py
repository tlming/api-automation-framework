import json
from dataclasses import dataclass
from requests import Response
from requests.structures import CaseInsensitiveDict

from api.auth import decrypt


@dataclass
class APIResponse:
    status_code: int
    data: dict | list | None
    headers: CaseInsensitiveDict
    raw: Response #保留原始Response数据

    @classmethod
    def from_response(cls, resp: Response,need_decrypt) -> 'APIResponse':
        try:
            data=resp.json() if resp.content else None
        except json.JSONDecodeError:
            data = None

        if need_decrypt and data:
            data=decrypt(data)

        return cls(
            status_code=resp.status_code,
            data=data,
            headers=resp.headers,
            raw=resp
        )