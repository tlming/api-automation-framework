from api.endpoints.base import BaseAPI
from api.response import APIResponse


class UserAPI(BaseAPI):

    def user_list(self) -> APIResponse:
        '''
        GET /users —— 获取所有的user
        '''
        return self._get(path='/users')

    def get_user_by_id(self, user_id: int) -> APIResponse:
        '''
        GET /users/{id} ——通过id获取user信息
        '''
        return self._get(path=f'/users/{user_id}')

    def get_user_posts(self, user_id: int) -> APIResponse:
        '''
        GET /users/{id}/posts   ——通过id获取对应user的post信息
        '''
        return self._get(path=f'/users/{user_id}/posts')

    def get_user_albums(self, user_id: int) -> APIResponse:
        '''
        GET /users/{id}/albums  ——通过id获取对应user的album信息
        '''
        return self._get(path=f'/users/{user_id}/albums')

    def get_user_todos(self, user_id: int) -> APIResponse:
        '''
        GET /users/{id}/todos ——通过id获取对应user的todo信息
        '''
        return self._get(f'/users/{user_id}/todos')

    def create(self, user_data: dict) -> APIResponse:
        '''
        POST /users ——创建user信息
        '''
        return self._post(path='/users', json=user_data)

    def update(self, user_id: int, user_data: dict) -> APIResponse:
        '''
        PUT /users/{id} ——更新user的全部信息
        '''
        return self._put(path=f'/users/{user_id}', json=user_data)

    def patch(self, user_id: int, **kwargs) -> APIResponse:
        '''
        PATCH /users/{id} ——更新user的部分信息
        '''
        return self._patch(path=f'/users/{user_id}', **kwargs)

    def delete(self, user_id: int) -> APIResponse:
        '''
        DELETE /users/{id}   ——通过id删除user
        '''
        return self._delete(f'/users/{user_id}')
