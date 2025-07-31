def process_stuUserInfo(session, cursor):

    query_conditions = []

    # 获取查询条件
    stu_id = session.get("userId")


    # 构造SQL查询语句
    sql = "SELECT * FROM students_infos WHERE stu_id = %s"
    params = (stu_id,)



    # 执行查询
    cursor.execute(sql, params)
    results = cursor.fetchall()


    print(params)

    print(results)

    return query_conditions, results