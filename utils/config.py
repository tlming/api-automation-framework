from coverage.annotate import os
from dotenv import load_dotenv

#将.env.test中设置的变量导入进来
load_dotenv('.env.test')

class Config:
    base_url = os.getenv('BASE_URL')
    timeout = int(os.getenv('TIMEOUT'))
    login_url = os.getenv('LOGIN_URL')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    token_buffer_seconds = int(os.getenv('TOEKN_BUFFER_SECONDS'))

config = Config()