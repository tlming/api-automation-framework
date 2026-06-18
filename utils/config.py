from coverage.annotate import os
from dotenv import load_dotenv

#将.env.test中设置的变量导入进来
load_dotenv('.env.test')

class Config:
    base_url = os.getenv('BASE_URL')
    timeout = int(os.getenv('TIMEOUT'))

config = Config()