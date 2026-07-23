import os
import json
from datetime import datetime, date, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSES_PATH = os.path.join(BASE_DIR, "data", "courses.json")
CONFIG_PATH = os.path.join(BASE_DIR, "data", "config.json")

def load_courses():
    with open(COURSES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def str_to_date(s):
    return datetime.strptime(s,"%Y-%m-%d").date()

def get_current_week(target_date, semester_start):
    d=(target_date-semester_start).days
    return 0 if d<0 else d//7+1

def count_remain_weekend(target_date, semester_end):
    c=0
    cur=target_date
    while cur<=semester_end:
        if cur.weekday()>=5:
            c+=1
        cur+=timedelta(days=1)
    return c

def merge_courses(course_list):
    result={}
    for c in course_list:
        name=c["name"]
        if name not in result:
            result[name]={
                "course_name":name,
                "credit":c["credit"],
                "difficulty":c["difficulty"],
                "week_list":set()
            }
        result[name]["week_list"].update(c["week_list"])
        result[name]["credit"]=max(result[name]["credit"],c["credit"])
        result[name]["difficulty"]=max(result[name]["difficulty"],c["difficulty"])
    for v in result.values():
        v["week_list"]=sorted(v["week_list"])
        v["total_classes"]=len(v["week_list"])
    return list(result.values())

def build_course_statistics(course_data,current_week):
    out=[]
    for c in course_data:
        finished=sum(1 for w in c["week_list"] if w<current_week)
        total=c["total_classes"]
        remain=max(total-finished,0)
        percent=0 if total==0 else round(finished/total*100,1)
        out.append({
            "course_name":c["course_name"],
            "credit":c["credit"],
            "difficulty":c["difficulty"],
            "total_classes":total,
            "finished":finished,
            "remain":remain,
            "percent":percent
        })
    return out

def get_all_course_progress(target_date):
    cfg=load_config()
    start=str_to_date(cfg["semester_start"])
    end=str_to_date(cfg["semester_end"])
    current_week=get_current_week(target_date,start)
    return {
        "target_query_date":target_date.strftime("%Y-%m-%d"),
        "current_week":current_week,
        "semester_remain_days":max((end-target_date).days,0),
        "remain_weekend_count":count_remain_weekend(target_date,end),
        "course_list":build_course_statistics(merge_courses(load_courses()),current_week)
    }

if __name__=="__main__":
    print(json.dumps(get_all_course_progress(date.today()),ensure_ascii=False,indent=2))