import sqlite3

class Database:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS plates (
            id      INTEGER     PRIMARY KEY AUTOINCREMENT,  
            country TEXT        NOT NULL,
            number  INTEGER(3)  NOT NULL,
            letters TEXT        NOT NULL,
            region  TEXT        NOT NULL          
        );""")
        self.conn.commit()
    
    def add_license_plate(self, country, number, letters, region):
        self.cursor.execute("INSERT INTO plates VALUES (NULL, ?, ?, ?, ?)", (country, number, letters, region))
        self.conn.commit()

    def remove_license_plate(self, id):
        self.cursor.execute("DELETE FROM plates WHERE id = ?", (id,))
        self.conn.commit()

    def check_license_plate(self, country, number, letters, region):
        self.cursor.execute("SELECT * FROM plates WHERE country = ? AND number = ? AND letters = ? AND region = ?", (country, number, letters, region))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()