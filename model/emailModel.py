import smtplib
from email.mime.text import MIMEText
import random

class EmailModel():
    def __init__(self):
        
        #设置服务器所需信息
        #163邮箱服务器地址
        self.mail_host = 'smtp.163.com'  
        #163用户名
        self.mail_user = 'x2352798581@163.com'  
        #授权码
        self.mail_pass = 'XJVEZVUZLBABSAHI'   
        #邮件发送方邮箱地址
        self.sender = 'x2352798581@163.com'  
        # #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发---------------先默认就发一个，不用列表
        self.receivers = ""

    def codeGenerate(self):
        code = ""
        for i in range(6):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            code += ch
        print(code)
        return code

    def registerEmail(self,receiver:str):
        self.receivers = receiver
        #设置email信息
        #邮件内容设置
        code = self.codeGenerate()
        # print(code)
        content = "欢迎注册语音技术吧。\n您此次操作的验证码为："+code
        message = MIMEText(content,'plain','utf-8')
        #邮件主题       
        title = "语音技术吧"
        message['Subject'] = title 
        #发送方信息
        message['From'] = self.sender 
        #接受方信息     
        message['To'] = self.receivers  

        #登录并发送邮件
        try:
            smtpObj = smtplib.SMTP()
            #连接到服务器
            smtpObj.connect(self.mail_host,25)
            #登录到服务器
            smtpObj.login(self.mail_user,self.mail_pass) 
            #发送
            smtpObj.sendmail(
                self.sender,self.receivers,message.as_string()) 
            #退出
            smtpObj.quit() 
            print('成功发送邮件')
            return code
        except smtplib.SMTPException as e:
            print('发送邮件失败',e) 
    
if __name__ == "__main__":
    emailmodel = EmailModel()
    emailmodel.codeGenerate()
    code = emailmodel.registerEmail("1111@qq.com")