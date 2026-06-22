import os


def is_running_in_jenkins():
    """
    检测当前是否运行在 Jenkins 构建环境中。
    通过检查多个典型的 Jenkins 环境变量来判断。
    """
    # Jenkins 必设的变量列表（只要存在其中一个，大概率就是 Jenkins 环境）
    jenkins_vars = [
        'JENKINS_HOME',  # Jenkins 主目录
        'JENKINS_URL',  # Jenkins 访问地址
        'BUILD_NUMBER',  # 构建编号
        'JOB_NAME',  # 任务名称
        'WORKSPACE',  # 工作目录
        'JENKINS_SERVER_COOKIE'  # 某些版本会有
    ]
    for var in jenkins_vars:
        if os.environ.get(var):
            return True
    return False
