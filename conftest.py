import pytest
from api import ApiClient,PostsAPI
from utils import config, setup_logger


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