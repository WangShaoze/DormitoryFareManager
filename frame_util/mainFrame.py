import csv
import json
from tkinter import *
from dao.dataDao import *
import tkinter.messagebox as ms_box
import time
import xlwt
from tkinter.ttk import Treeview
from tkinter.ttk import Style


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

        # 给Entry对象提供一些可以选择的参数
        today = time.strftime("%Y/%m/%d", time.localtime())
        self.entry_selectors(date_entry, date_entry, options_=[today])
        self.entry_selectors(fare_entry, fare_entry, options_=["交水费", "充宿舍费"])
        self.entry_selectors(bonus_entry, bonus_entry, options_=["-11", "100", "120", "180", "240"])
        self.entry_selectors(note_entry, note_entry, options_=["小王付钱", "小黄付钱", "小苏付钱", "小平付钱", "小苏付钱", "启航付钱", "全员参与"])

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
        money = float(yu_e + float(bonus))  # 新的余额
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

    @staticmethod
    def entry_selectors(master: Tk or Frame or Entry, obj: Entry, options_: list or set):
        """
        :params:
            master    将该选择器放到哪一个对象上，一般是 obj 的 master, 即: master 可能是 Tk 或者是 Frame 的对象
            obj       该选择器针对的对象，选择器最终的结果应该放到 哪个 Entry 对象，obj 就是 那个对象
            options_  为选择器提供可选的值 list 或者 set 都行
        """

        def selection(event, options: list or set):
            """
            :params:
                event    处理事件的对象
                options_ 声明下拉菜单选项内容 ["小王付钱", "小黄付钱", "小苏付钱", "小平付钱", "小苏付钱"]
            """
            # 创建StringVar对象，用于将当前选项选中的内容填写到输入框中
            e_var = StringVar()  # 获取变量
            obj.config(textvariable=e_var)  # 将变量挂载到传入的对象上

            # 创建StringVar对象，用于记录当前选择的选项
            selected_option = StringVar(master)
            selected_option.set(options[0])  # 第一个是默认选项

            def on_change(option):
                """
                当 选项菜单 中的每一个菜单被选中时，需要将 这个值 通过 e_var 传入 obj 这个 输入框中
                """
                e_var.set(option)
                option_menu.pack_forget()  # 不显示显示选项菜单对象

            # 创建选项菜单对象
            option_menu = OptionMenu(master, selected_option, *options, command=on_change)
            option_menu.pack()  # 显示选项菜单对象

        obj.bind("<Button-3>", lambda opts_: selection("e", options_))  # 将事件绑定到鼠标的右键


