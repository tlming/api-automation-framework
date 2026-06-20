from api.response import APIResponse


class BaseAPI(object):
    def __init__(self, client):
        self.client = client

    def _get(self, path, **kwargs):
        return APIResponse.from_response(self.client.get(path, **kwargs))

    def _post(self, path, **kwargs):
        return APIResponse.from_response(self.client.post(path, **kwargs))

    def _put(self, path, **kwargs):
        return APIResponse.from_response(self.client.put(path, **kwargs))

    def _patch(self, path, **kwargs):
        return APIResponse.from_response(self.client.patch(path, **kwargs))

    def _delete(self, path, **kwargs):
        return APIResponse.from_response(self.client.delete(path, **kwargs))
