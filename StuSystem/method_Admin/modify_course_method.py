def process_courseModify(request, cursor, db):
    insert_result = ""
    results = []

    if request.method == 'POST':
        stu_id = request.form.get("stu_id", "")
        stu_course1 = request.form.get("stu_course1", "")
        stu_course2 = request.form.get("stu_course2", "")
        stu_course3 = request.form.get("stu_course3", "")


        # 输出日志，检查参数是否正确
        print(f"Student ID: {stu_id}, Course Name: {stu_course1}, Test Score: {stu_course2}, Usual Score: {stu_course3},")

        try:
            # 更新学生成绩表中对应学生和课程的成绩信息
            sql_update = """
                        UPDATE students_courses
                        SET stu_course1 = %s, stu_course2 = %s, stu_course3 = %s
                        WHERE stu_id = %s 
                        """
            cursor.execute(sql_update, (stu_course1, stu_course2, stu_course3, stu_id))

            # 提交数据库事务
            db.commit()

            # 查询更新后的结果
            sql_query = """
                        SELECT si.stu_id, si.stu_name, si.stu_gender, si.stu_grade, si.stu_school, si.stu_specialtyWithClass,
                                ss.stu_course1, ss.stu_course2, ss.stu_course3
                        FROM students_infos si
                        JOIN students_courses ss ON si.stu_id = ss.stu_id
                        WHERE si.stu_id = %s 
                        """

            cursor.execute(sql_query, stu_id)
            results = cursor.fetchall()

            insert_result = "数据修改成功！"

        except Exception as e:
            print("Error while updating data:", e)
            insert_result = "数据修改失败，请稍后重试！"
            # 发生错误时回滚事务
            db.rollback()

    return insert_result, results