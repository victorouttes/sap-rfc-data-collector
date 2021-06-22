import pandas as pd
from pyrfc import ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError

from .connection import SAPConnection


class SAP:
    def __init__(self,
                 host: str,
                 service: str,
                 group: str,
                 sysname: str,
                 client: str,
                 lang: str,
                 user: str,
                 password: str):
        self.connection = SAPConnection(
            host=host,
            service=service,
            group=group,
            sysname=sysname,
            client=client,
            lang=lang,
            user=user,
            password=password
        )

    def _to_dataframe(self, result: list, colunas: list) -> pd.DataFrame:
        df = pd.DataFrame(columns=colunas)
        for j, d in enumerate(result):
            resultado = d['WA']
            df.loc[j] = resultado.split('¬')
        return df

    def get_dataframe(self, table: str, columns: list, where: str = None, page_size: int = 1000) -> pd.DataFrame:
        """
        Get data from SAP table in pandas dataframe format.
        :param table: SAP table name.
        :param columns: list of columns desired.
        :param where: where clause (optional)
        :param page_size: number of rows per query. Optional. Default: 1000.
        :return: pandas dataframe.
        """
        fields = []
        where_clause = []
        page = 1
        df = pd.DataFrame(columns=columns)

        if where:
            where_clause = [{"TEXT": where}]

        if columns:
            fields = [{"FIELDNAME": f} for f in columns]

        while True:
            try:
                connection = self.connection.get_connection()

                start = (page - 1) * page_size
                limit = page_size
                result = connection.call('RFC_READ_TABLE',
                                         QUERY_TABLE=table,
                                         DELIMITER='¬',
                                         FIELDS=fields,
                                         OPTIONS=where_clause,
                                         ROWSKIPS=start,
                                         ROWCOUNT=limit)
                df = df.append(self._to_dataframe(result['DATA'], columns))
                connection.close()
                print(f'Approximated rows collected...{page * page_size}')
                if len(result['DATA']) < page_size:
                    break
                page += 1
            except CommunicationError:
                if df.empty:
                    df['error'] = ['Could not connect to server.']
                else:
                    df['error'] = 'Could not connect to server.'
                break
            except LogonError:
                if df.empty:
                    df['error'] = ['Could not log in. Wrong credentials?']
                else:
                    df['error'] = 'Could not log in. Wrong credentials?'
                break
            except (ABAPApplicationError, ABAPRuntimeError):
                if df.empty:
                    df['error'] = ['An error occurred.']
                else:
                    df['error'] = 'An error occurred.'
                break

        return df
