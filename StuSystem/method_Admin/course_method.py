# 学生选课信息管理

def process_course(request, cursor):

    query_conditions = []

    # 获取查询条件
    stu_id = request.values.get("stu_id", "")
    stu_name = request.values.get("stu_name", "")
    stu_gender = request.values.get("stu_gender", "")
    stu_grade = request.values.get("stu_grade", "")
    stu_school = request.values.get("stu_school", "")
    stu_specialtyWithClass = request.values.get("stu_specialtyWithClass", "")

    # 构造 SQL 查询语句
    sql = """
    SELECT 
        students_infos.stu_id, students_infos.stu_name, students_infos.stu_gender,
        students_infos.stu_grade, students_infos.stu_school, students_infos.stu_specialtyWithClass,
        students_courses.stu_course1, students_courses.stu_course2, students_courses.stu_course3
    FROM 
        students_infos
    LEFT JOIN 
        students_courses ON students_infos.stu_id = students_courses.stu_id
    WHERE 
        1=1
    """
    params = []

    if stu_id:
        sql += " AND students_infos.stu_id = %s"
        params.append(stu_id)
        query_conditions.append("学号：" + stu_id)
    if stu_name:
        sql += " AND students_infos.stu_name = %s"
        params.append(stu_name)
        query_conditions.append("姓名：" + stu_name)
    if stu_gender:
        sql += " AND students_infos.stu_gender = %s"
        params.append(stu_gender)
        query_conditions.append("性别：" + stu_gender)
    if stu_grade:
        sql += " AND students_infos.stu_grade = %s"
        params.append(stu_grade)
        query_conditions.append("年级：" + stu_grade)
    if stu_school:
        sql += " AND students_infos.stu_school = %s"
        params.append(stu_school)
        query_conditions.append("学院：" + stu_school)
    if stu_specialtyWithClass:
        sql += " AND students_infos.stu_specialtyWithClass = %s"
        params.append(stu_specialtyWithClass)
        query_conditions.append("专业班级：" + stu_specialtyWithClass)

    # 执行查询
    cursor.execute(sql, params)
    results = cursor.fetchall()

    return query_conditions, results
