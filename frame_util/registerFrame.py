from tkinter import *


class RegisterFrame(Frame):
    def __init__(self, obj: Tk = None, **kwargs):
        super(RegisterFrame, self).__init__(obj, kwargs)

        # 一些必要的属性初始化
        self.user = None  # 输入用户名的输入框
        self.pwd = None  # 输入密码的输入框
        self.go_login = None  # 去登录按钮

        # 配置Frame的背景颜色
        self.config(bg="#CCFFFF")
        self.registerPage()  # 将 页面上的组件注册到 Frame 上

    def registerPage(self):
        """注册页面的实现"""
        row = 0
        column = 0
        bgs = ["#CCFFFF"]
        Label(self, text="~~421的小伙伴，请注册~~", font=("黑体", 20), width=20, bg=bgs[0]).grid(row=row, columnspan=3)

        row += 1
        l1 = Label(self, text="用户:", font=("黑体", 14), width=10, bg="#CCFFFF")
        l1.grid(row=row, column=column)
        self.user = Entry(self, font=("黑体", 14), width=20)
        self.user.grid(row=row, column=column + 1)

        row += 1
        Label(self, font=("黑体", 20), width=20, bg="#CCFFFF").grid(row=row, columnspan=3)

        row += 1
        l2 = Label(self, text="密码:", font=("黑体", 14), width=10, bg="#CCFFFF")
        l2.grid(row=row, column=column)
        self.pwd = Entry(self, font=("黑体", 14), width=20)
        self.pwd.grid(row=row, column=column + 1)
        self.pwd.config(show="*")

        row += 1
        Label(self, font=("黑体", 20), width=20, bg="#CCFFFF").grid(row=row, columnspan=3)

        row += 1
        self.register = Button(self, text='注册', font=("黑体", 18), width=10)
        self.register.grid(row=row, column=column)
        self.go_login = Button(self, text='去登录', font=("黑体", 18), width=10)
        self.go_login.grid(row=row, column=column + 2)
