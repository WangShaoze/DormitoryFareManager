from tkinter import *
from frame_util.loginFrame import LoginFrame
from frame_util.registerFrame import RegisterFrame
from frame_util.mainFrame import MainFrame
from dao.userDao import UserDao
import tkinter.messagebox as msgbox


class Face(Tk):
    def __init__(self, **kwargs):
        super(Face, self).__init__(**kwargs)
        self.setAttributes()

        # 初始化一个 Frame() 的对象, 用于后期切换
        self.current_frame = None  # 表示当前在展示的Frame

    def setAttributes(self, maxim=False, **kwargs):
        """
            设置桌面窗口的基本属性
        """

        FACE_WIDTH = 550  # 软件的宽度
        FACE_HEIGHT = 200  # 软件的高度
        TITLE = "宿舍管理小软件"  # 默认的标题
        BG = "#CCFFFF"  # 默认的背景颜色

        # 传入的参数中有  宽度的 属性，就要按照传入的参数设置
        if "w" in kwargs:
            FACE_WIDTH = kwargs["w"]
        if "wide" in kwargs:
            FACE_WIDTH = kwargs["wide"]

        # 传入的参数中有  高度的 属性，就要按照传入的参数设置
        if "h" in kwargs:
            FACE_HEIGHT = kwargs["h"]
        if "height" in kwargs:
            FACE_HEIGHT = kwargs["height"]

        WIN_WIDTH = self.winfo_screenwidth()  # 获取屏幕的宽度
        WIN_WEIGHT = self.winfo_screenheight()  # 获取屏幕的高度

        if maxim is not True:
            # 设置窗口的大小和剧中显示`
            self.geometry("{}x{}+{}+{}".format(FACE_WIDTH, FACE_HEIGHT, int((WIN_WIDTH - FACE_WIDTH) / 2),
                                               int((WIN_WEIGHT - FACE_HEIGHT) / 2)))  # 实现居中显示
        else:
            self.state("zoomed")

        # 设置标题
        if "title" in kwargs:
            TITLE = kwargs["title"]
        self.title(TITLE)

        # 设置窗口的背景颜色
        if "bg" in kwargs:
            BG = kwargs["bg"]
        if "background" in kwargs:
            BG = kwargs["background"]
        self.config(bg=BG)  # 设置背景颜色

    def login(self):
        """登录实现"""
        loginFrame = LoginFrame(self)
        if self.current_frame is not None:  # 如果当前展示的窗口不是空，则需要忘记当前展示的窗口
            self.current_frame.pack_forget()

        def isUser(event):
            user = loginFrame.user_entry.get()
            pwd = loginFrame.pwd_entry.get()
            # 需要做出提示
            # 当用户名或者密码有问题时
            if user == "" or pwd == "":
                msgbox.showerror("提示", "用户名和密码不为空")
                return
            person = UserDao()
            person.setUser(user)
            person.setPwd(pwd)
            if person.isUser():
                # 在登陆成功之后，需要跳转到主界面
                self.changeFace()
                self.mainPage()
            else:
                msgbox.showerror("提示", "登录失败!!不是421的同志，不能注册！！")

        def changToPwdEntry(event):
            loginFrame.pwd_entry.focus()

        loginFrame.login.config(command=lambda: isUser("e"))
        loginFrame.pwd_entry.bind("<Return>", isUser)
        loginFrame.user_entry.bind("<Return>", changToPwdEntry)

        loginFrame.register.config(command=self.register)
        self.current_frame = loginFrame
        self.current_frame.pack()

    def register(self):
        """ 注册实现 """
        registerFrame = RegisterFrame(self)  # 注册页面，用于用户注册
        if self.current_frame is not None:  # 如果当前展示的窗口不是空，则需要忘记当前展示的窗口
            self.current_frame.pack_forget()

        def insertInfo(event):
            user = registerFrame.user.get()
            pwd = registerFrame.pwd.get()
            if user == "" or pwd == "":
                msgbox.showerror("错误", "用户名和密码不为空")
                return
            person = UserDao()
            person.setUser(user)
            person.setPwd(pwd)
            if person.insertUser():
                msgbox.showinfo("提示", "信息注册成功！！请重新登录！！")
            else:
                msgbox.showerror("提示", "注册失败，请重试！！")

        def changToPwdEntry(event):
            registerFrame.pwd.focus()

        registerFrame.go_login.config(command=self.login)
        registerFrame.register.config(command=lambda: insertInfo("e"))
        registerFrame.pwd.bind("<Return>", insertInfo)
        registerFrame.user.bind("<Return>", changToPwdEntry)
        self.current_frame = registerFrame
        self.current_frame.pack()

    def mainPage(self):
        """ 主界面的实现 """
        mainFrame = MainFrame(self)  # 信息展示界面, 展示界面中应该实现数据的 增删改查
        if self.current_frame is not None:  # 如果当前展示的窗口不是空，则需要忘记当前展示的窗口
            self.current_frame.pack_forget()
        self.current_frame = mainFrame
        self.current_frame.pack()

    def changeFace(self):
        """用于改变窗口的大小和一些基本属性，主要是当用户登录成功之后需要进入主界面时，改变根窗体"""
        self.setAttributes(maxim=True, wide=900, height=600, background="#cdf4ff")


if __name__ == '__main__':
    face = Face()
    face.login()
    face.mainloop()