class UpdateDataFrame(Frame):
    def __init__(self, master, **kwargs):
        super(UpdateDataFrame, self).__init__(master, kwargs)
        self.config(bg="#FFF5EE")
        self.search_button = None
        self.update_button = None
        self.var_date = None
        self.var_fare = None
        self.var_bonus = None
        self.var_note = None

        self.date_entry = None
        self.fare_entry = None
        self.bonus_entry = None
        self.note_entry = None
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
        var_date = StringVar()
        date_label = Label(self, text="日期:", **kwargs_label)
        date_label.grid(row=row, column=column)
        date_entry = Entry(self, textvariable=var_date, **kwargs_entry)
        date_entry.grid(row=row, column=column + 1)

        # 分割
        row += 1
        Label(self, text="", **kwargs_other).grid(row=row, columnspan=3)

        row += 1
        var_fare = StringVar()
        fare_label = Label(self, text="事务:", **kwargs_label)
        fare_label.grid(row=row, column=column)
        fare_entry = Entry(self, textvariable=var_fare, **kwargs_entry)
        fare_entry.grid(row=row, column=column + 1)

        # 分割
        row += 1
        Label(self, text="", **kwargs_other).grid(row=row, columnspan=3)

        row += 1
        var_bonus = StringVar()
        bonus_label = Label(self, text="事务金额:", **kwargs_label)
        bonus_label.grid(row=row, column=column)
        bonus_entry = Entry(self, textvariable=var_bonus, **kwargs_entry)
        bonus_entry.grid(row=row, column=column + 1)

        # 分割
        row += 1
        Label(self, text="", **kwargs_other).grid(row=row, columnspan=3)

        row += 1
        var_note = StringVar()
        note_label = Label(self, text="备注:", **kwargs_label)
        note_label.grid(row=row, column=column)
        note_entry = Entry(self, textvariable=var_note, **kwargs_entry)
        note_entry.grid(row=row, column=column + 1)

        # 分割
        row += 1
        Label(self, text="", **kwargs_other).grid(row=row, columnspan=3)

        # 提示
        row += 1
        kwargs_tip = {"font": ("宋体", 15), "width": 90, "bg": "#FFF5EE"}
        Label(self, text="查询是以日期作为主键查询的，即: 输入你需要查询的那条记录的日期即可点击查询", **kwargs_tip).grid(row=row, columnspan=3)

        row += 1
        search_button = Button(self, text="查询", command=lambda: self.search("e"), **kwargs_button)
        search_button.grid(row=row, column=column)
        update_button = Button(self, text="修改", command=lambda: self.update_task("e"), **kwargs_button)
        update_button.grid(row=row, column=column + 2)

        self.var_date = var_date
        self.var_fare = var_fare
        self.var_bonus = var_bonus
        self.var_note = var_note

        # 特殊情况：
        self.date_entry = date_entry
        self.fare_entry = fare_entry
        self.bonus_entry = bonus_entry
        self.note_entry = note_entry

        self.search_button = search_button
        self.search_button = update_button

        date_entry.bind("<Return>", self.search)
        fare_entry.bind("<Return>", self.update_task)
        bonus_entry.bind("<Return>", self.update_task)
        note_entry.bind("<Return>", self.update_task)

        # 给Entry对象提供一些可以选择的参数
        today = time.strftime("%Y/%m/%d", time.localtime())
        self.entry_selectors(date_entry, date_entry, options_=[today])
        self.entry_selectors(fare_entry, fare_entry, options_=["交水费", "充宿舍费"])
        self.entry_selectors(bonus_entry, bonus_entry, options_=["-11", "100", "120", "180", "240"])
        self.entry_selectors(note_entry, note_entry, options_=["小王付钱", "小黄付钱", "小苏付钱", "小平付钱", "小苏付钱", "启航付钱", "全员参与"])

    def search(self, event):
        """实现查询出对应日期的记录"""
        date = self.var_date.get()
        if date == "" or date is None:
            date = self.date_entry.get()
            if date == "" or date is None:
                ms_box.showinfo("提示", "请输入日期作为查询条件！")
        dataDao = DataDao()
        data = dataDao.search_by_date(date)  # 以日期作为查询条件，查询需要修改的数据
        if len(data) > 1:
            data = data[-1]
        elif len(data) == 1:
            data = data[0]
        else:
            ms_box.showinfo('提示', "数据查询失败！！没有找到对应的记录。")
            return
        fare = data[-4]
        bonus = data[-3]
        note = data[-1]
        # 给输入框赋值显示出查询结果
        self.var_fare.set(fare)
        self.var_bonus.set(bonus)
        self.var_note.set(note)
        # 删除数据库中的 刚刚查询出的 那一条记录
        if dataDao.delete_record_by_columns(date=date, fare=fare, bonus=bonus, note=note):
            ms_box.showinfo('提示', "数据查询成功")
        else:
            ms_box.showinfo('提示', "数据查询失败")

    def update_task(self, event):
        # 查出历史数据，由于在查询的最后一步， 最后一条数据被删除， 原来的倒数第二条数据会变成倒数第一条数据，获取第一条记录的余额
        dataDao = DataDao()
        # 计算 出新的余额
        old_yu_e = float(dataDao.getHistoryData()[-1][-2])
        # 获取 用户修改后的其他各项数据，重新写入数据库
        # date = self.var_date.get()  # 这里在测试过程中发现可能是空值，所以需要做出判断
        # if date == "" or date is None:
        date = self.date_entry.get()  # 如果真的是空值的话，那就需要从 self.date_entry ----> Entry 的对象身上取出来

        # fare = self.var_fare.get()
        # if self.var_fare.get() == "" or self.var_fare.get() is None:
        fare = self.fare_entry.get()

        # bonus = self.var_bonus.get()
        # if self.var_bonus.get() == "" or self.var_bonus.get() is None:
        bonus = self.bonus_entry.get()
        new_yu_e = old_yu_e + float(bonus)

        # note = self.var_note.get()
        # if self.var_note.get() == "" or self.var_note.get() is None:
        note = self.note_entry.get()
        dataDao.setDate(date)
        dataDao.setFair(fare)
        dataDao.setBonus(bonus)
        dataDao.setMoney(new_yu_e)
        dataDao.setNote(note)
        if dataDao.insertRecord():
            ms_box.showinfo("提示", "数据修改成功")
        else:
            ms_box.showerror("错误", "数据修改失败，原来的数据已经删除，请重新添加！！")

    @staticmethod
    def entry_selectors(master: Tk or Frame or Entry, obj: Entry, options_: list or set):
        """
        :params:
            master    将该选择器放到哪一个对象上，一般是 obj 的 master, 即: master 可能是 Tk 或者是 Frame 的对象
            obj       该选择器针对的对象，选择器最终的结果应该放到 哪个 Entry 对象，obj 就是 那个对象
            options_  为选择器提供可选的值 list 或者 set 都行
        """

        def selection(event, options: list or set):
            """
            :params:
                event    处理事件的对象
                options_ 声明下拉菜单选项内容 ["小王付钱", "小黄付钱", "小苏付钱", "小平付钱", "小苏付钱"]
            """
            # 创建StringVar对象，用于将当前选项选中的内容填写到输入框中
            e_var = StringVar()  # 获取变量
            obj.config(textvariable=e_var)  # 将变量挂载到传入的对象上

            # 创建StringVar对象，用于记录当前选择的选项
            selected_option = StringVar(master)
            selected_option.set(options[0])  # 第一个是默认选项

            def on_change(option):
                """
                当 选项菜单 中的每一个菜单被选中时，需要将 这个值 通过 e_var 传入 obj 这个 输入框中
                """
                e_var.set(option)
                option_menu.pack_forget()  # 不显示显示选项菜单对象

            # 创建选项菜单对象
            option_menu = OptionMenu(master, selected_option, *options, command=on_change)
            option_menu.pack()  # 显示选项菜单对象

        obj.bind("<Button-3>", lambda opts_: selection("e", options_))  # 将事件绑定到鼠标的右键


