import requests
import sqlite3

def get_new_data():
    url = 'https://data.moenv.gov.tw/api/v2/aqx_p_488?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=JSON'
    try:
        response = requests.get(url)
        response.raise_for_status()
        original = response.json() 
        #此時取得的data是json，與已整理過的舊資料不一致
        data= []
        sitenames = set()
        for row in original['records']:
            record = {
                'date': row[0],
                'county': row[1],
                'aqi': row[2],
                'pm25': row[3],
                'status': row[4],
                'lat': row[5],
                'lon': row[6],
                'sitename': row[7]
                }
            #以上字串非原始json之欄位名稱，而是DB檔裡設定的名稱
            #沒有設定把新資料更新入DB檔
            data.append(record)
            sitenames.add(record['sitename'])
        sitenames = list(sitenames)
    except Exception as e:
        print(e)
    else:
        return data, sitenames

def fetch_old_data():
    # connect to SQLite and create cursor
    conn = sqlite3.connect("AQI.db")
    cursor = conn.cursor()
    try:
    # execute and choose all data, get all data
        cursor.execute("SELECT * FROM records")
        rows = cursor.fetchall()
        data= []
        sitenames = set()
        for row in rows:
            record = {
                'date': row[0],
                'county': row[1],
                'aqi': row[2],
                'pm25': row[3],
                'status': row[4],
                'lat': row[5],
                'lon': row[6],
                'sitename': row[7]
                }
            data.append(record)
            sitenames.add(record['sitename'])
        sitenames = list(sitenames)
    except Exception as e:
        print(e)
        return [], []
    finally:  
        # 關閉游標和連接
        cursor.close()
        conn.close()
    return data, sitenames
    
def get_selected_data(sitename:str, data)->list[list]:
    outerlist = []
    #以下未改成DB檔裡頭的欄位名稱，會有衝突
    for items in data['records']:
        if items['sitename'] == sitename:
            innerlist = [items['datacreationdate'],items['county'],items['aqi'],items['pm2.5'],items['status'],items['latitude'],items['longitude']]
            outerlist.append(innerlist)
    return outerlist