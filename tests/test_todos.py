from pathlib import Path
from unittest import case

import pytest
import yaml

# 加载测试数据
test_dir = Path(__file__).parent.parent
with open(f'{test_dir}/test_data/todo.yaml', encoding='utf-8') as f:
    todos_test_data = yaml.safe_load(f)
CREATE_TODO_DATA = todos_test_data['create']


# 编写测试用例
def test_get_all_todo(api_todo):
    '''
    获取所有的todo,总数量应为200
    '''
    resp = api_todo.todo_list()
    assert isinstance(resp.data, list)
    assert len(resp.data) == 200


@pytest.mark.parametrize('case', (1, 99))
def test_get_todo_by_userId(api_todo, case):
    '''
    通过userid获取todo信息
    '''
    resp = api_todo.get_todo_by_userId(case)
    data = resp.data
    assert isinstance(data, list)
    assert all(isinstance(p['completed'], bool) for p in data)


@pytest.mark.parametrize('case', (1, 99))
def test_get_todo_by_id(api_todo, case):
    '''
    通过id获取单个todo信息
    '''
    resp = api_todo.get_todo_by_id(case)
    data = resp.data
    assert isinstance(data, dict)
    assert isinstance(data['completed'], bool) if data['completed'] else True


@pytest.mark.parametrize('case', CREATE_TODO_DATA, ids=[ct['casename'] for ct in CREATE_TODO_DATA])
def test_create(api_todo, case):
    resp = api_todo.create(user_id=case['payload']['userId'], title=case['payload']['title'],
                           completed=case['payload']['completed'])
    assert isinstance(resp.data, dict)
    assert "id" in resp.data
    assert resp.status_code == case['expected_status']


def test_update(api_todo):
    '''
    通过id更新整个todo信息
    '''
    resp = api_todo.update(todo_id=1, user_id=9999, title="9999", completed=True)
    data = resp.data
    assert data['id'] == 1
    assert data['userId'] == 9999
    assert data['title'] == '9999'
    assert data['completed'] is True


def test_patch(api_todo):
    '''
    通过id更新todo部分信息
    '''
    resp = api_todo.patch(todo_id=1, json={"user_id":9999})
    data = resp.data
    assert data['user_id'] == 9999


def test_delete(api_todo):
    '''
    通过id删除todo信息
    '''
    resp = api_todo.delete(todo_id=1)
    assert resp.status_code == 200
    assert resp.data == {}
