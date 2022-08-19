import sqlite3

class DB():
    def __init__(self, db_name):
        if not isinstance(db_name, str):
            raise TypeError("db_name must be path to db")

        self.conn = sqlite3.connect(db_name)
        
        curr = self.conn.cursor()
        curr.execute("CREATE TABLE IF NOT EXISTS scanned_data (id INTEGER PRIMARY KEY, parking_type TEXT, code TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
    
    def insert_data(self, data):
        """ Data should have parking_type, and code from QR """

        cur = self.conn.cursor()
        cur.execute("INSERT INTO scanned_data (parking_type, code) VALUES (?, ?)", (data['parking_type'], data['code']))

        self.conn.commit()
        cur.close()