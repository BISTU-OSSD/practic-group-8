import json
import os

# 数据文件路径
DATA_PATH = "data/course.json"

# 自动创建data文件夹，不存在就新建
if not os.path.exists("data"):
    os.mkdir("data")

# 读取现有课程数据
def load_courses():
    if not os.path.exists(DATA_PATH):
        # 文件不存在，创建空文件
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# 保存课程到json文件
def save_courses(course_list):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(course_list, f, ensure_ascii=False, indent=2)

# 1. 新增课程
def add_course(course_info):
    courses = load_courses()
    # 自动分配最大id+1
    if len(courses) == 0:
        new_id = 1
    else:
        new_id = max(item["id"] for item in courses) + 1
    course_info["id"] = new_id
    courses.append(course_info)
    save_courses(courses)
    return {"status": "success", "msg": "课程新增完成", "data": course_info}

# 2. 根据ID修改课程
def update_course(target_id, new_info):
    courses = load_courses()
    for item in courses:
        if item["id"] == target_id:
            new_info["id"] = target_id
            idx = courses.index(item)
            courses[idx] = new_info
            save_courses(courses)
            return {"status": "success", "msg": f"ID{target_id}课程修改成功"}
    return {"status": "fail", "msg": f"未找到ID={target_id}的课程"}

# 3. 删除课程 + 删除后ID全部重排连续
def delete_course(target_id):
    courses = load_courses()
    new_courses = [item for item in courses if item["id"] != target_id]
    # 重新顺序赋值id
    for index, course in enumerate(new_courses):
        course["id"] = index + 1
    save_courses(new_courses)
    return {"status": "success", "msg": f"ID{target_id}课程已删除，ID自动重排完成"}

# 4. 获取全部课程
def get_all_courses():
    return load_courses()

# 测试代码
if __name__ == "__main__":
    # 1.测试新增课程
    test_course = {
        "name": "大学英语",
        "credit": 3,
        "teacher": "李老师",
        "week_type": "单双周",
        "week_range": [1,16],
        "hours": 48
    }
    print("===新增课程测试===")
    res1 = add_course(test_course)
    print(res1)

    # 2.测试修改课程（修改id=1的课程）
    print("\n===修改课程测试===")
    new_info = {
        "name": "大学英语上册",
        "credit": 3,
        "teacher": "李老师",
        "week_type": "单双周",
        "week_range": [1,16],
        "hours": 48
    }
    res2 = update_course(1, new_info)
    print(res2)

    # 3.查看所有课程
    print("\n===查询全部课程===")
    all = get_all_courses()
    print(all)

    # 4.测试删除课程
    print("\n===删除课程测试===")
    res3 = delete_course(1)
    print(res3)

    # 删除后再次查看
    print("\n===删除后课程列表===")
    print(get_all_courses())