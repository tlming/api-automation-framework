import pytest
from api import ApiClient, PostsAPI, TodoAPI, UserAPI
from utils import config, setup_logger,is_running_in_jenkins,send_serverchan_message
@pytest.fixture(scope='session')
def api_client():
    """Session 范围的 APIClient，整个测试会话只创建一次。"""
    # 加载配置logging
    setup_logger()

    return ApiClient(
        base_url=config.base_url,
        timeout=config.timeout,
    )


@pytest.fixture()
def api_post(api_client):
    # 每一个测试都使用一个PostsAPI
    return PostsAPI(api_client)


@pytest.fixture()
def api_todo(api_client):
    # 每一个测试都使用一个TodoAPI
    return TodoAPI(api_client)


@pytest.fixture()
def api_user(api_client):
    # 每一个测试都使用一个UserAPI
    return UserAPI(api_client)

def pytest_sessionfinish(session):
    if is_running_in_jenkins():
        import os
        server_sendkey = os.environ.get('server_sendkey')
        BUILD_NUMBER=os.environ.get('BUILD_NUMBER')
        url=f'http://localhost:8080/job/api-automation-framework/{BUILD_NUMBER}/allure/'
        send_serverchan_message(sckey=server_sendkey,title='api-automation-framework自动化运行完毕',content=f'报告地址:{url}')



