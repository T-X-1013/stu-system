# # 定义要清空数据的表名
# table_name = "students_infos"
#
# # 构建 SQL 清空表数据的语句
# sql_delete = f"DELETE FROM {table_name}"
#
# try:
#     # 执行清空表数据的操作
#     cursor.execute(sql_delete)
#
#     # 提交事务
#     connection.commit()
#     print(f"{table_name}表数据清空成功！")
# except Exception as e:
#     # 发生错误时回滚
#     connection.rollback()
#     print(f"{table_name}表数据清空失败:", e)
#
# # 关闭游标和数据库连接
# cursor.close()
# connection.close()
