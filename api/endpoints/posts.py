from api.endpoints.base import BaseAPI
from api.response import APIResponse


class PostsAPI(BaseAPI):
    """/posts 接口的业务封装。"""


    def post_list(self) -> APIResponse:
        """GET /posts —— 列出所有 posts。"""
        return self._get(path="/posts")

    def get_by_userId(self, user_id) -> APIResponse:
        '''
        GET /posts?userId={userId} —— 通过userId获取post接口信息
        '''
        return self._get(path=f"/posts?userId={user_id}")

    def get_by_id(self, post_id) -> APIResponse:
        '''
        GET/posts/{post_id} —— 通过id获取单个post接口信息
        '''
        return self._get(path=f"/posts/{post_id}")

    def get_post_comments(self, post_id) -> APIResponse:
        '''
        GET /posts/{id}/comments —— 通过id获取对于title的评论列表
        '''
        return self._get(path=f"/posts/{post_id}/comments")

    def create(self, user_id: int, title: str, body: str) -> APIResponse:
        '''
        POST/posts —— 创建post接口
        '''
        return self._post(path=f"/posts",json={"userId": user_id, "title": title, "body": body})

    def update(self, post_id: int, user_id: int, title: str, body: str) -> APIResponse:
        '''
        PUT/posts/{id} ——更新接口全部信息
        '''

        return self._put(path=f'/posts/{post_id}',json={"userId": user_id, "title": title, "body": body})

    def patch(self, post_id: int, **kwargs) -> APIResponse:
        '''
        PATCH /posts/{id}  ——更新接口部分信息
        '''
        return self._patch(path=f"/posts/{post_id}",**kwargs)

    def delete(self, post_id: int) -> APIResponse:
        '''
        DELETE /posts/{id} ——删除接口信息
        '''
        return self._delete(path=f"/posts/{post_id}")
