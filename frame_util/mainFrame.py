from tkinter import *
from dao.dataDao import *
import tkinter.messagebox as ms_box


class AddDateFrame(Frame):
    """
    添加数据的页面
    组件名            Label                 Entry              Button
    date             date_label            date_entry
    fare             fare_label            fare_entry
    bonus            bonus_label           bonus_entry
    note             note_label            note_entry

    录入按钮                                                    add_button
        按钮对应的功能就在本类内部实现
            主要是查询历史数据，
            把最后一条的 余额 这个数据拿到，
            后根据用户输入的  事务金额 ，
            计算出新的 余额 ，
            最后将 日期 ， 事务 ， 事务金额 ， 余额 ，备注 五个数据汇总，
            作为一条新的记录 添加 到数据库

    """

    def __init__(self, master, **kwargs):
        super(AddDateFrame, self).__init__(master, kwargs)
        self.date_entry = None
        self.fare_entry = None
        self.bonus_entry = None
        self.note_entry = None
        self.add_button = None
        self.config(bg='#FFF5EE')
        self.widget()

    def widget(self):
        row, column = 0, 0
        font = ("黑体", 30)
        BG = "#FFF5EE"
        BG1 = "white"

        # 页面标题
        Label(self, text="日常事务--添加", font=("宋体", 40), width=60, bg=BG).grid(row=row, columnspan=5)

        #  日期
        row += 1
        date_label = Label(self, text="日期:", font=font, width=20, height=2, bg=BG)
        date_label.grid(row=row, column=column, sticky=E)
        date_entry = Entry(self, font=font, width=35, bg=BG1)
        date_entry.grid(row=row, column=column + 1)

        # 分割
        row += 1
        Label(self, text="", font=("宋体", 25), width=100, bg=BG).grid(row=row, columnspan=5)

        # 事务
        row += 1
        fare_label = Label(self, text="事务:", font=font, width=20, height=2, bg=BG)
        fare_label.grid(row=row, column=column, sticky=E)
        fare_entry = Entry(self, font=font, width=35, bg=BG1)
        fare_entry.grid(row=row, column=column + 1)

        # 分割
        row += 1
        Label(self, text="", font=("宋体", 25), width=100, bg=BG).grid(row=row, columnspan=5)

        # 事务金额
        row += 1
        bonus_label = Label(self, text="事务金额:", font=font, width=20, height=2, bg=BG)
        bonus_label.grid(row=row, column=column, sticky=E)
        bonus_entry = Entry(self, font=font, width=35, bg=BG1)
        bonus_entry.grid(row=row, column=column + 1)

        # 分割
        row += 1
        Label(self, text="", font=("宋体", 25), width=100, bg=BG).grid(row=row, columnspan=5)

        # 备注
        row += 1
        note_label = Label(self, text="备注:", font=font, width=20, height=2, bg=BG)
        note_label.grid(row=row, column=column, sticky=E)
        note_entry = Entry(self, font=font, width=35, bg=BG1)
        note_entry.grid(row=row, column=column + 1)

        # 分割
        row += 1
        Label(self, text="", font=("宋体", 25), width=100, bg=BG).grid(row=row, columnspan=5)

        #  添加按钮
        row += 1
        add_button = Button(self, text="添加", font=font, width=20, height=2, command=lambda: self.addFunction("e"))
        add_button.grid(row=row, column=column + 2)

        def changeToNext(event, next_):
            next_.focus()

        date_entry.bind("<Return>", lambda _next: changeToNext("event", fare_entry))
        fare_entry.bind("<Return>", lambda _next: changeToNext("event", bonus_entry))
        bonus_entry.bind("<Return>", lambda _next: changeToNext("event", note_entry))

        #  注册组件
        self.date_entry = date_entry
        self.fare_entry = fare_entry
        self.bonus_entry = bonus_entry
        self.note_entry = note_entry
        self.add_button = add_button

        # 将添加数据的按钮的功能也绑定到 备注 输入框----》 note_entry
        note_entry.bind("<Return>", self.addFunction)

    def addFunction(self, event):
        # 创建表对象
        dataDao = DataDao()
        # 获取历史数据
        his_data = dataDao.getHistoryData()
        # 原来的余额
        yu_e = float(his_data[-1][-2])

        # 用户输入的数据
        date = self.date_entry.get()
        fare = self.fare_entry.get()
        bonus = float(self.bonus_entry.get())
        money = float(yu_e - float(bonus))  # 新的余额
        note = self.note_entry.get()

        #  设置新的数据
        dataDao.setDate(date)
        dataDao.setFair(fare)
        dataDao.setBonus(bonus)
        dataDao.setMoney(money)
        dataDao.setNote(note)

        # 将数据添加到数据库中
        if dataDao.insertRecord():
            ms_box.showinfo("提示", "数据添加成功！！请刷新数据查看！！")
            return
        ms_box.showerror("错误", '由于某种原因数据添加失败！')


