import pytest
from api import ApiClient, PostsAPI, TodoAPI, UserAPI
from api.auth import TokenManager
from utils import config, setup_logger,is_running_in_jenkins,send_serverchan_message


@pytest.fixture(scope='session')
def token_manager(tmp_path_factory,worker_id):
    '''
    跨进程安全的TokenManager

    工作原理：
    1、单进程时不考虑文件锁，使用内存锁，直接将token放进内存中
    2、多进程模式使用文件锁
        - 所有的worker共享的一个json文件
        - 使用filelock确定一次只能有一个进程访问文件
        -
    '''

    #单进程模式直接返回TokenManager
    if worker_id =='master':
        return TokenManager(
            login_url=config.login_url,
            username=config.username,
            password=config.password,
            token_buffer_seconds=config.token_buffer_seconds
        )
    shared_token_file=tmp_path_factory.getbasetemp().parent / 'shared_token.json'
    return TokenManager(
            login_url=config.login_url,
            username=config.username,
            password=config.password,
            token_buffer_seconds=config.token_buffer_seconds,
            shared_token_file=shared_token_file
        )

@pytest.fixture(scope='session')
def api_client(token_manager):
    """Session 范围的 APIClient，整个测试会话只创建一次。"""
    # 加载配置logging
    setup_logger()

    return ApiClient(
        base_url=config.base_url,
        timeout=config.timeout,
        token_manager=token_manager,
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
    # 怕买到是否为主节点，单进程 or 多进程非主节点都会存在workerinput
    if hasattr(session.config,'workerinput'):
        return
    if is_running_in_jenkins():
        import os
        server_sendkey = os.environ.get('server_sendkey')
        BUILD_NUMBER=os.environ.get('BUILD_NUMBER')
        url=f'http://localhost:8080/job/api-automation-framework/{BUILD_NUMBER}/allure/'
        send_serverchan_message(sckey=server_sendkey,title='api-automation-framework自动化运行完毕',content=f'报告地址:{url}')



