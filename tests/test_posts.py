'''API端到端测试 --Day2'''


def test_get_all_posts(api_post):
    '''
    获取所有接口 应该有100个
    '''
    resp = api_post.post_list()
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 100
    assert all("userId" in p and "id" in p and "title" in p and "body" in p for p in data)


def test_get_post_by_id(api_post):
    '''
    获取单个接口信息， 测试id=1
    '''
    resp = api_post.get_by_id(1)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert data["id"] == 1
    assert "title" in data


def test_get_noexist_post(api_post):
    '''
    接口共计100个，获取第101不存在，应该返回404
    '''
    resp = api_post.get_by_id(101)
    assert resp.status_code == 404


def test_create_post(api_post):
    '''
    创建接口信息
    '''
    resp = api_post.create(user_id=1, title="my first testPost", body="hahahahaha")
    assert resp.status_code == 201
    data = resp.json()
    assert data["userId"] == 1
    assert data["title"] == "my first testPost"
    assert data["body"] == "hahahahaha"

def test_creat_long_post(api_post):
    '''
    创建接口时，字符串超长情况
    '''
    pass



def test_update_post(api_post):
    '''
    修改接口全部信息
    '''
    data = api_post.update(post_id=1, user_id=2, title="updated post", body="zezezeeze").json()
    assert data["id"] == 1
    assert data["userId"] == 2
    assert data["title"] == "updated post"


def test_update_noexist_post(api_post):
    '''
    修改不存在的接口信息，应服务器返回500
    post_id=101
    '''
    resp = api_post.update(post_id=101, user_id=1, title="updated post", body='')
    assert resp.status_code == 500


def test_patch_post(api_post):
    '''
    修改接口部分信息
    '''
    data = api_post.patch(post_id=1, json={"userId": 3, "title": "pathc post", "body": "patch patch"}).json()
    assert data["userId"] == 3
    assert data["title"] == "pathc post"
    assert data["body"] == "patch patch"


def test_delete_post(api_post):
    '''
    删除接口信息
    DELETE /posts/{id}
    '''
    resp = api_post.delete(post_id=1)
    assert resp.json() == {}
