from api.endpoints.base import BaseAPI
from api.response import APIResponse


class TodoAPI(BaseAPI):

    def todo_list(self) -> APIResponse:
        '''
        GET /todos —— 获取所有的todo
        '''
        return self._get(path=f"/todos")

    def get_todo_by_userId(self, user_id: int) -> APIResponse:
        '''
        GET /todos?userId={userId}  ——通过userid获取todo信息
        '''
        return self._get(path=f"/todos?userId={user_id}")

    def get_todo_by_id(self, todo_id) -> APIResponse:
        '''
        GET /todos/{id} ——通过id获取单个todo信息
        '''
        return self._get(path=f"/todos/{todo_id}")

    def create(self, user_id: int, title: str, completed: bool) -> APIResponse:
        '''
        POST /todos ——创建todo
        '''
        return self._post(path='/todos', json={"userId": user_id, "title": title, "completed": completed})

    def update(self, todo_id: int, user_id: int, title: str, completed: bool) -> APIResponse:
        '''
        PUT /todos/{id}   ——通过id更新整个todo的信息
        '''
        return self._put(path=f'/todos/{todo_id}', json={"userId": user_id, "title": title, "completed": completed})

    def patch(self, todo_id: int, **kwargs) -> APIResponse:
        '''
        PATCH /todos/{id}   ——通过id更新部分todo的信息
        '''
        return self._patch(path=f'/todos/{todo_id}', **kwargs)

    def delete(self, todo_id: int) -> APIResponse:
        '''
        DELETE /todos/{id}   ——通过id删除todo
        '''
        return self._delete(path=f'/todos/{todo_id}')
