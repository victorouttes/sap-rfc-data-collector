import json
from typing import List, Generator, Any

import pandas as pd
from pyrfc import ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError

from .connection import SAPConnection
from .exceptions import SAPException


class SAP:
    def __init__(self, connection: SAPConnection):
        self.connection = connection

    def _to_dataframe(self, result: list, colunas: list, tamanhos: list) -> pd.DataFrame:
        df = pd.DataFrame(columns=colunas)
        for j, d in enumerate(result):
            resultado = d['WA']
            linha_resultado = []
            for i, col in enumerate(colunas):
                valor = resultado[sum(tamanhos[:i]):sum(tamanhos[:i + 1])]
                linha_resultado.append(valor)
            df.loc[j] = linha_resultado
        df_obj = df.select_dtypes(['object'])
        df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
        return df

    def get_data_df(self,
                    table: str,
                    columns: List[str],
                    where: str = None,
                    where_list: List[str] = None,
                    humanized_columns: List[str] = None,
                    page_size: int = 1000) -> Generator[pd.DataFrame, None, None]:
        fields = []
        where_clause = []
        if where:
            where_clause = [{"TEXT": where}]
        elif where_list:
            where_clause = [{"TEXT": w} for w in where_list]
        if columns:
            fields = [{"FIELDNAME": f} for f in columns]

        page = 1
        while True:
            try:
                connection = self.connection.get_connection()
                start = (page - 1) * page_size
                limit = page_size
                result = connection.call('RFC_READ_TABLE',
                                         QUERY_TABLE=table,
                                         # DELIMITER='¬',
                                         FIELDS=fields,
                                         OPTIONS=where_clause,
                                         ROWSKIPS=start,
                                         ROWCOUNT=limit)
                connection.close()
                response_columns = result.get('FIELDS')
                response_columns_lenght = [int(col.get('LENGTH')) for col in response_columns]
                response_columns = [col.get('FIELDNAME') for col in response_columns]
                data = self._to_dataframe(result['DATA'], response_columns, response_columns_lenght)
                if humanized_columns:
                    new_humanized_columns = dict(zip(columns, humanized_columns))
                    data.rename(columns=new_humanized_columns, inplace=True)
                yield data
                if len(result['DATA']) < page_size:
                    break
                page += 1
            except CommunicationError:
                raise SAPException('Could not connect to server')
            except LogonError:
                raise SAPException('Could not log in. Wrong credentials?')
            except (ABAPApplicationError, ABAPRuntimeError):
                raise SAPException('An error occurred at ABAP level')

    def get_data_json(self,
                      table: str,
                      columns: List[str],
                      page: int,
                      where: str = None,
                      where_list: List[str] = None,
                      humanized_columns: List[str] = None,
                      page_size: int = 1000) -> Any:
        fields = []
        where_clause = []
        if where:
            where_clause = [{"TEXT": where}]
        elif where_list:
            where_clause = [{"TEXT": w} for w in where_list]
        if columns:
            fields = [{"FIELDNAME": f} for f in columns]

        try:
            connection = self.connection.get_connection()
            start = (page - 1) * page_size
            limit = page_size
            result = connection.call('RFC_READ_TABLE',
                                     QUERY_TABLE=table,
                                     # DELIMITER='¬',
                                     FIELDS=fields,
                                     OPTIONS=where_clause,
                                     ROWSKIPS=start,
                                     ROWCOUNT=limit)
            connection.close()

            response_columns = result.get('FIELDS')
            response_columns_lenght = [int(col.get('LENGTH')) for col in response_columns]
            response_columns = [col.get('FIELDNAME') for col in response_columns]
            data = self._to_dataframe(result['DATA'], response_columns, response_columns_lenght)
            if humanized_columns:
                new_humanized_columns = dict(zip(columns, humanized_columns))
                data.rename(columns=new_humanized_columns, inplace=True)
            return json.loads(data.to_json(orient='records', force_ascii=False))
        except CommunicationError:
            raise SAPException('Could not connect to server')
        except LogonError:
            raise SAPException('Could not log in. Wrong credentials?')
        except (ABAPApplicationError, ABAPRuntimeError):
            raise SAPException('An error occurred at ABAP level')
