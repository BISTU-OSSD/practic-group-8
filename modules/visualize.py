BAR_LEN = 30
FILL = "█"
EMPTY = "─"


def _make_bar(percent):
    fill = int(BAR_LEN * percent / 100)
    return FILL * fill + EMPTY * (BAR_LEN - fill)


def draw_course_progress_bar(progress_info):
    """
    main.py直接调用
    """

    print("\n========== 课程学习进度 ==========\n")

    print(f"查询日期：{progress_info['target_query_date']}")
    print(f"当前教学周：第{progress_info['current_week']}周")
    print(f"距离学期结束：{progress_info['semester_remain_days']}天")
    print(f"剩余周末：{progress_info['remain_weekend_count']}天\n")

    for course in progress_info["course_list"]:

        bar = _make_bar(course["percent"])

        print(
            f"{course['course_name']}"
        )

        print(
            f"[{bar}] "
            f"{course['finished']}/{course['total_classes']} "
            f"({course['percent']}%)"
        )

        print(
            f"剩余课次：{course['remain']}"
        )

        print("-" * 60)


def draw_recommend_rank_bar(recommend_list):
    """
    main.py直接调用
    """

    print("\n========== 复习优先级 ==========\n")

    if len(recommend_list) == 0:
        print("暂无推荐课程")
        return

    max_score = max(
        item["priority_score"]
        for item in recommend_list
    )

    if max_score == 0:
        max_score = 1

    for index, item in enumerate(recommend_list, start=1):

        percent = item["priority_score"] / max_score * 100

        bar = _make_bar(percent)

        print(
            f"{index}. {item['course_name']}"
        )

        print(
            f"[{bar}] "
            f"{item['priority_score']} 分"
        )

        print(
            f"预计复习："
            f"{item['estimate_review_hour']} 小时"
        )

        print("-" * 60)


if __name__ == "__main__":

    test_progress = {
        "target_query_date": "2026-10-20",
        "current_week": 8,
        "semester_remain_days": 70,
        "remain_weekend_count": 20,
        "course_list": [
            {
                "course_name": "高等数学",
                "finished": 8,
                "remain": 7,
                "total_classes": 15,
                "percent": 53.3
            },
            {
                "course_name": "Python",
                "finished": 5,
                "remain": 6,
                "total_classes": 11,
                "percent": 45.5
            }
        ]
    }

    test_recommend = [
        {
            "course_name": "高等数学",
            "priority_score": 93.5,
            "estimate_review_hour": 8.4
        },
        {
            "course_name": "Python",
            "priority_score": 74.1,
            "estimate_review_hour": 7.2
        }
    ]

    draw_course_progress_bar(test_progress)

    draw_recommend_rank_bar(test_recommend)