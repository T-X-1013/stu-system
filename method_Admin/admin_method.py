# 系 统 管 理 员 变 动

import re


def process_admin(request, cursor, db):
    insert_result = ""
    results = []

    if request.method == 'GET':
        sql_list = "select * from admins"
        cursor.execute(sql_list)
        results = cursor.fetchall()

    if request.method == 'POST':
        admin_name = request.values.get("admin_name", "")
        admin_password = request.values.get("admin_password", "")

        admin_name_result = re.search(r"^[a-zA-Z]+$", admin_name)
        admin_password_result = re.search(r"^[a-zA-Z\d]+$", admin_password)

        if admin_name_result and admin_password_result:
            select = request.form.get('selected_one')
            if select == '增加管理员':
                try:
                    sql = "create table if not exists admins(id int primary key auto_increment,admin_name varchar(15),admin_password varchar(20));"
                    cursor.execute(sql)
                    sql_1 = "insert into admins(admin_name,admin_password)values(%s,%s)"
                    cursor.execute(sql_1, (admin_name, admin_password))
                    insert_result = "成功增加了一名管理员"
                except Exception as err:
                    insert_result = "增加管理员操作失败"
                db.commit()
            elif select == '修改管理员密码':
                try:
                    sql = "update admins set admin_password=%s where admin_name=%s;"
                    cursor.execute(sql, (admin_password, admin_name))
                    insert_result = "管理员" + admin_name + "的密码修改成功!"
                except Exception as err:
                    insert_result = "修改管理员密码失败!"
                db.commit()
            elif select == '删除管理员':
                try:
                    sql_delete = "delete from admins where admin_name='" + admin_name + "';"
                    cursor.execute(sql_delete)
                    insert_result = "成功删除管理员" + admin_name
                except Exception as err:
                    insert_result = "删除管理员失败"
                db.commit()
        else:
            insert_result = "输入的格式不符合要求!"

        sql_list = "select * from admins"
        cursor.execute(sql_list)
        results = cursor.fetchall()

    return insert_result, results