def process_stuUserScore(userId, cursor):
    query_conditions = []

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

    # 添加 userId 作为查询条件
    sql += " AND si.stu_id = %s"
    params.append(userId)
    query_conditions.append("学号：" + userId)

    # 执行查询
    cursor.execute(sql, params)
    results = cursor.fetchall()

    return query_conditions, results
