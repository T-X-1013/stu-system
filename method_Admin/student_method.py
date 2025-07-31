def process_studentAdd(request, cursor):
    insert_result = ""
    inserted_data = {}  # 存储插入的学生信息

    if request.method == 'GET':
        sql_list = "select * from students_infos"
        cursor.execute(sql_list)
        results = cursor.fetchall()

    if request.method == 'POST':
        stu_id = request.values.get("stu_id", "")
        stu_name = request.values.get("stu_name", "")
        stu_gender = request.values.get("stu_gender", "")
        stu_age = request.values.get("stu_age", "")
        stu_grade = request.values.get("stu_grade", "")
        stu_school = request.values.get("stu_school", "")
        stu_specialtyWithClass = request.values.get("stu_specialtyWithClass", "")
        stu_birthday = request.values.get("stu_birthday", "")
        stu_hometown = request.values.get("stu_hometown", "")

        if not all([stu_id, stu_name, stu_gender, stu_age, stu_grade, stu_school, stu_specialtyWithClass, stu_birthday, stu_hometown]):
            insert_result = "输入的学生信息不能为空"
        else:
            try:
                sql = "create table if not exists students_infos(stu_id varchar(12) primary key, stu_name varchar(50), stu_gender varchar(4), student_age int(2), stu_grade varchar(4), stu_school varchar(50), stu_specialtyWithClass varchar(50), stu_birthday varchar(8), stu_hometown varchar(50));"
                cursor.execute(sql)
                sql_1 = "insert into students_infos(stu_id, stu_name, stu_gender, stu_age, stu_grade, stu_school, stu_specialtyWithClass, stu_birthday, stu_hometown) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql_1, (stu_id, stu_name, stu_gender, stu_age, stu_grade, stu_school, stu_specialtyWithClass, stu_birthday, stu_hometown))
                insert_result = "成功存入一条学生信息"

                # 构造插入的学生信息字典
                inserted_data = {
                    "stu_id": stu_id,
                    "stu_name": stu_name,
                    "stu_gender": stu_gender,
                    "stu_age": stu_age,
                    "stu_grade": stu_grade,
                    "stu_school": stu_school,
                    "stu_specialtyWithClass": stu_specialtyWithClass,
                    "stu_birthday": stu_birthday,
                    "stu_hometown": stu_hometown
                }
            except Exception as err:
                print(err)
                insert_result = "学生信息插入失败"

            cursor.connection.commit()

        sql_list = "select * from students_infos"
        cursor.execute(sql_list)
        results = cursor.fetchall()

    return insert_result, results, inserted_data