class JustLookFrame(Frame):
    def __init__(self, master, **kwargs):
        super(JustLookFrame, self).__init__(master, kwargs)
        self.widget()

    def widget(self):
        frame_up = Frame(self)

        columns = ('date', 'fare', 'bonus', 'money', 'note')
        s = Style()
        s.theme_use('clam')
        # 添加行高
        s.configure('Treeview', rowheight=40)
        tree = Treeview(frame_up, columns=columns, show="headings", displaycolumns="#all", height=15)

        font_title = ("宋体", 24)
        font_record = ("黑体", 20)
        s.configure("Treeview.Heading", font=font_title)
        s.configure("Treeview.column", font=font_record)
        tree.column("# 1", anchor=E, stretch=NO, width=100 * 2)
        tree.heading('date', text="日期", anchor=E)
        tree.column("# 2", anchor=CENTER, stretch=NO, width=150 * 2)
        tree.heading('fare', text="事务", anchor=CENTER)
        tree.column("# 3", anchor=CENTER, stretch=NO, width=150 * 2)
        tree.heading('bonus', text="事务金额", anchor=CENTER)
        tree.column("# 4", anchor=CENTER, stretch=NO, width=150 * 2)
        tree.heading('money', text="余额", anchor=CENTER)
        tree.column("# 5", anchor=CENTER, stretch=NO, width=230 * 2)
        tree.heading('note', text="备注", anchor=CENTER)

        def refresh(is_first: bool = False):
            def fill_data_to_tree():
                """从数据库中将数据读取出来，然后填充到tree上"""
                history_data = DataDao().getHistoryData()
                for itm in history_data:
                    tree.insert("", END, values=itm)

            if is_first:
                fill_data_to_tree()
            else:
                tree.delete(*tree.get_children())
                fill_data_to_tree()

        refresh(True)
        tree.pack(expand=1, fill=BOTH)
        frame_up.pack()

        frame_down = Frame(self)
        refresh_button = Button(frame_down, text="刷新数据", font=("黑体", 25), fg="blue", bg='grey', command=refresh)
        refresh_button.pack()
        frame_down.pack()


