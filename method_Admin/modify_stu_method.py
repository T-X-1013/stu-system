def process_studentModify(request, cursor, db):
    insert_result = ""
    results = []

    if request.method == 'POST':
        stu_id = request.form.get("stu_id", "")
        stu_name = request.form.get("stu_name", "")
        stu_gender = request.form.get("stu_gender", "")
        stu_age = request.form.get("stu_age", "")
        stu_grade = request.form.get("stu_grade", "")
        stu_school = request.form.get("stu_school", "")
        stu_specialtyWithClass = request.form.get("stu_specialtyWithClass", "")
        stu_birthday = request.form.get("stu_birthday", "")
        stu_hometown = request.form.get("stu_hometown", "")


        # 连接数据库
        try:
            # 假设你的数据库连接已经在 server.py 中建立，传递过来了 cursor 和 conn
            # 更新数据库中对应学生的信息
            sql_update = """UPDATE students_infos SET stu_name=%s, stu_gender=%s, stu_age=%s, stu_grade=%s,
                            stu_school=%s, stu_specialtyWithClass=%s, stu_birthday=%s, stu_hometown=%s 
                            WHERE stu_id=%s"""
            cursor.execute(sql_update, (stu_name, stu_gender, stu_age, stu_grade, stu_school,
                                        stu_specialtyWithClass, stu_birthday, stu_hometown, stu_id))

            # 提交数据库事务
            db.commit()

            # 查询更新后的结果
            sql_query = "SELECT * FROM students_infos WHERE stu_id=%s"
            cursor.execute(sql_query, stu_id)
            results = cursor.fetchall()

            insert_result = "数据修改成功！"

        except Exception as e:
            print("Error while updating data:", e)
            insert_result = "数据修改失败，请稍后重试！"
            # 发生错误时回滚事务
            db.rollback()

    return insert_result, results