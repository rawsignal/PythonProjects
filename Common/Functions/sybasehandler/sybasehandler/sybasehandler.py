import sybpydb as sybase
import os
import sys

class Connection(object) :
    def __init__(self, username, password, servername) :
        self._username = username
        self._password = password
        self._servername = servername
        self.conn = sybase.connect(user=self._username, password=self._password, servername=self._servername)

    def get_Conn(self) :
        return self.conn

    def close_Connection(self) :
        self.conn.close()

    def __exit__(self) :
        self.conn.close()


obj = Connection("gisuser", "bng67f", "ctmdev")
print(type(obj))
conn = obj.get_Conn()
print(type(conn))
obj.close_Connection()
