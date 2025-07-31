# 删除学生数据的方法
def process_studentDelete(student_id, cursor, db):
    try:

        cursor.execute("DELETE FROM students_infos WHERE stu_id = %s", (student_id,))
        db.commit()

        # 用你实际的删除数据的代码替换这个注释

        print(f"已删除学生 ID 为：{student_id}")

    except Exception as e:
        # 处理删除过程中发生的任何异常
        raise e