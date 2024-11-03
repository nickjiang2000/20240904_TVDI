import sqlite3
import requests

def get_data()->list[list]:
    url = 'https://data.moenv.gov.tw/api/v2/aqx_p_488?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=JSON'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(e)
        return []  # 回傳空列表以避免後續錯誤
    else:
        outerlist = []
        for items in data['records']:
            innerlist = [items['sitename'],
                         items['datacreationdate'],
                         items['county'],
                         items['aqi'],
                         items['pm2.5'],
                         items['status'],
                         items['latitude'],
                         items['longitude']]
            outerlist.append(innerlist)
        return outerlist

def insert_data(conn, AQI_data):
    # 在不重複的情況下插入資料，可使用 INSERT OR IGNORE 語句。當重複時，該記錄會被忽略
    insertSQL = """
    INSERT OR IGNORE INTO records(sitename, date, county, aqi, pm25, status, lat, lon)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?)
    """
    # Create a cursor object
    cursor2 = conn.cursor()
    # insert a table
    cursor2.executemany(insertSQL,AQI_data)
    # Commit changes and close the cursor
    conn.commit()
    cursor2.close()


def main():
    sql = '''
    CREATE TABLE IF NOT EXISTS records (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	sitename TEXT NOT NULL,
    date TEXT,
	County TEXT,
	aqi INTEGER,
    pm25 NUMERIC,
	status TEXT,
	lat NUMERIC,
	lon NUMERIC,
    UNIQUE (sitename, date)
    );
    '''
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("AQI.db")
    # Create a cursor object
    cursor = conn.cursor()
    # Create a table
    cursor.execute(sql)
    cursor.close()
    # Get all AQI data
    AQI_data = get_data()
    # insert into the db file
    insert_data(conn,AQI_data)
    # close the connection
    conn.close()
    print("mission completed")

# 執行主程式
if __name__ == "__main__":
    main()