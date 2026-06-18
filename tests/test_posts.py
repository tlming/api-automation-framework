'''API端到端测试 --Day2'''


def test_get_all_posts(api_post):
    '''
    获取所有接口 应该有100个
    '''
    result = api_post.postlist()
    assert isinstance(result, list)
    assert len(result) == 100
    assert all("userId" in p and "id" in p and "title" in p and "body" in p for p in result)


def test_get_post_by_id(api_post):
    '''
    获取单个接口信息， 测试id=1
    '''
    result = api_post.get(1)
    assert isinstance(result, dict)
    assert result["id"] == 1
    assert "title" in result


def test_create_post(api_post):
    '''
    创建接口信息
    '''
    result = api_post.create(user_id=1, title="my first testPost", body="hahahahaha")
    assert result["userId"] == 1
    assert result["title"] == "my first testPost"
    assert result["body"] == "hahahahaha"

# def test_update_post(api_post):
#     '''
#     修改接口全部信息
#     '''
#     result = api_post.put(1)