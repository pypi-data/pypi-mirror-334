# Code below is based on information here: https://learn.microsoft.com/en-us/azure/azure-sql/database/azure-sql-python-quickstart?view=azuresql&tabs=windows%2Csql-inter

import pyodbc, struct
from azure import identity

#from typing import Union
#from fastapi import FastAPI
#from pydantic import BaseModel

#class Person(BaseModel):
#    first_name: str
#    last_name: Union[str, None] = None

# Azure SQL details
SERVER = ""
DATABASE = ""
    
connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{SERVER},1433;Database={DATABASE};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30"

def get_conn():
    credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    print(type(conn))
    return conn

try:
        conn = get_conn()
        cursor = conn.cursor()
        print(type(cursor))

        query = """
                    SELECT   SLK.[User Type]
                            ,FORMAT(COUNT(*), 'N0')
                    FROM    Slack.v_Slack_ABK_Users SLK
                    GROUP BY SLK.[User Type] WITH ROLLUP
                """

        # Table should be created ahead of time in production app.
        cursor.execute(query)

        # Print results
        for row in cursor.fetchall():
            print(row)

        # Close DB connection
        conn.close()

except Exception as e:
    print(e)
