def process_scoreModify(request, cursor, db):
    insert_result = ""
    results = []

    if request.method == 'POST':
        stu_id = request.form.get("stu_id", "")
        course_name = request.form.get("course_name", "")
        test_score = request.form.get("test_score", "")
        usual_score = request.form.get("usual_score", "")
        final_score = request.form.get("final_score", "")

        # 输出日志，检查参数是否正确
        print(f"Student ID: {stu_id}, Course Name: {course_name}, Test Score: {test_score}, Usual Score: {usual_score}, Final Score: {final_score}")

        try:
            # 更新学生成绩表中对应学生和课程的成绩信息
            sql_update = """
                        UPDATE students_scores 
                        SET test_score = %s, usual_score = %s, final_score = %s
                        WHERE stu_id = %s AND course_id = (
                            SELECT course_id FROM courses_infos WHERE course_name = %s
                        )
                        """
            cursor.execute(sql_update, (test_score, usual_score, final_score, stu_id, course_name))

            # 提交数据库事务
            db.commit()

            # 查询更新后的结果
            sql_query = """
                        SELECT si.stu_id, si.stu_grade, si.stu_name, si.stu_gender, 
                               si.stu_school, si.stu_specialtyWithClass, ci.course_name, 
                               ss.test_score, ss.usual_score, ss.final_score, ti.ter_name
                        FROM students_scores ss
                        JOIN courses_infos ci ON ss.course_id = ci.course_id
                        JOIN students_infos si ON ss.stu_id = si.stu_id
                        LEFT JOIN teachers_infos ti ON ss.ter_id = ti.ter_id
                        WHERE ss.stu_id = %s AND ci.course_name = %s
                        """




            cursor.execute(sql_query, (stu_id, course_name))
            results = cursor.fetchall()

            insert_result = "数据修改成功！"

        except Exception as e:
            print("Error while updating data:", e)
            insert_result = "数据修改失败，请稍后重试！"
            # 发生错误时回滚事务
            db.rollback()

    return insert_result, results