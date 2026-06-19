class PostsAPI:
    """/posts 接口的业务封装。"""

    def __init__(self, client):
        self.client = client

    def post_list(self) -> list:
        """GET /posts —— 列出所有 posts。"""
        return self.client.get('/posts')

    def get_by_userId(self, user_id)->dict:
        '''
        GET /posts?userId={userId} —— 通过userId获取post接口信息
        '''
        return self.client.get(f'/posts?userId={user_id}')

    def get_by_id(self, post_id) -> dict:
        '''
        GET/posts/{post_id} —— 通过id获取单个post接口信息
        '''
        return self.client.get(f'/posts/{post_id}')

    def get_post_comments(self, post_id) -> list:
        '''
        GET /posts/{id}/comments —— 通过id获取对于title的评论列表
        '''
        return self.client.get(f'/posts/{post_id}/comments')

    def create(self, user_id: int, title: str, body: str) -> dict:
        '''
        POST/posts —— 创建post接口
        '''
        return self.client.post('/posts', json={"userId": user_id, "title": title, "body": body})

    def update(self, post_id: int,user_id: int, title: str, body: str) -> dict:
        '''
        PUT/posts/{id} ——更新接口全部信息
        '''
        return self.client.put(f'/posts/{post_id}', json={"userId": user_id, "title": title, "body": body})

    def patch(self, post_id: int,**kwargs) -> dict:
        '''
        PATCH /posts/{id}  ——更新接口部分信息
        '''
        return  self.client.patch(f'/posts/{post_id}', json=kwargs)
    def delete(self, post_id: int) -> dict:
        '''
        DELETE /posts/{id} ——删除接口信息
        '''
        return self.client.delete(f'/posts/{post_id}')