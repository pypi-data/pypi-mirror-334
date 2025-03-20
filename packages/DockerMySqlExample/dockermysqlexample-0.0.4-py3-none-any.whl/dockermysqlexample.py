import os

import pymysql
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    userid = os.getenv("MYSQL_USER", "root")
    pwd = os.getenv("MYSQL_PASSWORD", "N0Pa55wrd")
    try:
        connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            # user=os.getenv("INSTALLER_USERID", "root"),
            # password=os.getenv("MYSQL_ROOT_PASSWORD", "N0Pa55wrd"),
            user=userid,
            password=pwd,
            database=os.getenv("MYSQL_DATABASE", "DockerMySqlExample"),
            port=int(os.getenv("MYSQL_TCP_PORT", 3306)),
        )
        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES;")
            databases = cursor.fetchall()
        connection.close()
        return {"databases": databases}
    except Exception as e:
        s = f"str({e}) userid:{userid} password:{pwd}"
        return {"error": s}
