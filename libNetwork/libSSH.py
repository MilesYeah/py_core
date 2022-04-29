import paramiko


class BaseSSH(object):

    def __init__(self, hostname, port, username, password, timeout, command):
        """
        :param hostname: 主机名
        :param port:     端口
        :param username: 用户
        :param password: 密码
        :param timeout:  tcp连接超时时间 单位ms
        :param command:  shell命令
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout / 1000  # ms to s
        self.command = command

    def __enter__(self):
        # 实例化SSHClient
        self.client = paramiko.SSHClient()
        # 自动添加策略，保存服务器的主机名和密钥信息，如果不添加，那么不再本地know_hosts文件中记录的主机将无法连接
        # 报错：paramiko.ssh_exception.SSHException: Server '127.0.0.1(Server地址)' not found in known_hosts
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接SSH服务端，以用户名和密码进行认证
        self.client.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password,
                            timeout=self.timeout)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.client.close()

    def exec_command(self):
        """
        :return: stdin, stdout, stderr
        """
        # 打开一个Channel并执行命令
        return self.client.exec_command(self.command)  # stdout 为正确输出，stderr为错误输出，同时是有1个变量有值



