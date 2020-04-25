import tushare as ts
import get_date as gtd

ts.set_token("5e2ad725eacd63551be36913a89266136d834a92776c7a9c9a41b468")
pro = ts.pro_api()
start_date='20171201'
end_date='20190330'

print(gtd.get_date_list(start_date,end_date))


"""
import pymysql

con = pymysql.connect(host="localhost", user="root", passwd="mysql", db="stockvision")
cursor=con.cursor()


dates = gdte.get_date_list(startDate, endDate)
df = pd.DataFrame()
for date in dates:
    frame = td.get_index_weight(pro, date, retry_count, pause)
    df = df.append(frame)
    print(frame)

try:
    sql = "CREATE TABLE  index_weight (index_code VARCHAR(10),con_code VARCHAR(10) ,trade_date VARCHAR(8),weight FLOAT,PRIMARY KEY (index_code,con_code,trade_date))"
    cursor.execute(sql)
    con.commit()
except:
    con.rollback()
"""
