# import sqlite3
#
# conn = sqlite3.connect("dormitoryFareManager.db")
# cursor = conn.cursor()
#
# # 创建表
# cursor.execute("create table if not exists user_list (user text, pwd text)")
# # cursor.execute("""insert into user_list values
# # ('李启航', "421"),
# # ('黄庆', "421"),
# # ('刘新平', "421"),
# # ('苏鹏', "421"),
# # ('王绍泽', "421"),
# # ('高文立', "421");
# # """)
#
# # cursor.execute("""insert into user_list values('{}', '{}');""".format("xiowang", "123456"))
# #
# # # 提交更改
# conn.commit()
# # 查询数据
# cursor.execute('SELECT * FROM user_list')
# for uni in cursor.fetchall():
#     print(uni)
#
# conn.close()


import sqlite3
import json

# 创建表 在 dormitoryFareManager.db 数据库中
# 建立连接
conn = sqlite3.connect("dormitoryFareManager.db")
cursor = conn.cursor()

# create_table_sql = "create table if not exists dormitory_fare(日期 text,事务 text,事务金额 real,余额 real, 备注 text);"
# cursor.execute(create_table_sql)

"""
 self.create_table_sql 创建表 的过程 
    需要的字段类型
    ---- 日期  --- text ---  文本
    ---- 事务 --- text ---  文本
    ---- 事务金额 --- real ---  浮点
    ---- 余额 --- real ---  浮点
    ---- 备注 --- text ---  文本
"""

# with open("data.json", mode="r", encoding="utf-8") as f:
#     data = json.load(f)
#     for uni in data:
#         uni = list(dict(uni).values())
#         record_sql = "insert into dormitory_fare values('{}', '{}', {}, {}, '{}');".format(uni[0], uni[1], uni[2], uni[3], uni[4])
#         cursor.execute(record_sql)
#         print(record_sql)

sql = "select * from dormitory_fare;"
cursor.execute(sql)
for uni in cursor.fetchall():
    print(uni)

# sql = "insert into dormitory_fare values('jiji', 'jiji000', -11.0, 93.5, '0fhjd');"
# cursor.execute(sql)
conn.commit()
conn.close()
