class PostsAPI:
    """/posts 接口的业务封装。"""

    def __init__(self, client):
        self.client = client

    def postlist(self) -> list:
        """GET /posts —— 列出所有 posts。"""
        return self.client.get('/posts').json()

    def get(self, post_id) -> dict:
        '''
        GET/posts/{post_id} —— 获取单个post接口信息
        '''
        return self.client.get(f'/posts/{post_id}').json()

    def create(self, user_id: int, title: str, body: str) -> dict:
        '''
        POST/posts —— 创建post接口
        '''
        return self.client.post('/posts', json={"userId": user_id, "title": title, "body": body}).json()

    def update(self, post_id: int,user_id: int, title: str, body: str) -> dict:
        '''
        PUT/posts/{id} ——更新接口全部信息
        '''
        return self.client.put(f'/posts/{post_id}', json={"userId": user_id, "title": title, "body": body}).json()

    def patch(self, post_id: int,**kwargsr) -> dict:
        '''
        PATCH /posts/{id}  ——更新接口部分信息
        '''
        return  self.client.patch(f'/posts/{post_id}', json=kwargsr).json()
    def delete(self, post_id: int) -> dict:
        '''
        DELETE /posts/{id} ——删除接口信息
        '''
        return self.client.delete(f'/posts/{post_id}').json()