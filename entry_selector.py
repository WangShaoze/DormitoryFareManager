# from tkinter import *
#
# root = Tk()
#
# root.geometry("900x800")
# e = Entry(root)
# e.pack()
#
#
# def selection(event):
#     pass
#
#
# e.bind("<Button-3>", selection)  # 将事件绑定到鼠标的右键
# root.mainloop()


from tkinter import *

window = Tk()
window.title("下拉菜单示例")
window.geometry("900x800")


def entry_selectors(master: Tk or Frame, obj: Entry, options_: list or set):
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


options_1 = ["小王付钱", "小黄付钱", "小苏付钱", "小平付钱", "小苏付钱"]
f = Frame(window)
e = Entry(f)
e.pack()
entry_selectors(f, e, options_1)

e = Entry(f)
e.pack()
entry_selectors(window, e, options_1)
f.pack()
window.mainloop()