class UpdateDataFrame(Frame):
    def __init__(self, master, **kwargs):
        super(UpdateDataFrame, self).__init__(master, kwargs)
        self.config(bg="#FFF5EE")
        self.widget()

    def widget(self):
        kwargs_button = {"font": ("宋体", 25), "width": 10, "bg": "white"}
        kwargs_label = {"font": ("宋体", 25), "width": 25, "bg": "#FFF5EE", "anchor": "e"}
        kwargs_entry = {"font": ("宋体", 25), "width": 30, "bg": "white"}
        kwargs_other = {"font": ("宋体", 15), "width": 30, "bg": "#FFF5EE"}

        row = 0
        column = 0
        Label(self, text="宿舍日常事务--修改", font=("宋体", 40), width=60, bg="#FFF5EE").grid(row=row, columnspan=3)

        # 分割
        row += 1
        Label(self, text="", **kwargs_other).grid(row=row, columnspan=3)

        row += 1
        date_label = Label(self, text="日期:", **kwargs_label)
        date_label.grid(row=row, column=column)
        date_entry = Entry(self, **kwargs_entry)
        date_entry.grid(row=row, column=column + 1)

        # 分割
        row += 1
        Label(self, text="", **kwargs_other).grid(row=row, columnspan=3)

        row += 1
        fare_label = Label(self, text="事务:", **kwargs_label)
        fare_label.grid(row=row, column=column)
        fare_entry = Entry(self, **kwargs_entry)
        fare_entry.grid(row=row, column=column + 1)

        # 分割
        row += 1
        Label(self, text="", **kwargs_other).grid(row=row, columnspan=3)

        row += 1
        bonus_label = Label(self, text="事务金额:", **kwargs_label)
        bonus_label.grid(row=row, column=column)
        bonus_entry = Entry(self, **kwargs_entry)
        bonus_entry.grid(row=row, column=column + 1)

        # 分割
        row += 1
        Label(self, text="", **kwargs_other).grid(row=row, columnspan=3)

        row += 1
        note_label = Label(self, text="备注:", **kwargs_label)
        note_label.grid(row=row, column=column)
        note_entry = Entry(self, **kwargs_entry)
        note_entry.grid(row=row, column=column + 1)

        # 分割
        row += 1
        Label(self, text="", **kwargs_other).grid(row=row, columnspan=3)

        # 提示
        row += 1
        kwargs_tip = {"font": ("宋体", 15), "width": 90, "bg": "#FFF5EE"}
        Label(self, text="查询是以日期作为主键查询的，即: 输入你需要查询的那条记录的日期即可点击查询", **kwargs_tip).grid(row=row, columnspan=3)

        row += 1
        search_button = Button(self, text="查询", **kwargs_button)
        search_button.grid(row=row, column=column)
        update_button = Button(self, text="修改", **kwargs_button)
        update_button.grid(row=row, column=column + 2)


class JustLookFrame(Frame):
    def __init__(self, master, **kwargs):
        super(JustLookFrame, self).__init__(master, kwargs)
        self.widget()

    def widget(self):
        Button(self, text="仅查看").pack()


class TransToPDFFrame(Frame):
    def __init__(self, master, **kwargs):
        super(TransToPDFFrame, self).__init__(master, kwargs)
        self.widget()

    def widget(self):
        Button(self, text="转化为PDF").pack()


class OutputToExcelFrame(Frame):
    def __init__(self, master, **kwargs):
        super(OutputToExcelFrame, self).__init__(master, kwargs)
        self.widget()

    def widget(self):
        Button(self, text="输出为Excel表格").pack()


class OutputToCSVFrame(Frame):
    def __init__(self, master, **kwargs):
        super(OutputToCSVFrame, self).__init__(master, kwargs)
        self.widget()

    def widget(self):
        Button(self, text="输出为CSV表格").pack()


class OutputToJsonFrame(Frame):
    def __init__(self, master, **kwargs):
        super(OutputToJsonFrame, self).__init__(master, kwargs)
        self.widget()

    def widget(self):
        Button(self, text="转化为Json文件").pack()


