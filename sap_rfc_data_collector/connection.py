from pyrfc import Connection


class SAPConnection:
    def __init__(self,
                 client: str,
                 lang: str,
                 user: str,
                 password: str,
                 host: str = None,
                 service: str = None,
                 sysname: str = None,
                 group: str = None):
        self.params = {
            'mshost': host,
            'msserv': service,
            'group': group,
            'sysid': sysname,
            'client': client,
            'lang': lang,
            'user': user,
            'passwd': password,
        }

    def get_connection(self) -> Connection:
        params = {k: v for k, v in self.params.items() if v is not None}
        return Connection(**params)