class TransToPDFFrame(Frame):
    def __init__(self, master, **kwargs):
        super(TransToPDFFrame, self).__init__(master, kwargs)
        self.file_name_entry = None
        self.trans_files = "trans_files"
        self.widget()

    def widget(self):
        # 将 数据写到一颗树上，用表的形式显示出来给用户看
        frame_up = Frame(self)

        columns = ('date', 'fare', 'bonus', 'money', 'note')
        s = Style()
        s.theme_use('clam')
        # 添加行高
        s.configure('Treeview', rowheight=40)
        tree = Treeview(frame_up, columns=columns, show="headings", displaycolumns="#all", height=15)

        font_title = ("宋体", 24)
        font_record = ("黑体", 20)
        s.configure("Treeview.Heading", font=font_title)
        s.configure("Treeview.column", font=font_record)
        tree.column("# 1", anchor=E, stretch=NO, width=100 * 2)
        tree.heading('date', text="日期", anchor=E)
        tree.column("# 2", anchor=CENTER, stretch=NO, width=150 * 2)
        tree.heading('fare', text="事务", anchor=CENTER)
        tree.column("# 3", anchor=CENTER, stretch=NO, width=150 * 2)
        tree.heading('bonus', text="事务金额", anchor=CENTER)
        tree.column("# 4", anchor=CENTER, stretch=NO, width=150 * 2)
        tree.heading('money', text="余额", anchor=CENTER)
        tree.column("# 5", anchor=CENTER, stretch=NO, width=230 * 2)
        tree.heading('note', text="备注", anchor=CENTER)

        def refresh(is_first: bool = False):
            def fill_data_to_tree():
                """从数据库中将数据读取出来，然后填充到tree上"""
                history_data = DataDao().getHistoryData()
                for itm in history_data:
                    tree.insert("", END, values=itm)

            if is_first:
                fill_data_to_tree()
            else:
                tree.delete(*tree.get_children())
                fill_data_to_tree()

        refresh(True)
        tree.pack(expand=1, fill=BOTH)
        frame_up.pack()

        frame_down = Frame(self)
        name_label = Label(frame_down, text="请输入文件名:", font=("黑体", 30), fg="#CCFFCC", bg="#333333", width=35)
        name_label.grid(row=0, column=0)
        self.file_name_entry = Entry(frame_down, font=("黑体", 30), width=35)
        self.file_name_entry.grid(row=0, column=1)
        json_button = Button(frame_down, text="转化为PDF", font=("黑体", 25), command=self.trans)
        json_button.grid(row=1, column=1)
        frame_down.pack()

    def trans(self):
        dataDao = DataDao()
        input_file_name = self.file_name_entry.get()
        if input_file_name is None or input_file_name == "":
            ms_box.showinfo("提示", "必须要输入文件名！！")
        if ".pdf" not in input_file_name:
            input_file_name += ".pdf"


