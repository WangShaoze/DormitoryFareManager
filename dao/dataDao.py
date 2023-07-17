import sqlite3


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
        self.__conn = sqlite3.connect(database="dao/dormitoryFareManager.db")
        cursor = self.__conn.cursor()
        sql = "insert into dormitory_fare values('{}', '{}', {}, {}, '{}');".format
        try:
            sql = sql(self.getDate(), self.getFair(), self.getBonus(), self.getMoney(), self.getNote())
            cursor.execute(sql)
            self.__conn.commit()
        except Exception as e:
            print(e)
            flag = False
        finally:
            self.__conn.close()
        return flag

    def search_by_date(self, date):
        self.__conn = sqlite3.connect(database="dao/dormitoryFareManager.db")
        cursor = self.__conn.cursor()
        cursor.execute("select * from dormitory_fare where 日期='{}';".format(date))
        _data = cursor.fetchall()  # 查询所有的数据
        self.__conn.commit()
        self.__conn.close()
        return _data

    def delete_record_by_columns(self, **kwargs):
        """
        kwargs :
            date="date", fare="fare", bonus="bonus", note="note"
        :return: bool
        """
        if len(kwargs) == 0:
            return False
        sql = "DELETE FROM dormitory_fare WHERE"
        if "date" in kwargs:
            if list(kwargs.keys()).index("date") == len(list(kwargs.keys())) - 1:
                sql += " 日期='{}'".format(kwargs["date"])
            else:
                sql += " 日期='{}' and".format(kwargs["date"])
        if "fare" in kwargs:
            if list(kwargs.keys()).index("date") == len(list(kwargs.keys())) - 1:
                sql += " 事务='{}'".format(kwargs["date"])
            else:
                sql += " 事务='{}' and".format(kwargs["fare"])
        if "bonus" in kwargs:
            if list(kwargs.keys()).index("date") == len(list(kwargs.keys())) - 1:
                sql += " 事务金额={}".format(kwargs["date"])
            else:
                sql += " 事务金额={} and".format(kwargs["bonus"])
        if "note" in kwargs:
            if list(kwargs.keys()).index("date") == len(list(kwargs.keys())) - 1:
                sql += " 备注='{}'".format(kwargs["date"])
            else:
                sql += " 备注='{}'".format(kwargs["note"])
        sql += ";"
        print(sql)
        try:
            self.__conn = sqlite3.connect(database="dao/dormitoryFareManager.db")
            cursor = self.__conn.cursor()
            cursor.execute(sql)  # 执行删除指定的记录
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.__conn.commit()
            self.__conn.close()


if __name__ == '__main__':
    # 测试时数据库的路径可能不对，需要该路径即可
    dateDao = DataDao()
    # dateDao.setDate("2023/7/9")
    # dateDao.setFair("交水费")
    # dateDao.setBonus(-11.0)
    # dateDao.setMoney(82.5)
    # dateDao.setNote("小王付钱")
    # dateDao.insertRecord()
    for uni in dateDao.getHistoryData():
        print(uni)

    if dateDao.delete_record_by_columns(date="2023/07/15", note="小苏付钱", fare="交水费"):
        print("已经成功删除: 2023/07/13 的数据")
    for uni in dateDao.getHistoryData():
        print(uni)