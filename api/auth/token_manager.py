class TokenManager:
    '''
    token管理器，涉及自动刷新和并发控制
    '''

    def __init__(self, login_url, username, password, token_buffer_seconds):
        self.login_url = login_url
        self.username = username,
        self.password = password,
        self.token_buffer_seconds = token_buffer_seconds  # token过期时间
        pass

    def get_token(self):
        pass
