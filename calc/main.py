from tkinter import *

class calculator:
    
    # 窗口初始化
    def __init__(self):
        self.isRegister = False # 激活码使用情况
        

        
        window = Tk() # 初始化窗口
        window.title('Calc') # 设置窗口标题
        window.configure(background="black") # 设置窗口背景颜色
        window.resizable(False,False)  # 不允许改变窗口大小
        
        # 设置空白区域
        space = Label(window, width=30, height=3, bg='#000')
        space.grid(row=0, column=0, columnspan=20, sticky=(N, W, E), padx=2) # 设置对齐方式 N,E,W 代表与左上右的边框关联

        self.string = StringVar() # 输入框关联字符串

        # 设置输入框
        entry = Entry(window, textvariable=self.string,width=18, font=("Calibri", 18)) # textvariable 绑定组件显示的文本
        entry.grid(row=1, column=0, columnspan=20, sticky=(N, W, E), padx=2)
        entry.configure(bg="#000")
        entry.configure(fg="#fff")
        entry.configure(relief="flat") # 设置输入框样式为平面（flat）样式
        entry.focus() # 设置焦点到输入框

        ops = ["AC", "C", "%", "/",
               "7", "8", "9", "*",
               "4", "5", "6", "-",
               "1", "2", "3", "+",
               "0", ".", "="] # 所有按钮集合

        colLine = ["AC", "C", "%"] # 列单独配色按钮
        rowLine = ["/", "*", "-", "+", "="] # 行单独配色按钮
        i = 0 # 循环次数
        row = 2 # 当前 grid 行数，初始为第二行
        col = 0 # 当前 grid 列数，初始最左边
        for op in ops:
            padx = 10 # 水平边距
            pady = 10 # 垂直边距
            # 每 4 个换行
            if(i % 4 == 0 and i != 0):
                row = row+1 
                col = 0 # 重置列到最左边
            

            # 判断各种类型操作符
            if(op == "0"):
                btn = Button(window, height=2, width=13, padx=padx, pady=pady,
                             relief="flat", text=op, command=lambda txt=op: self.addChar(txt)) # command 点击按钮事件
                btn.grid(row=row, column=col, columnspan=2, padx=2, pady=2) # 设置 grid 布局
            elif(op in [".", "="]):
                if(op == "="):
                    btn = Button(window, height=2, width=4, padx=padx, pady=pady,
                                 relief="flat", text=op, command=lambda txt=op: self.equals(window))
                else:
                    btn = Button(window, height=2, width=4, padx=padx, pady=pady,
                                 relief="flat", text=op, command=lambda txt=op: self.addChar(txt))
                btn.grid(row=row, column=col+1, columnspan=1, padx=2, pady=2) # 因为按钮 0 占用两格，所以按钮 . 和 = 的列位置要加 1 即 col+1
            else:
                if(op == "C"):
                    btn = Button(window, height=2, width=4, padx=padx, pady=pady,
                                 relief="flat", text=op, command=lambda txt=op: self.delete())
                elif(op == "AC"):
                    btn = Button(window, height=2, width=4, padx=padx, pady=pady,
                                 relief="flat", text=op, command=lambda txt=op: self.clearall())
                else:
                    btn = Button(window, height=2, width=4, padx=padx, pady=pady,
                                 relief="flat", text=op, command=lambda txt=op: self.addChar(txt))
                btn.grid(row=row, column=col, padx=2, pady=2)


            # 行列特殊按钮样式设置
            if(op in colLine):
                btn.configure(bg="#a5a5a5")
                btn.configure(fg="#000")
            elif(op in rowLine):
                btn.configure(bg="#efa43e")
                btn.configure(fg="#fff")
            else:
                btn.configure(bg="#333333")
                btn.configure(fg="#fff")

            col = col+1
            i = i+1
        window.mainloop() # 进入到事件循环

    # 清空输入框
    def clearall(self): 
        self.string.set("")

    # 计算结果
    def equals(self, window):

        # 如果没有使用优惠券
        if(not self.isRegister):
            tk = Toplevel(window) # 新建消息弹窗
            tk.wm_attributes('-topmost', 1) # 置顶窗口
            codeLabel = Label(tk, text="请输入优惠券：").grid(row=0, column=0)
            entry = Entry(tk, width=20)
            entry.grid(row=0, column=1)
            btn = Button(tk, text="提交", width=40, command=lambda txt=entry.get(): self.checkCode(entry.get(),entry,tk))
            btn.grid(row=1, column=0, columnspan=2)
            tk.grab_set() # 禁用背景窗口
            return

        result = ""
        try:
            result = eval(self.string.get()) # 计算结果
            self.string.set(result)
        except:
            result = "无效输入"
        self.string.set(result)

    # 添加操作符到 string 变量中
    def addChar(self, char):
        self.string.set(self.string.get()+(str(char)))
    
    # 删除最后一位操作符
    def delete(self):
        self.string.set(self.string.get()[0:-1])

    # 检查优惠券
    def checkCode(self, code,entry,tk):
        import requests
        import json
        url = "http://127.0.0.1:5000/ajax/coupon/check"
        payload = {'code': code}
        response = requests.request("POST", url, data=payload) # 发送请求到服务器验证优惠券
        result = json.loads(response.text) # 返回结果转对象

        self.isRegister = result["status"]
        entry.delete(0,END)
        entry.insert(0,result["msg"])
        if(self.isRegister):
            tk.destroy() # 销毁消息弹窗


if __name__ == "__main__":
    # 启动计算器
    calculator()
