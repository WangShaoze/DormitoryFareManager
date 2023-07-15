import sqlite3


# conn = sqlite3.connect("dormitoryFareManager.db")
# cursor = conn.cursor()
# cursor.execute("select * from  dormitory_fare;")
# data = cursor.fetchall()
# for uni in data:
#     print(uni)
# conn.commit()
# conn.close()

class DataDao:
    def __init__(self):
        self.__date = None  # 获取当天的日期
        self.__fair = None  # 事务
        self.__bonus = None  # 事务金额
        self.__money = None  # 余额
        self.__note = None  # 备注

        # 初始化一个数据库连接
        self.__conn = None

    def getDate(self):
        return self.__date

    def setDate(self, date):
        self.__date = date

    def getFair(self):
        return self.__fair

    def setFair(self, fair):
        self.__fair = fair

    def getBonus(self):
        return self.__bonus

    def setBonus(self, bonus):
        self.__bonus = bonus

    def getMoney(self):
        return self.__money

    def setMoney(self, money):
        self.__money = money

    def getNote(self):
        return self.__note

    def setNote(self, note):
        self.__note = note

    def getHistoryData(self):
        """
        获取数据库中已有的数据
        :return: history_data -----> type---------> list
        """
        self.__conn = sqlite3.connect(database="dao/dormitoryFareManager.db")
        cursor = self.__conn.cursor()
        cursor.execute("select * from dormitory_fare;")
        history_data = cursor.fetchall()  # 查询所有的数据
        self.__conn.commit()
        self.__conn.close()
        return history_data

    def insertRecord(self):
        """
        向表中添加 单条数据
        :return: flag  ----> type ----> bool
        """
        flag = True
        self.__conn = sqlite3.connect(database="dormitoryFareManager.db")
        cursor = self.__conn.cursor()
        sql = "insert into dormitory_fare values('{}', '{}', {}, {}, '{}');".format
        try:
            sql = sql(self.getDate(), self.getFair(), self.getBonus(), self.getMoney(), self.getNote())
            print(sql)
            cursor.execute(sql)
        except Exception as e:
            print(e)
            flag = False
        finally:
            self.__conn.commit()
            self.__conn.close()
        return flag


if __name__ == '__main__':
    dateDao = DataDao()
    # dateDao.setDate("2023/7/9")
    # dateDao.setFair("交水费")
    # dateDao.setBonus(-11.0)
    # dateDao.setMoney(82.5)
    # dateDao.setNote("小王付钱")
    # dateDao.insertRecord()
    for uni in dateDao.getHistoryData():
        print(uni)
