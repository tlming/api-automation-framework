class TodoAPI:
    def __init__(self, client):
        self.client = client

    def todo_list(self) -> list:
        '''
        GET /todos —— 获取所有的todo
        '''
        return self.client.get('/todos')

    def get_todo_by_userId(self, user_id: int) -> list:
        '''
        GET /todos?userId={userId}  ——通过userid获取todo信息
        '''
        return self.client.get(f'/todos?userId={user_id}')

    def get_todos_by_id(self, todo_id) -> dict:
        '''
        GET /todos/{id} ——通过id获取todo信息
        '''
        return self.client.get(f'/todos/{todo_id}')

    def create(self, user_id: int, title: str, completed: bool) -> dict:
        '''
        POST /todos ——创建todo
        '''
        return self.client.post('/todos', json={"useId": user_id, "title": title, "completed": completed})

    def update(self, todo_id: int, user_id: int, title: str, completed: bool) -> dict:
        '''
        PUT /todos/{id}   ——通过id更新整个todo的信息
        '''
        return self.client.put(f'/todos/{todo_id}', json={"userId": user_id, "title": title, "completed": completed})

    def patch(self, todo_id: int, **kwargs) -> dict:
        '''
        PATCH /todos/{id}   ——通过id更新部分todo的信息
        '''
        return self.client.patch(f'/todos/{todo_id}', json=kwargs)

    def delete(self, todo_id: int) -> dict:
        '''
        DELETE /todos/{id}   ——通过id删除todo
        '''
        return self.client.delete(f'/todos/{todo_id}')
