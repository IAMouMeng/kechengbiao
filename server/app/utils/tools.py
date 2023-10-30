from time import localtime
import re

def getWeeksInfo(text):
    pattern = r'周([一二三四五六日])第(\d+(?:,\d+)?)节\{第(\d+)-(\d+)周(?:\|(?:单|双)周)?\}'
    matches = re.search(pattern, text)
    day_of_week = matches.group(1)  # 周几
    periods = matches.group(2)      # 节次
    start_week = matches.group(3)   # 开始周
    end_week = matches.group(4)     # 结束周
    return {
        "day":day_of_week,
        "periods":periods.split(","),
        "start":int(start_week),
        "end":int(end_week)
    }


def getTagContent(html, tag):
    pattern = r'<{tag}[^>]*>(.*?)</{tag}>'.format(tag=tag)
    matches = re.findall(pattern, html, re.DOTALL)
    return matches[0]


def trimKeyword(text):
    blackList = ["早晨","上午","下午","晚上","\xa0"]

    if not text:
        return True

    if len(text) in (3, 4):
        return True
    
    for i in blackList:
        if i in text:
            return True
        
    return False

def toUtf8(content):
    return content.encode('utf-8', errors='ignore').decode('utf-8')

def trimContent(content):
    return content.replace("\n","").replace("\r","").replace(" ","")

def trimAndMathGPA(matrix):
    for mi,mv in enumerate(matrix):
        
        if "◆" in mv[1]:
            matrix[mi][1] = mv[1].replace("◆" ,"")

        if "." not in mv[7] and mv[7] != "0":
            matrix[mi][7] += ".0"
            
        for vi,vv in enumerate(mv):
            
            if vv == "\xa0":
                matrix[mi][vi] = ""
        
        if isChinese(mv[3]):
            gpa = mv[3]
        else:
            if mv[5] != "" and mv[6] == "":
                if int(mv[5]) >= 60 and int(mv[5]) < 75:
                    gpa = "1.0"
                elif int(mv[5]) >= 75 and int(mv[5]) < 90:
                    gpa = "2.0"
                elif int(mv[5]) >= 90:
                    gpa = "3.0"
                else:
                    gpa = "0"
            elif mv[6] != "":
                if int(mv[6]) >= 60 and int(mv[6]) < 75:
                    gpa = "1.0"
                elif int(mv[6]) >= 75 and int(mv[6]) < 90:
                    gpa = "2.0"
                elif int(mv[6]) >= 90:
                    gpa = "3.0"
                else:
                    gpa = "0"
            else:
                gpa = str(round(int(mv[3])/10-5,1)) if int(mv[3]) > 59 else "0"
            
            if "." not in gpa and gpa != "0":
                gpa += ".0"
            
        matrix[mi].append(gpa)

def mathYearAndXq(year,semester):
    yearNow = localtime().tm_year
    monthNow = localtime().tm_mon
    
    if not year:
        year = str(yearNow - 1) + "-" +  str(yearNow) 
    else:
        info = year.split("-")
        if len(info) != 2 or not info[0].isdigit() or not info[1].isdigit() or int(info[0]) < 2000 or int(info[0]) > yearNow or int(info[1]) > yearNow + 1:
            year = str(yearNow - 1) + "-" + str(yearNow) 
        else:
            if int(info[0]) > int(info[1]):
                year = info[1] + "-" + info[0]
            elif int(info[0]) == int(info[1]):
                year = info[1] + "-" + str(int(info[1])-1)

    if semester not in ["1","2","3"]:
        if monthNow in [12,1,2,3,4,5]:
            semester = "1"
        elif monthNow in [6,7,8,9,10,11]: # 便于阅读 和调整
            semester = "2"
        # 考试月：7月 1月 提前一个月开始默认展示期末成绩
    
    return year,semester

def isChinese(character):
    for cha in character:
        if not '\u0e00' <= cha <= '\u9fa5':
            return False
    else:
        return True