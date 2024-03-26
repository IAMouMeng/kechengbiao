import requests
import ddddocr
from datetime import datetime
from re import findall
from bs4 import BeautifulSoup
from app.utils.tools import toUtf8,trimContent,trimAndMathGPA,trimKeyword,getTagContent

requests.Response.encoding = "GBK"

class System:
    def __init__(self) -> None:
        self.url = "http://124.93.201.59:84/"
        self.cookie = None
        self.stuId = None
        self.stuName = None

    def GetCode(self):
        try:
            response = requests.get(f"{self.url}/CheckCode.aspx",timeout=5)
            self.cookie = response.headers["Set-Cookie"]
            return ddddocr.DdddOcr(show_ad=False).classification(response.content)
        except:
            return False

    def Login(self,username,password):
        
        url = f"{self.url}/default2.aspx"

        code = self.GetCode()
        
        if not code:
            return False,"教务系统异常"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie":self.cookie,
            "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        }

        try:
            response = requests.get(url,headers=headers,allow_redirects=False,timeout=5)
            html = trimContent(toUtf8(response.text))
            __VIEWSTATE = findall(r'\_\_VIEWSTATE\"value\=\"(.*?)\"', html)[0]
    
            data = {
                "__VIEWSTATE":__VIEWSTATE,
                "txtUserName":username,
                "TextBox2":password,
                "txtSecretCode":code,
                "Button1":""
            }
    
            response = requests.post(url,headers=headers,data=data,allow_redirects=False,timeout=5)
    
            html = trimContent(toUtf8(response.text))
    
            if response.status_code == 302 and "/xs_main.aspx?xh=" in response.headers["Location"]:
                self.stuId = username
                return True,None
            elif "请登录" in html:
                if "验证码不正确" in html:
                    return False,"请重新登录" # CODE INCORRECT
    
                if "用户名不存在" in html:
                    return False,"用户名错误" # USERNAME INCORRECT
    
                if "密码错误" in html:
                    
                    try:
                        limitLoginCount = findall(r'您还有(.*?)次尝试机会', html)[0] # 预留
                    except:
                        return False,f"账号锁定"
                        
                    return False,f"密码错误" # PASSWORD INCORRECT
    
            else:
                return False,"未知错误" # UNKNOWN ERROR
        except:
            return False,"教务系统异常"
             
        
    
    def GetScore(self,stuYear,stuSem):
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie":self.cookie,
            "Referer":"http://124.93.201.59:84/",
            "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        }

        response = requests.get(f"{self.url}/xscj.aspx?xh={self.stuId}",headers=headers,allow_redirects=False,timeout=5)
        html = trimContent(toUtf8(response.text))

        try:
            __VIEWSTATE = findall(r'\_\_VIEWSTATE\"value\=\"(.*?)\"', html)[0]

        
            data = {
                "Button1":"%B0%B4%D1%A7%C6%DA%B2%E9%D1%AF",
                "ddlXQ":stuSem,
                "ddlXN":stuYear,
                "__VIEWSTATE":__VIEWSTATE
            }

            response = requests.post(f"{self.url}/xscj.aspx?xh={self.stuId}",headers=headers,data=data,allow_redirects=False,timeout=5)

            html = trimContent(toUtf8(response.text)).replace('</span><spanid="Label7">',"")
            
            reStuInfo = findall(r'Label[5-9]\"\>(.*?)\<\/', html)
            
            stuInfo = {}

            for info in reStuInfo:
                info = info.split("：")
                stuInfo[info[0]] = info[1]


            soup = BeautifulSoup(toUtf8(response.text), 'html.parser')

            tableRows = soup.select('table.datelist')[0].find_all('tr')[1:]
            stuScore = [[cell.get_text() for cell in row.find_all('td')] for row in tableRows]

            trimAndMathGPA(stuScore)
            
            return stuInfo,stuScore
        except:
            return None,None
    
    def GetCourses(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie":self.cookie,
            "Cache-Control":"no-cache",
            "Referer":"http://124.93.201.59:84/",
            "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        }
        try:

            # response = requests.get(f"{self.url}//xskbcx.aspx?xh={self.stuId}",headers=headers,allow_redirects=False,timeout=5)
            
                
            # html = trimContent(toUtf8(response.text))
            
            # __VIEWSTATE = findall(r'\_\_VIEWSTATE\"value\=\"(.*?)\"', html)[0]
            
            data = {
                # "__EVENTTARGET":"xqd",
                # "__VIEWSTATE":__VIEWSTATE,
                # "xqd":2 if datetime.now().month in [2,3,4,5,6,7,8] else 1,
            }
            
            response = requests.post(f"{self.url}/xskbcx.aspx?xh={self.stuId}",data=data,headers=headers,allow_redirects=False,timeout=5)

            soup = BeautifulSoup(toUtf8(response.text), 'html.parser')

            tableRows = soup.select('table.blacktab')[0].find_all('tr')[1:]

            course = [[trimContent(getTagContent(cell.prettify(),"td")) for cell in row.find_all('td')] for row in tableRows]

            trimCourse = []
            for day in course:
                for name in day:
                    for n in name.split("<br/><br/>"):
                        if not trimKeyword(n):
                            trimCourse.append(n.split("<br/>"))
            
            return trimCourse
        except Exception as e:
            print(e)
            return None
    