class OutputToExcelFrame(Frame):
    def __init__(self, master, **kwargs):
        super(OutputToExcelFrame, self).__init__(master, kwargs)
        self.file_name_entry = None
        self.trans_files = "trans_files"
        self.widget()

    def widget(self):
        # 将 数据写到一颗树上，用表的形式显示出来给用户看
        frame_up = Frame(self)

        columns = ('date', 'fare', 'bonus', 'money', 'note')
        s = Style()
        s.theme_use('clam')
        # 添加行高
        s.configure('Treeview', rowheight=40)
        tree = Treeview(frame_up, columns=columns, show="headings", displaycolumns="#all", height=15)

        font_title = ("宋体", 24)
        font_record = ("黑体", 20)
        s.configure("Treeview.Heading", font=font_title)
        s.configure("Treeview.column", font=font_record)
        tree.column("# 1", anchor=E, stretch=NO, width=100 * 2)
        tree.heading('date', text="日期", anchor=E)
        tree.column("# 2", anchor=CENTER, stretch=NO, width=150 * 2)
        tree.heading('fare', text="事务", anchor=CENTER)
        tree.column("# 3", anchor=CENTER, stretch=NO, width=150 * 2)
        tree.heading('bonus', text="事务金额", anchor=CENTER)
        tree.column("# 4", anchor=CENTER, stretch=NO, width=150 * 2)
        tree.heading('money', text="余额", anchor=CENTER)
        tree.column("# 5", anchor=CENTER, stretch=NO, width=230 * 2)
        tree.heading('note', text="备注", anchor=CENTER)

        def refresh(is_first: bool = False):
            def fill_data_to_tree():
                """从数据库中将数据读取出来，然后填充到tree上"""
                history_data = DataDao().getHistoryData()
                for itm in history_data:
                    tree.insert("", END, values=itm)

            if is_first:
                fill_data_to_tree()
            else:
                tree.delete(*tree.get_children())
                fill_data_to_tree()

        refresh(True)
        tree.pack(expand=1, fill=BOTH)
        frame_up.pack()

        frame_down = Frame(self)
        name_label = Label(frame_down, text="请输入文件名:", font=("黑体", 30), fg="#CCFFCC", bg="#333333", width=35)
        name_label.grid(row=0, column=0)
        self.file_name_entry = Entry(frame_down, font=("黑体", 30), width=35)
        self.file_name_entry.grid(row=0, column=1)
        json_button = Button(frame_down, text="输出为Excel表格", font=("黑体", 25), command=self.trans)
        json_button.grid(row=1, column=1)
        frame_down.pack()

    def trans(self):
        dataDao = DataDao()
        input_file_name = self.file_name_entry.get()
        if input_file_name is None or input_file_name == "":
            ms_box.showinfo("提示", "必须要输入文件名！！")
        if ".xlsx" not in input_file_name:
            input_file_name += ".xlsx"

        # 创建一个Workbook对象
        workbook = xlwt.Workbook()
        # 添加一个sheet页
        sheet = workbook.add_sheet('Sheet1')

        # 写入表头
        title = ["日期", "事务", "事务金额", "余额", "备注"]
        for c in range(len(title)):
            sheet.write(0, c, title[c])

        # 写入数据
        all_data = dataDao.getHistoryData()
        for r in range(len(all_data)):
            for c in range(len(title)):
                sheet.write(r + 1, c, all_data[r][c])
        else:
            # 保存文件
            workbook.save('{}/{}'.format(self.trans_files, input_file_name))
            ms_box.showinfo("提示", "文件保存成功！！")


class OutputToCSVFrame(Frame):
    def __init__(self, master, **kwargs):
        super(OutputToCSVFrame, self).__init__(master, kwargs)
        self.trans_files = "trans_files"
        self.file_name_entry = None
        self.widget()

    def widget(self):
        # 将 数据写到一颗树上，用表的形式显示出来给用户看
        frame_up = Frame(self)

        columns = ('date', 'fare', 'bonus', 'money', 'note')
        s = Style()
        s.theme_use('clam')
        # 添加行高
        s.configure('Treeview', rowheight=40)
        tree = Treeview(frame_up, columns=columns, show="headings", displaycolumns="#all", height=15)

        font_title = ("宋体", 24)
        font_record = ("黑体", 20)
        s.configure("Treeview.Heading", font=font_title)
        s.configure("Treeview.column", font=font_record)
        tree.column("# 1", anchor=E, stretch=NO, width=100 * 2)
        tree.heading('date', text="日期", anchor=E)
        tree.column("# 2", anchor=CENTER, stretch=NO, width=150 * 2)
        tree.heading('fare', text="事务", anchor=CENTER)
        tree.column("# 3", anchor=CENTER, stretch=NO, width=150 * 2)
        tree.heading('bonus', text="事务金额", anchor=CENTER)
        tree.column("# 4", anchor=CENTER, stretch=NO, width=150 * 2)
        tree.heading('money', text="余额", anchor=CENTER)
        tree.column("# 5", anchor=CENTER, stretch=NO, width=230 * 2)
        tree.heading('note', text="备注", anchor=CENTER)

        def refresh(is_first: bool = False):
            def fill_data_to_tree():
                """从数据库中将数据读取出来，然后填充到tree上"""
                history_data = DataDao().getHistoryData()
                for itm in history_data:
                    tree.insert("", END, values=itm)

            if is_first:
                fill_data_to_tree()
            else:
                tree.delete(*tree.get_children())
                fill_data_to_tree()

        refresh(True)
        tree.pack(expand=1, fill=BOTH)
        frame_up.pack()

        frame_down = Frame(self)
        name_label = Label(frame_down, text="请输入文件名:", font=("黑体", 30), fg="#CCFFCC", bg="#333333", width=35)
        name_label.grid(row=0, column=0)
        self.file_name_entry = Entry(frame_down, font=("黑体", 30), width=35)
        self.file_name_entry.grid(row=0, column=1)
        json_button = Button(frame_down, text="转化为CSV文件", font=("黑体", 25), command=self.trans)
        json_button.grid(row=1, column=1)
        frame_down.pack()

    def trans(self):
        dataDao = DataDao()
        input_file_name = self.file_name_entry.get()
        if input_file_name is None or input_file_name == "":
            ms_box.showinfo("提示", "必须要输入文件名！！")
        if ".csv" not in input_file_name:
            input_file_name += ".csv"
        with open(self.trans_files + '/' + input_file_name, mode='w', encoding="utf-8") as f:
            f.write("{},{},{},{},{}\n".format("日期", "事务", "事务金额", "余额", "备注"))
            for uni in dataDao.getHistoryData():
                f.write("{},{},{},{},{}\n".format(*uni))
                f.flush()
            else:
                ms_box.showinfo("提示", "文件保存成功！！")


