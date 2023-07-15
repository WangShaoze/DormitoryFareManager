from tkinter import *


class LoginFrame(Frame):
    """
    实现登录功能的 Frame
    """

    def __init__(self, obj: Tk = None, **params):
        """
                初始化框架的参数，Frame类 对象有的基本属性, 该类的对象都有
        :param obj: 需要放在哪一个界面上时，就传入那个对象
        :param params:  Frame类基本属性
        """
        super(LoginFrame, self).__init__(obj, **params)
        self.config(bg="#CCFFFF")
        self.user_entry = None
        self.pwd_entry = None
        self.login: Button() = None
        self.register: Button() = None
        self.loginPage()

    def loginPage(self):
        """
        登录框中的内部界面
        有的组件：
            用户 --- Label ---> l1 , ---- Entry ---> e1
            密码 --- Label ---> l2 , ---- Entry ---> e2
        :return:
                 login_frame 内部界面对象
                 e1  用户名输入输入框
                 e2  用户密码输入输入框
                 b1  用户登录按钮
                 b2  用户用户注册按钮
        """

        row = 0
        column = 0
        l1 = Label(self, text="421的小伙伴，请登录", font=("黑体", 18), width=20)
        l1.grid(row=row, column=column + 1)
        l1.config(bg="#CCFFFF")

        row += 1
        l1 = Label(self, text="用户:", font=("黑体", 14), width=10, bg="#CCFFFF")
        l1.grid(row=row, column=column)
        e1 = Entry(self, font=("黑体", 14), width=20)
        self.user_entry = e1
        e1.grid(row=row, column=column + 1)

        row += 1
        Label(self, font=("黑体", 20), width=20, bg="#CCFFFF").grid(row=row, columnspan=3)

        row += 1
        l2 = Label(self, text="密码:", font=("黑体", 14), width=10, bg="#CCFFFF")
        l2.grid(row=row + 2, column=column)
        e2 = Entry(self, font=("黑体", 14), width=20)
        self.pwd_entry = e2
        self.pwd_entry.config(show="*")
        e2.grid(row=row + 2, column=column + 1)

        Label(self, font=("黑体", 20), width=20, bg="#CCFFFF").grid(row=row + 3, columnspan=3)

        self.login = Button(self, text='登录', font=("黑体", 18), width=10)
        self.login.grid(row=row + 4, column=column)
        self.register = Button(self, text='注册', font=("黑体", 18), width=10)
        self.register.grid(row=row + 4, column=column + 2)