class MainFrame(Frame):
    """
                     主界面
        有的组件：
            菜单栏
                添加刷新数据 --- operatePage
                查看       ---  lookPage

            operatePage
                添加（带有刷新按钮）
                    ---- 日期  --- text ---  文本
                        可以填写，默认是当天
                    ---- 事务 --- text ---  文本
                        可以填写，默认是 交水费
                    ---- 事务金额 --- real ---  浮点
                        可以填写，默认是 -11
                    ---- 余额 --- real ---  浮点
                        由上一次的余额计算而来
                    ---- 备注 --- text ---  文本
                        可以填写，也可一直接选择

                修改（带有刷新按钮）
                    每一个字段均可以修改
            lookPage
                查看所有历史记录，按照时间排序
                    显示所有字段
    """

    def __init__(self, root: Tk = None, **kwargs):
        super(MainFrame, self).__init__(root, kwargs)
        self.root = root
        # frame 的一些基本属性
        self.config(bg="#FFF5EE")
        self.current_page = None  # 当前正在挂载的界面
        self.mainPage()  # 将主界面挂载到Frame上
        self.addData()  # 默认主界面的页面是添加数据的页面

    def mainPage(self):
        """
        主界面代码实现
        :return:
                 login_frame 内部界面对象
                 e1  用户名输入输入框
                 e2  用户密码输入输入框
                 b1  用户登录按钮
                 b2  用户用户注册按钮
        """

        # 设置主菜单---- 一个顶级菜单
        mainMenu = Menu(self)
        # 创建下拉菜单 ---- 操作数据
        operateDataMenu = Menu(mainMenu, tearoff=False)
        mainMenu.add_cascade(label="操纵数据", menu=operateDataMenu)
        operateDataMenu.add_command(label="添加", command=self.addData)
        operateDataMenu.add_command(label="修改", command=self.updateData)

        # 创建下拉菜单 ---- 操作数据
        lookDataMenu = Menu(mainMenu, tearoff=False)
        mainMenu.add_cascade(label="查看数据", menu=lookDataMenu)
        lookDataMenu.add_command(label="仅查看", command=self.justLook)
        lookDataMenu.add_command(label="转化为PDF", command=self.transToPDF)
        lookDataMenu.add_command(label="输出为Excel表格", command=self.outputToExcel)
        lookDataMenu.add_command(label="输出为CSV表格", command=self.outputToCSV)
        lookDataMenu.add_command(label="转化为Json文件", command=self.outputToJson)

        self.root.config(menu=mainMenu)

    def addData(self):
        """ 实现 --添加-- 菜单 对应的功能"""
        if self.current_page is not None:
            self.current_page.pack_forget()
        addDataPage = AddDateFrame(self)
        self.current_page = addDataPage
        self.current_page.pack()

    def updateData(self):
        """ 实现 --修改-- 菜单 对应的功能"""
        if self.current_page is not None:
            self.current_page.pack_forget()
        updateDataPage = UpdateDataFrame(self)
        self.current_page = updateDataPage
        self.current_page.pack()

    def justLook(self):
        """ 实现 --仅查看-- 菜单 对应的功能"""
        if self.current_page is not None:
            self.current_page.pack_forget()
        justLookPage = JustLookFrame(self)
        self.current_page = justLookPage
        self.current_page.pack()

    def transToPDF(self):
        """ 实现 --转化为PDF-- 菜单 对应的功能"""
        if self.current_page is not None:
            self.current_page.pack_forget()
        transToPDFPage = TransToPDFFrame(self)
        self.current_page = transToPDFPage
        self.current_page.pack()

    def outputToExcel(self):
        """ 实现 --输出为Excel表格-- 菜单 对应的功能"""
        if self.current_page is not None:
            self.current_page.pack_forget()
        outputToExcelPage = OutputToExcelFrame(self)
        self.current_page = outputToExcelPage
        self.current_page.pack()

    def outputToCSV(self):
        """ 实现 --输出为CSV表格-- 菜单 对应的功能"""
        if self.current_page is not None:
            self.current_page.pack_forget()
        outputToCSVPage = OutputToCSVFrame(self)
        self.current_page = outputToCSVPage
        self.current_page.pack()

    def outputToJson(self):
        """ 实现 --转化为Json文件-- 菜单 对应的功能"""
        if self.current_page is not None:
            self.current_page.pack_forget()
        outputToJsonPage = OutputToJsonFrame(self)
        self.current_page = outputToJsonPage
        self.current_page.pack()
