import flask

def process_stuUsercourse(cursor):
    # 获取当前登录用户的学号
    stu_id = flask.session.get("userId")

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
        students_infos.stu_id = %s
    """

    # 执行查询
    cursor.execute(sql, (stu_id,))
    query_results = cursor.fetchall()

    return query_results