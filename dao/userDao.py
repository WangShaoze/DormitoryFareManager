import sqlite3


class UserDao:
    def __init__(self):
        self.__user = None
        self.__pwd = None
        self.conn = None

    def getUser(self):
        return self.__user

    def getPwd(self):
        return self.__pwd

    def setUser(self, user: str):
        self.__user = user

    def setPwd(self, pwd: str):
        if pwd.isalnum():
            self.__pwd = pwd

    def isUser(self):
        if self.__user == "" or self.__user is None:
            return False
        if self.__pwd == "" or self.__pwd is None:
            return False
        self.conn = sqlite3.connect("dao/dormitoryFareManager.db")
        cursor = self.conn.cursor()
        # 查询数据
        cursor.execute('SELECT * FROM user_list;')
        data = cursor.fetchall()
        self.conn.close()
        for uni in data:
            if self.getUser() in uni and self.getPwd() in uni:
                return True
        else:
            return False

    def insertUser(self):
        if str(self.getPwd()).isdigit():
            self.conn = sqlite3.connect("dao/dormitoryFareManager.db")
            cursor = self.conn.cursor()
            try:
                # 插入记录
                cursor.execute("INSERT INTO user_list VALUES('{}', '{}')".format(self.getUser(), self.getPwd()))
                self.conn.commit()
                return True
            except Exception as e:
                print(e)
                return False
            finally:
                self.conn.close()
