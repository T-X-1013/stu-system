import re
import flask


def process_stuUser(userId, cursor, db):
    insert_result = ""
    results = []

    if userId:
        # 如果 userId 存在，则查询该学生用户信息
        sql = "SELECT * FROM stu_users WHERE stu_id = %s"
        cursor.execute(sql, (userId,))
        results = cursor.fetchall()

    if flask.request.method == 'POST':
        admin_id = flask.request.values.get("admin_id", "")
        admin_password = flask.request.values.get("admin_password", "")

        admin_id_result = re.search(r"^\d+$", admin_id)
        admin_password_result = re.search(r"^[a-zA-Z\d]+$", admin_password)

        if admin_id_result and admin_password_result:
            try:
                sql = "UPDATE stu_users SET stu_pwd=%s WHERE stu_id=%s;"
                cursor.execute(sql, (admin_password, admin_id))
                db.commit()
                insert_result = "用户" + admin_id + "的密码修改成功!"
            except Exception as err:
                insert_result = "修改密码失败!"

            # 重新执行与当前用户相关的查询
            if userId:
                sql = "SELECT * FROM stu_users WHERE stu_id = %s"
                cursor.execute(sql, (userId,))
                results = cursor.fetchall()
        else:
            insert_result = "输入的格式不符合要求!"

    return insert_result, results