class OutputToJsonFrame(Frame):
    """
    将数据库中的记录转化为json格式的数据

    思路： 读取数据库中的数据，每一条记录用字典存储，所有记录放到一个列表中
    """

    def __init__(self, master, **kwargs):
        super(OutputToJsonFrame, self).__init__(master, kwargs)
        self.trans_files = "trans_files"
        self.file_name_entry = None
        self.widget()

    def widget(self):
        # 将 数据写到一颗树上，用表的形式显示出来给用户看
        frame_up = Frame(self)

        columns = ('date', 'fare', 'bonus', 'money', 'note')
        s = Style()
        s.theme_use('clam')
        # 添加行高
        s.configure('Treeview', rowheight=40)
        tree = Treeview(frame_up, columns=columns, show="headings", displaycolumns="#all", height=15)

        font_title = ("宋体", 24)
        font_record = ("黑体", 20)
        s.configure("Treeview.Heading", font=font_title)
        s.configure("Treeview.column", font=font_record)
        tree.column("# 1", anchor=E, stretch=NO, width=100 * 2)
        tree.heading('date', text="日期", anchor=E)
        tree.column("# 2", anchor=CENTER, stretch=NO, width=150 * 2)
        tree.heading('fare', text="事务", anchor=CENTER)
        tree.column("# 3", anchor=CENTER, stretch=NO, width=150 * 2)
        tree.heading('bonus', text="事务金额", anchor=CENTER)
        tree.column("# 4", anchor=CENTER, stretch=NO, width=150 * 2)
        tree.heading('money', text="余额", anchor=CENTER)
        tree.column("# 5", anchor=CENTER, stretch=NO, width=230 * 2)
        tree.heading('note', text="备注", anchor=CENTER)

        def refresh(is_first: bool = False):
            def fill_data_to_tree():
                """从数据库中将数据读取出来，然后填充到tree上"""
                history_data = DataDao().getHistoryData()
                for itm in history_data:
                    tree.insert("", END, values=itm)

            if is_first:
                fill_data_to_tree()
            else:
                tree.delete(*tree.get_children())
                fill_data_to_tree()

        refresh(True)
        tree.pack(expand=1, fill=BOTH)
        frame_up.pack()

        frame_down = Frame(self)
        name_label = Label(frame_down, text="请输入文件名:", font=("黑体", 30), fg="#CCFFCC", bg="#333333", width=35)
        name_label.grid(row=0, column=0)
        self.file_name_entry = Entry(frame_down, font=("黑体", 30), width=35)
        self.file_name_entry.grid(row=0, column=1)
        json_button = Button(frame_down, text="转化为Json文件", font=("黑体", 25), command=self.trans)
        json_button.grid(row=1, column=1)
        frame_down.pack()

    def trans(self):
        dataDao = DataDao()
        write_to_json_data = [eval('{' + '"日期":"{}", "事务":"{}", "事务金额":{}, "余额":{}, "备注":"{}"'.format(*uni) + '}') for
                              uni in dataDao.getHistoryData()]
        input_file_name = self.file_name_entry.get()
        if input_file_name is None or input_file_name == "":
            ms_box.showinfo("提示", "必须要输入文件名！！")
        if ".json" not in input_file_name:
            input_file_name += ".json"
        with open(self.trans_files + '/' + input_file_name, mode='w', encoding="utf-8") as f:
            json.dump(obj=write_to_json_data, fp=f, indent=4, ensure_ascii=False)
            ms_box.showinfo("提示", "文件保存成功！！")


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
