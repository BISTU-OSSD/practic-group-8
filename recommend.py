from typing import List, Dict

# ====================== 权重配置 ======================
WEIGHT_CREDIT = 2.5      # 学分权重
WEIGHT_DIFFICULTY = 3.0  # 难度权重
WEIGHT_REMAIN = 1.8      # 剩余课时权重
HOUR_PER_CLASS = 1.2     # 每节课建议复习时长(h)
# =====================================================


def get_recommend_schedule(progress_data: Dict) -> List[Dict]:
    """
    根据B模块统计结果生成推荐列表
    """

    course_list = progress_data["course_list"]

    recommend_result = []

    for course in course_list:

        remain = course["remain"]

        if remain <= 0:
            priority_score = 0
            estimate_hour = 0
        else:

            base_score = (
                course["credit"] * WEIGHT_CREDIT +
                course["difficulty"] * WEIGHT_DIFFICULTY +
                remain * WEIGHT_REMAIN
            )

            progress_factor = 1 + (100 - course["percent"]) / 100

            priority_score = round(base_score * progress_factor, 1)

            estimate_hour = round(remain * HOUR_PER_CLASS, 1)

        recommend_result.append({

            "course_name": course["course_name"],

            "priority_score": priority_score,

            "credit": course["credit"],

            "difficulty": course["difficulty"],

            "remain_classes": remain,

            "total_classes": course["total_classes"],

            "finished_classes": course["finished"],

            "complete_percent": course["percent"],

            "estimate_review_hour": estimate_hour

        })

    recommend_result.sort(
        key=lambda x: (
            x["priority_score"],
            x["remain_classes"]
        ),
        reverse=True
    )

    return recommend_result


# ====================== 工具函数 ======================

def filter_unfinished_courses(recommend_list):

    return [
        item
        for item in recommend_list
        if item["remain_classes"] > 0
    ]


def get_top_n_recommend(recommend_list, top_n=5):

    return filter_unfinished_courses(recommend_list)[:top_n]


# ====================== 本地测试 ======================
if __name__ == "__main__":

    mock_data = {
        "course_list": [
            {
                "course_name": "高等数学",
                "credit": 5,
                "difficulty": 5,
                "total_classes": 15,
                "finished": 7,
                "remain": 8,
                "percent": 46.7
            },
            {
                "course_name": "Python",
                "credit": 3,
                "difficulty": 4,
                "total_classes": 11,
                "finished": 6,
                "remain": 5,
                "percent": 54.5
            }
        ]
    }

    result = get_recommend_schedule(mock_data)

    for i in result:
        print(i)