from pyrfc import Connection


class SAPConnection:
    def __init__(self,
                 host: str,
                 service: str,
                 group: str,
                 sysname: str,
                 client: str,
                 lang: str,
                 user: str,
                 password: str):
        self.host = host
        self.service = service
        self.group = group
        self.sysname = sysname
        self.client = client
        self.lang = lang
        self.user = user
        self.password = password

    def get_connection(self) -> Connection:
        return Connection(
            user=self.user,
            passwd=self.password,
            mshost=self.host,
            msserv=self.service,
            group=self.group,
            sysid=self.sysname,
            client=self.client,
            lang=self.lang
        )
