import os
import csv
import sqlite3


def import_files(filename: str, table: str) -> None:
    conn = sqlite3.connect('skyanalytics_swamp.db')
    cur = conn.cursor()
    path = 'C:\\Users\\Work\\Desktop\\projects\\skyanalytics\\datasets_raw\\'
    with open(os.path.join(path, filename), 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # Skip the header row
        for row in reader:
            placeholders = ','.join('?' for _ in row)
            cur.execute(f"INSERT INTO {table} VALUES ({placeholders})", row)
    
    conn.commit()
    conn.close()




#import_files(r'C:\Users\Work\Desktop\projects\skyanalytics\datasets_raw\degradations_2024-06-07.csv', 'degradation')


