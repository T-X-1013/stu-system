# 毕 业 学 生 去 向 查 看
from collections import Counter

def process_graduation(request, cursor):
    query_conditions = []

    # 获取查询条件
    stu_id = request.values.get("stu_id", "")
    stu_name = request.values.get("stu_name", "")
    stu_gender = request.values.get("stu_gender", "")
    stu_age = request.values.get("stu_age", "")
    stu_grade = request.values.get("stu_grade", "")
    stu_school = request.values.get("stu_school", "")
    stu_specialtyWithClass = request.values.get("stu_specialtyWithClass", "")
    stu_hometown = request.values.get("stu_hometown", "")

    # 构造SQL查询语句
    sql = "SELECT s.*, g.stu_gradition FROM students_infos s RIGHT JOIN students_graditions g ON s.stu_id = g.stu_id WHERE 1=1"
    params = []

    if stu_id:
        sql += " AND s.stu_id = %s"
        params.append(stu_id)
        query_conditions.append("学号：" + stu_id)
    if stu_name:
        sql += " AND s.stu_name = %s"
        params.append(stu_name)
        query_conditions.append("姓名：" + stu_name)
    if stu_gender:
        sql += " AND s.stu_gender = %s"
        params.append(stu_gender)
        query_conditions.append("性别：" + stu_gender)
    if stu_age:
        sql += " AND s.stu_age = %s"
        params.append(stu_age)
        query_conditions.append("年龄：" + stu_age)
    if stu_grade:
        sql += " AND s.stu_grade = %s"
        params.append(stu_grade)
        query_conditions.append("年级：" + stu_grade)
    if stu_school:
        sql += " AND s.stu_school = %s"
        params.append(stu_school)
        query_conditions.append("学院：" + stu_school)
    if stu_specialtyWithClass:
        sql += " AND s.stu_specialtyWithClass = %s"
        params.append(stu_specialtyWithClass)
        query_conditions.append("专业班级：" + stu_specialtyWithClass)
    if stu_hometown:
        sql += " AND s.stu_hometown = %s"
        params.append(stu_hometown)
        query_conditions.append("籍贯：" + stu_hometown)

    # 执行查询
    cursor.execute(sql, params)
    results = cursor.fetchall()


    # 计算毕业去向的统计数据
    last_elements = [sub_tuple[-1] for sub_tuple in results if sub_tuple]
    graduation_counts = Counter(last_elements)

    # 不再打印，而是返回统计信息
    return query_conditions, results, dict(graduation_counts)