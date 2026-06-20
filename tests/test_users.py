from pathlib import Path
from unittest import case

import pytest
import yaml

from models import UserResponse, UserRequest, UserTestCase

# 加载测试数据
test_dir = Path(__file__).parent.parent
with open(f'{test_dir}/test_data/user.yaml', encoding='utf-8') as f:
    users_test_data = yaml.safe_load(f)
USER_ID_DATA = users_test_data['user_id']
# 将users_test_data['create']中的每一个数据转换成Pydantic对象列表
CREATE_USER_DATA = [UserTestCase.model_validate(i) for i in users_test_data['create']]


# 测试用例编写
def test_get_all_posts(api_user):
    '''
    获取所有user数据，并校验返回类型，应该存在10个
    '''
    resp = api_user.user_list()
    assert resp.status_code == 200
    assert len(resp.data) == 10
    # 检验返回值类型
    for p in resp.data:
        UserResponse.model_validate(p)


@pytest.mark.parametrize('case', USER_ID_DATA, ids=[u['casename'] for u in USER_ID_DATA])
def test_get_user_by_id(api_user, case):
    '''
    通过id获取user数据，
    '''
    resp = api_user.get_user_by_id(case['payload']['user_id'])
    assert resp.status_code == case['expected_status']
    if case['expected_status'] == 200:
        UserResponse.model_validate(resp.data)


@pytest.mark.parametrize('case', (1, 99))
def test_get_user_posts(api_user, case):
    '''
    通过id获取对应user的post信息
    '''
    resp = api_user.get_user_posts(case)
    assert resp.status_code == 200
    data = resp.data
    assert isinstance(data, list)
    assert all("userId" in p for p in data)
    assert all("postId" not in p for p in data)


@pytest.mark.parametrize('case', (1, 99))
def test_get_user_albums(api_user, case):
    '''
    通过id获取对应user的album信息
    '''
    resp = api_user.get_user_albums(case)
    assert resp.status_code == 200
    data = resp.data
    assert isinstance(data, list)
    assert all("userId" in p and "id" in p for p in data)


@pytest.mark.parametrize('case', (1, 99))
def test_get_user_todos(api_user, case):
    '''
    通过id获取对应user的todo信息
    '''
    resp = api_user.get_user_todos(case)
    assert resp.status_code == 200
    data = resp.data
    assert isinstance(data, list)
    assert all(isinstance(p["completed"], bool) for p in data)


@pytest.mark.parametrize('case', CREATE_USER_DATA, ids=[u.casename for u in CREATE_USER_DATA])
def test_create_user(api_user, case):
    '''
    新建一个user信息
    '''
    resp = api_user.create(case.payload.model_dump())
    assert resp.status_code == case.expected_status


@pytest.mark.parametrize('case', CREATE_USER_DATA)
def test_update_user(api_user, case):
    '''
    通过id更新user全部信息，user_id=1
    '''
    resp = api_user.update(user_id=1, user_data=case.payload.model_dump())
    assert resp.status_code == 200
    assert resp.data["username"] == case.payload.model_dump()["username"]


def test_patch_user(api_user):
    '''
    通过id更新user部分信息，user_id=1
    '''
    resp = api_user.patch(user_id=1, json={"username": "cs_patch", "phone": "1xxxxxxxxx"})
    assert resp.status_code == 200
    assert resp.data["username"] == "cs_patch"
    assert resp.data["phone"] == "1xxxxxxxxx"


def test_delete_user(api_user):
    '''
    通过id删除user信息
    '''
    resp = api_user.delete(user_id=1)
    assert resp.status_code == 200
    assert resp.data == {}
