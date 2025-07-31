# 学 生 成 绩 查 询

def process_score(request, cursor):
    query_conditions = []

    # 获取查询条件
    stu_id = request.values.get("stu_id", "")
    stu_grade = request.values.get("stu_grade", "")
    stu_name = request.values.get("stu_name", "")
    stu_gender = request.values.get("stu_gender", "")
    stu_school = request.values.get("stu_school", "")
    stu_specialtyWithClass = request.values.get("stu_specialtyWithClass", "")
    course_name = request.values.get("course_name", "")
    test_course = request.values.get("test_course", "")
    usual_course = request.values.get("usual_course", "")
    final_course = request.values.get("final_course", "")


    # 构造SQL查询语句
    sql = """
    SELECT 
        si.stu_id, 
        si.stu_grade, 
        si.stu_name, 
        si.stu_gender, 
        si.stu_school, 
        si.stu_specialtyWithClass, 
        cs.course_name, 
        ss.test_score, 
        ss.usual_score, 
        ss.final_score, 
        ti.ter_name
    FROM 
        students_infos si
    LEFT JOIN 
        students_scores ss ON si.stu_id = ss.stu_id
    LEFT JOIN 
        courses_infos cs ON ss.course_id = cs.course_id
    LEFT JOIN 
        teachers_infos ti ON ss.ter_id = ti.ter_id
    WHERE 
        1=1
    """
    params = []

    if stu_id:
        sql += " AND si.stu_id = %s"
        params.append(stu_id)
        query_conditions.append("学号：" + stu_id)
    if stu_grade:
        sql += " AND si.stu_grade = %s"
        params.append(stu_grade)
        query_conditions.append("年级：" + stu_grade)
    if stu_name:
        sql += " AND si.stu_name = %s"
        params.append(stu_name)
        query_conditions.append("姓名：" + stu_name)
    if stu_gender:
        sql += " AND si.stu_gender = %s"
        params.append(stu_gender)
        query_conditions.append("性别：" + stu_gender)
    if stu_school:
        sql += " AND si.stu_school = %s"
        params.append(stu_school)
        query_conditions.append("学院：" + stu_school)
    if stu_specialtyWithClass:
        sql += " AND si.stu_specialtyWithClass = %s"
        params.append(stu_specialtyWithClass)
        query_conditions.append("专业班级：" + stu_specialtyWithClass)
    if course_name:  # 添加课程名称条件
        sql += " AND cs.course_name = %s"
        params.append(course_name)
        query_conditions.append("课程名称：" + course_name)
    if test_course:  # 添加课程名称条件
        sql += " AND ss.test_course = %s"
        params.append(test_course)
        query_conditions.append("课程名称：" + test_course)
    if usual_course:  # 添加课程名称条件
        sql += " AND ss.usual_course = %s"
        params.append(usual_course)
        query_conditions.append("课程名称：" + usual_course)
    if final_course:  # 添加课程名称条件
        sql += " AND ss.final_course = %s"
        params.append(final_course)
        query_conditions.append("课程名称：" + final_course)

    # 执行查询
    cursor.execute(sql, params)
    results = cursor.fetchall()




    return query_conditions, results