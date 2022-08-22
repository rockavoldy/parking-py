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

    def get_count_data(self, code=False, parking_type=False):
        if not code or parking_type:
            return 0
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM scanned_data WHERE code = ? AND parking_type = ?", (str(code), str(parking_type)))
        return cur.fetchone()[0]

    def get_data(self, code=False):
        if not code:
            return 0
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM scanned_data")
        return cur.fetchall()