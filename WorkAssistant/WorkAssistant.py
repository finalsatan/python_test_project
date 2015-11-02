#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose:   check the week report, if it is not exist, send mail to remind me
Version:    2015-06-23
Author:     zyh
"""

import re
import datetime
import http.cookiejar
import urllib.request, urllib.parse, urllib.error
import argparse
import smtplib  
from email.mime.text import MIMEText

class WorkAssistant:
    #send mail to me
    def sendMail(self):
        sender = 'xxxxxx@kmerit.com'  
        receiver = 'xxxxxx@kmerit.com'  
        subject = '周报提醒'  
        smtpserver = 'smtp.exmail.qq.com'  
        username = 'xxxxxx@kmerit.com'  
        password = 'xxxxxx'  
  
        msg = MIMEText('<html><h1>请及时提交本周周报!</h1></html>','html','utf-8')   
        msg['Subject'] = subject  
  
        smtp = smtplib.SMTP()  
        smtp.connect('smtp.exmail.qq.com')  
        smtp.login(username, password)  
        smtp.sendmail(sender, receiver, msg.as_string())  
        smtp.quit()  

    # just for print delimiter
    def printDelimiter(self):
        print("-"*80)

    # main function to emulate login OA
    def emulateLoginOA(self):

        # parse input parameters
        parser = argparse.ArgumentParser()
        parser.add_argument("username",help="Your OA Username")
        parser.add_argument("password",help="Your OA password")
        args = parser.parse_args()

        
        #using cookieJar & HTTPCookieProcessor to automatically handle cookies
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        urllib.request.install_opener(opener)

       
        #[step1] to get cookie
        getCookieUrl = "http://58.240.214.202:8008/login/Login.jsp?logintype=1"
        headersCookieUrl = {
            'Accept'          : 'text/html, application/xhtml+xml, */*',
            'Accept-Language' : 'zh-CN',
            'User-Agent'      : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Accept-Encoding' : 'gzip, deflate',
            'Host'            : '58.240.214.202:8008',
            'Connection'      : 'Keep-Alive'
        }
        reqGetCookie = urllib.request.Request(getCookieUrl, None, headersCookieUrl)
        respGetCookie = urllib.request.urlopen(reqGetCookie)
        

        #[step2] emulate login OA
        oaMainLoginUrl = "http://58.240.214.202:8008/login/VerifyLogin.jsp"
        postData = "loginfile=%2Fwui%2Ftheme%2Fecology7%2Fpage%2Flogin.jsp%3FtemplateId%3D4%26logintype%3D1%26gopage%3D&logintype=1&fontName=%CE%A2%C8%ED%D1%C5%BA%DA&message=&gopage=&formmethod=post&rnd=&serial=&username=&isie=true&submit="
        postData = postData + "&loginid=" + args.username + "&userpassword=" + args.password
        postData = postData.encode(encoding='GBK')     
        headersLogin = {
            'Accept'          : 'text/html, application/xhtml+xml, */*',
            'Accept-Language' : 'zh-CN',
            'User-Agent'      : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Accept-Encoding' : 'gzip, deflate',
            'Host'            : '58.240.214.202:8008',
            'Connection'      : 'Keep-Alive',
            'Referer'         : 'http://58.240.214.202:8008/login/Login.jsp?logintype=1',
            'Content-Type'    : 'application/x-www-form-urlencoded',
            'Cache-Control'   : 'no-cache'
        }        
        reqLogin = urllib.request.Request(oaMainLoginUrl, postData,headersLogin)
        respLogin = urllib.request.urlopen(reqLogin)
              
        #[step3] get the main page of OA
        mainPageOfOAUrl = "http://58.240.214.202:8008/wui/main.jsp?templateId=1"
        headersMainPage = {
            'Accept'          : 'text/html, application/xhtml+xml, */*',
            'Accept-Language' : 'zh-CN',
            'User-Agent'      : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Accept-Encoding' : 'gzip, deflate',
            'Host'            : '58.240.214.202:8008',
            'Connection'      : 'Keep-Alive',
            'Referer'         : 'http://58.240.214.202:8008/login/VerifyLogin.jsp',
            'Content-Type'    : 'application/x-www-form-urlencoded',
            'Cache-Control'   : 'no-cache'
        }

        reqMainPage = urllib.request.Request(mainPageOfOAUrl, None,headersMainPage)
        respMainPage = urllib.request.urlopen(reqMainPage)        
             
        #[step4] get the end content of OA
        endUrl = "http://58.240.214.202:8008/page/element/compatible/WorkflowTabContentData.jsp?tabId=3&ebaseid=8&eid=3&styleid=1419240666581&hpid=3&subCompanyId=5&e71434705692453=&tabsize=6&e71434705699104="
        headersEnd = {
            'Accept'          : 'text/html, application/xhtml+xml, */*',
            'Accept-Language' : 'zh-CN',
            'User-Agent'      : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Accept-Encoding' : 'gzip, deflate',
            'Host'            : '58.240.214.202:8008',
            'Connection'      : 'Keep-Alive',
            'Referer'         : 'http://58.240.214.202:8008/homepage/Homepage.jsp?hpid=3&subCompanyId=5&isfromportal=1&isfromhp=0',
            'Content-Type'    : 'application/x-www-form-urlencoded',
            'Cache-Control'   : 'no-cache'
        }

        reqEnd = urllib.request.Request(endUrl, None,headersEnd)
        respEnd = urllib.request.urlopen(reqEnd)     
        resultEnd = respEnd.read()  
        
        #[step5] get the processed content of OA
        processedUrl = "http://58.240.214.202:8008/page/element/compatible/WorkflowTabContentData.jsp?tabId=2&ebaseid=8&eid=3&styleid=1419240666581&hpid=3&subCompanyId=5&e71435027500112=&tabsize=6&e71435037514283="
        reqProcessed = urllib.request.Request(processedUrl, None,headersEnd)
        respProcessed = urllib.request.urlopen(reqProcessed)   
        resultProcessed = respProcessed.read()  
              
        #get the week num
        weekNum = datetime.datetime.now().isocalendar()
        iWeekNum = weekNum[1]
        sWeekNum = "周数:" + str(iWeekNum)
        sWeekNum = sWeekNum.encode('GBK')
                
        if((resultEnd.find(sWeekNum)>=0) or (resultProcessed.find(sWeekNum)>=0)):
            print("not send mail")
            pass
        else:        
            print("send mail")
            self.sendMail()

if __name__=="__main__":
    wa = WorkAssistant()
    wa.emulateLoginOA()
