from models.user import UserRequest


class UserAPI:
    def __init__(self, client):
        self.client = client

    def user_list(self) -> list:
        '''
        GET /users —— 获取所有的user
        '''
        return self.client.get('/users')

    def get_user_by_id(self, user_id: int) -> dict:
        '''
        GET /users/{id} ——通过id获取user信息
        '''
        return self.client.get(f'/users/{user_id}')

    def get_user_posts(self, user_id: int) -> list:
        '''
        GET /users/{id}/posts   ——通过id获取对应user的post信息
        '''
        return self.client.get(f'/users/{user_id}/posts')

    def get_user_albums(self, user_id: int) -> list:
        '''
        GET /users/{id}/albums  ——通过id获取对应user的album信息
        '''
        return self.client.get(f'/users/{user_id}/albums')

    def get_user_todos(self, user_id: int) -> list:
        '''
        GET /users/{id}/todos ——通过id获取对应user的todo信息
        '''
        return self.client.get(f'/users/{user_id}/todos')

    def create(self, payload: UserRequest) -> dict:
        '''
        POST /users ——创建user信息
        '''
        body = payload.model_dump(exclude_unset=True)  # 将Pydantic模型转换为json字典
        return self.client.post('/users', json=body)

    def update(self, user_id, payload: UserRequest) -> dict:
        '''
        PUT /users/{id} ——更新user的全部信息
        '''
        body = payload.model_dump(exclude_unset=True)  # 将Pydantic模型转换为json字典
        return self.client.put(f'/users/{user_id}', json=body)

    def patch(self, user_id, payload: UserRequest) -> dict:
        '''
        PATCH /users/{id} ——更新user的部分信息
        '''
        body = payload.model_dump(exclude_unset=True)  # 将Pydantic模型转换为json字典
        return self.client.patch(f'/users/{user_id}', json=body)

    def delete(self, user_id: int) -> dict:
        '''
        DELETE /users/{id}   ——通过id删除user
        '''
        return self.client.delete(f'/users/{user_id}')
