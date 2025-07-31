def process_teacher(request, cursor):

    query_conditions = []

    # 获取查询条件
    ter_id = request.values.get("ter_id", "")
    ter_name = request.values.get("ter_name", "")
    ter_gender = request.values.get("ter_gender", "")
    ter_school = request.values.get("ter_school", "")
    ter_title = request.values.get("ter_title", "")
    ter_class1 = request.values.get("ter_class1", "")
    ter_class2 = request.values.get("ter_class2", "")
    ter_class3 = request.values.get("ter_class3", "")

    # 构造SQL查询语句
    sql = "SELECT ti.*, " \
          "(SELECT course_info FROM courses_infos WHERE course_name = ti.ter_class1 LIMIT 1) AS class1_info, " \
          "(SELECT course_info FROM courses_infos WHERE course_name = ti.ter_class2 LIMIT 1) AS class2_info, " \
          "(SELECT course_info FROM courses_infos WHERE course_name = ti.ter_class3 LIMIT 1) AS class3_info " \
          "FROM teachers_infos ti WHERE 1=1"
    params = []

    if ter_id:
        sql += " AND ter_id = %s"
        params.append(ter_id)
        query_conditions.append("工号：" + ter_id)
    if ter_name:
        sql += " AND ter_name = %s"
        params.append(ter_name)
        query_conditions.append("姓名：" + ter_name)
    if ter_gender:
        sql += " AND ter_gender = %s"
        params.append(ter_gender)
        query_conditions.append("性别：" + ter_gender)
    if ter_school:
        sql += " AND ter_school = %s"
        params.append(ter_school)
        query_conditions.append("学院：" + ter_school)
    if ter_title:
        sql += " AND ter_title = %s"
        params.append(ter_title)
        query_conditions.append("职称：" + ter_title)
    if ter_class1:
        sql += " AND ter_class1 = %s"
        params.append(ter_class1)
        query_conditions.append("学院：" + ter_class1)
    if ter_class2:
        sql += " AND ter_class2 = %s"
        params.append(ter_class2)
        query_conditions.append("学院：" + ter_class2)
    if ter_class3:
        sql += " AND ter_class3 = %s"
        params.append(ter_class3)
        query_conditions.append("学院：" + ter_class3)

    # 执行查询
    cursor.execute(sql, params)
    results = cursor.fetchall()

    return query_conditions, results