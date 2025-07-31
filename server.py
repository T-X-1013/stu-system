import re  # 引入正则表达式对用户输入进行限制
import flask
import pymysql  # 连接数据库


from method_Admin.admin_method import process_admin
from method_Admin.modify_course_method import process_courseModify
from method_Admin.student_method import process_studentAdd
from method_Admin.modify_stu_method import process_studentModify
from method_Admin.delete_stu_method import process_studentDelete
from method_Admin.graduation_method import process_graduation
from method_Admin.teacher_method import process_teacher
from method_Admin.score_method import process_score
from method_Admin.course_method import process_course
from method_Admin.view_stu_method import process_studentView
from method_Admin.modify_score_method import process_scoreModify
from method_Student.stuUser_course_method import process_stuUsercourse
from method_Student.stuUser_info_method import process_stuUserInfo
from method_Student.stuUser_method import process_stuUser
from method_Student.stuUser_score_method import process_stuUserScore

app = flask.Flask(__name__)


# 使用pymysql.connect方法连接本地mysql数据库
db = pymysql.connect(host='localhost', port=3306, user='root', password='root', database='stu_system', charset='utf8')
# 操作数据库，获取db下的cursor对象
cursor = db.cursor()


# 存储登陆用户的名字用户其它网页的显示
users = []

usersId = []

# 检查登录状态
def check_login():
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    insert_result = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''
    return insert_result, user_info


@app.route("/", methods=["GET", "POST"])
def login():
    # 增加会话保护机制(未登陆前login的session值为空)
    flask.session['login'] = ''
    if flask.request.method == 'POST':
        user = flask.request.values.get("user", "")
        pwd = flask.request.values.get("pwd", "")
        result_user = re.search(r"^[a-zA-Z]+$", user)  # 限制用户名为全字母
        result_pwd = re.search(r"^[a-zA-Z\d]+$", pwd)  # 限制密码为 字母和数字的组合
        if result_user != None and result_pwd != None:  # 验证通过
            msg = '用户名或密码错误'
            sql1 = "select * from admins where admin_name='" + \
                   user + " ' and admin_password='" + pwd + "';"
            cursor.execute(sql1)
            result = cursor.fetchone()
            # 匹配得到结果即管理员数据库中存在此管理员
            if result:
                # 登陆成功
                flask.session['login'] = 'OK'
                users.append(user)  # 存储登陆成功的用户名用于显示
                return flask.redirect(flask.url_for('student_view'))
                # return flask.redirect('/file')
        else:  # 输入验证不通过
            msg = '非法输入'
    else:
        msg = ''
        user = ''
    return flask.render_template('login.html', msg=msg, user=user)


@app.route('/student_view', methods=['GET', 'POST'])
def student_view():

    insert_result, user_info = check_login()

    if flask.request.method == 'GET':
        insert_result, user_info = check_login()
        return flask.render_template('student_view.html', insert_result=insert_result, user_info=user_info)

    # 执行查询方法，获取查询条件和结果
    query_conditions, query_results = process_studentView(flask.request, cursor)

    # 检查是否执行了查询并且结果为空
    no_results = not query_conditions and not query_results

    return flask.render_template('student_view.html', query_conditions=query_conditions, query_results=query_results,
                                 no_results=no_results, insert_result=insert_result, user_info=user_info)


@app.route('/student', methods=['GET', 'POST'])
def student():
    insert_result, user_info = check_login()

    insert_result, results, inserted_data = process_studentAdd(flask.request, cursor)
    print(insert_result)

    print(inserted_data)



    return flask.render_template('student.html', insert_result=insert_result, user_info=user_info, results=results,
                                 inserted_data=inserted_data)


@app.route('/update_student', methods=['GET', "POST"])
def update_student():

    insert_result, user_info = check_login()

    if flask.request.method == 'GET':
        insert_result, user_info = check_login()
        return flask.render_template('update_student.html', user_info=user_info, insert_result=insert_result)

    # 执行查询方法，获取查询条件和结果
    query_conditions, query_results = process_studentView(flask.request, cursor)

    # 检查是否执行了查询并且结果为空
    no_results = not query_conditions and not query_results

    return flask.render_template('update_student.html', query_conditions=query_conditions, query_results=query_results,
                                 no_results=no_results, user_info=user_info, insert_result=insert_result)


@app.route('/modify_student', methods=['GET', 'POST'])
def modify_student():
    if flask.request.method == 'GET':
        insert_result, user_info = check_login()
        # 执行查询方法，获取查询条件和结果
        query_conditions, query_results = process_studentView(flask.request, cursor)

        # 检查是否执行了查询并且结果为空
        no_results = not query_conditions and not query_results

        return flask.render_template('modify_student.html', query_conditions=query_conditions, query_results=query_results,
                                     no_results=no_results, user_info=user_info, insert_result=insert_result)
    elif flask.request.method == 'POST':
        insert_result, user_info = check_login()
        # 调用修改方法，获取修改结果
        insert_result, query_results = process_studentModify(flask.request, cursor, db)

        # 检查是否执行了修改并且结果为空
        no_results = not query_results

        return flask.render_template('modify_student.html', insert_result=insert_result, query_results=query_results,
                                     no_results=no_results, user_info=user_info)


@app.route('/delete_student', methods=['GET', 'POST'])
def delete_student():
    if flask.request.method == 'GET':
        insert_result, user_info = check_login()
        # 执行查询方法，获取查询条件和结果
        query_conditions, query_results = process_studentView(flask.request, cursor)

        # 检查是否执行了查询并且结果为空
        no_results = not query_conditions and not query_results

        return flask.render_template('delete_student.html', query_conditions=query_conditions, query_results=query_results,
                                 no_results=no_results, user_info=user_info, insert_result=insert_result)

    if flask.request.method == 'POST':
        insert_result, user_info = check_login()
        student_id = flask.request.form['stu_id']
        try:
            # 调用删除学生数据方法
            process_studentDelete(student_id, cursor, db)
            # 成功删除后重定向到 update_student.html 页面
            return flask.redirect('update_student')
        except Exception as e:
            # 处理删除过程中的异常
            return flask.render_template('error.html', message="删除学生数据时出现错误：" + str(e), user_info=user_info, insert_result=insert_result)


@app.route('/teacher_class', methods=['GET', 'POST'])
def teacher_class():

    insert_result, user_info = check_login()

    if flask.request.method == 'GET':
        insert_result, user_info = check_login()
        return flask.render_template('teacher_class.html', user_info=user_info, insert_result=insert_result)

    # 执行查询方法，获取查询条件和结果
    query_conditions, query_results = process_teacher(flask.request, cursor)

    # 检查是否执行了查询并且结果为空
    no_results = not query_conditions and not query_results

    return flask.render_template('teacher_class.html', query_conditions=query_conditions, query_results=query_results,
                                 no_results=no_results, user_info=user_info, insert_result=insert_result)


@app.route('/student_courses', methods=['GET', "POST"])
def student_courses():

    insert_result, user_info = check_login()

    if flask.request.method == 'GET':
        insert_result, user_info = check_login()
        return flask.render_template('student_courses.html', user_info=user_info, insert_result=insert_result)

    # 执行查询方法，获取查询条件和结果
    query_conditions, query_results = process_course(flask.request, cursor)

    # 检查是否执行了查询并且结果为空
    no_results = not query_conditions and not query_results

    return flask.render_template('student_courses.html', query_conditions=query_conditions, query_results=query_results,
                                 no_results=no_results, user_info=user_info, insert_result=insert_result)


@app.route('/modify_course', methods=['GET', 'POST'])
def modify_course():
    if flask.request.method == 'GET':
        insert_result, user_info = check_login()
        # 执行查询方法，获取查询条件和结果
        query_conditions, query_results = process_course(flask.request, cursor)

        # 检查是否执行了查询并且结果为空
        no_results = not query_conditions and not query_results

        return flask.render_template('modify_course.html', query_conditions=query_conditions, query_results=query_results,
                                     no_results=no_results, user_info=user_info, insert_result=insert_result)
    elif flask.request.method == 'POST':
        insert_result, user_info = check_login()
        # 调用修改方法，获取修改结果
        insert_result, query_results = process_courseModify(flask.request, cursor, db)

        # 检查是否执行了修改并且结果为空
        no_results = not query_results

        return flask.render_template('modify_course.html', insert_result=insert_result, query_results=query_results,
                                     no_results=no_results, user_info=user_info)


@app.route('/score_infos', methods=['GET', 'POST'])
def score_infos():
    insert_result, user_info = check_login()

    query_conditions, results = process_score(flask.request, cursor)
    return flask.render_template('score_infos.html', user_info=user_info, query_conditions=query_conditions, results=results)


@app.route('/modify_score', methods=['GET', 'POST'])
def modify_score():
    if flask.request.method == 'GET':
        insert_result, user_info = check_login()
        # 执行查询方法，获取查询条件和结果
        query_conditions, query_results = process_score(flask.request, cursor)

        # 检查是否执行了查询并且结果为空
        no_results = not query_conditions and not query_results

        return flask.render_template('modify_score.html', query_conditions=query_conditions, query_results=query_results,
                                     no_results=no_results, user_info=user_info, insert_result=insert_result)
    elif flask.request.method == 'POST':
        insert_result, user_info = check_login()
        # 调用修改方法，获取修改结果
        insert_result, query_results = process_scoreModify(flask.request, cursor, db)

        # 检查是否执行了修改并且结果为空
        no_results = not query_results

        return flask.render_template('modify_score.html', insert_result=insert_result, query_results=query_results,
                                     no_results=no_results, user_info=user_info)


# 毕业学生去向界面的接口
@app.route('/graduation', methods=['GET', 'POST'])
def graduation():

    insert_result, user_info = check_login()

    if flask.request.method == 'GET':
        insert_result, user_info = check_login()
        return flask.render_template('graduation.html', user_info=user_info, insert_result=insert_result)

    # 执行查询方法，获取查询条件和结果
    query_conditions, query_results, graduation_counts = process_graduation(flask.request, cursor)

    graduation_stats = list(graduation_counts.items())

    # 检查是否执行了查询并且结果为空
    no_results = not query_conditions and not query_results

    return flask.render_template('graduation.html', query_conditions=query_conditions, query_results=query_results,
                                 no_results=no_results, graduation_stats=graduation_stats, user_info=user_info, insert_result=insert_result)

@app.route('/dataAnalysis', methods=['GET', "POST"])
def dataAnalysis():
    insert_result, user_info = check_login()


    return flask.render_template('dataAnalysis.html', user_info=user_info, insert_result=insert_result)


@app.route('/adminstator', methods=['GET', "POST"])
def adminstator():
    insert_result, user_info = check_login()

    insert_result, results = process_admin(flask.request, cursor, db)
    return flask.render_template('adminstator.html', user_info=user_info, insert_result=insert_result, results=results)


# 学 生
@app.route("/studentLogin", methods=["GET", "POST"])
def student_login():
    # 增加会话保护机制(未登陆前login的session值为空)
    flask.session['login'] = ''
    if flask.request.method == 'POST':
        user = flask.request.values.get("user", "")
        pwd = flask.request.values.get("pwd", "")
        result_user = re.search(r"^\d+$", user)
        result_pwd = re.search(r"^[a-zA-Z\d]+$", pwd)  # 限制密码为 字母和数字的组合
        if result_user != None and result_pwd != None:  # 验证通过
            msg = '用户名或密码错误'
            sql1 = "SELECT * FROM stu_users WHERE stu_id=%s AND stu_pwd=%s;"
            cursor.execute(sql1, (user, pwd))
            result = cursor.fetchone()
            # 匹配得到结果即管理员数据库中存在此管理员
            if result:
                # 登陆成功
                flask.session['login'] = 'OK'
                users.append(result[1])  # 存储登陆成功的用户姓名
                flask.session['userId'] = result[0]
                return flask.redirect(flask.url_for('stu_baseInfo'))
        else:  # 输入验证不通过
            msg = '非法输入'
    else:
        msg = ''
        user = ''
    return flask.render_template('studentLogin.html', msg=msg, user=user)


@app.route('/stu_baseInfo', methods=['GET', "POST"])
def stu_baseInfo():
    insert_result, user_info = check_login()

    if flask.request.method == 'GET':
        insert_result, user_info = check_login()
        print(user_info)
        return flask.render_template('stu_baseInfo.html', insert_result=insert_result, user_info=user_info)

    # 执行查询方法，获取查询条件和结果
    query_conditions, query_results = process_stuUserInfo(flask.session, cursor)

    # 检查是否执行了查询并且结果为空
    no_results = not query_conditions and not query_results

    return flask.render_template('stu_baseInfo.html', query_conditions=query_conditions,
                                 query_results=query_results,
                                 no_results=no_results, insert_result=insert_result, user_info=user_info)


@app.route('/stu_courses', methods=['GET', "POST"])
def stu_courses():

    insert_result, user_info = check_login()

    if flask.request.method == 'GET':
        insert_result, user_info = check_login()
        return flask.render_template('stu_courses.html', user_info=user_info, insert_result=insert_result)

    # 执行查询方法，获取查询条件和结果
    query_results = process_stuUsercourse(cursor)

    # 检查是否执行了查询并且结果为空
    no_results = not query_results

    return flask.render_template('stu_courses.html', query_results=query_results,
                                 no_results=no_results, user_info=user_info, insert_result=insert_result)


@app.route('/stu_modify_course', methods=['GET', 'POST'])
def stu_modify_course():
    if flask.request.method == 'GET':
        insert_result, user_info = check_login()
        # 执行查询方法，获取查询条件和结果
        query_conditions, query_results = process_course(flask.request, cursor)

        # 检查是否执行了查询并且结果为空
        no_results = not query_conditions and not query_results

        return flask.render_template('stu_modify_course.html', query_conditions=query_conditions, query_results=query_results,
                                     no_results=no_results, user_info=user_info, insert_result=insert_result)
    elif flask.request.method == 'POST':
        insert_result, user_info = check_login()
        # 调用修改方法，获取修改结果
        insert_result, query_results = process_courseModify(flask.request, cursor, db)

        # 检查是否执行了修改并且结果为空
        no_results = not query_results

        return flask.render_template('stu_modify_course.html', insert_result=insert_result, query_results=query_results,
                                     no_results=no_results, user_info=user_info)


@app.route('/stu_score', methods=['GET', 'POST'])
def stu_score():

    if flask.request.method == 'GET':
        insert_result, user_info = check_login()
        return flask.render_template('stu_score.html', user_info=user_info, insert_result=insert_result)

    elif flask.request.method == 'POST':
        insert_result, user_info = check_login()

        # 获取当前登录用户的 userId
        userId = flask.session.get('userId')

        # 执行查询方法，获取查询条件和结果
        query_conditions, results = process_stuUserScore(userId, cursor)
        return flask.render_template('stu_score.html', user_info=user_info, query_conditions=query_conditions, results=results)



@app.route('/stu_terCourse', methods=['GET', "POST"])
def stu_terCourse():

    insert_result, user_info = check_login()

    if flask.request.method == 'GET':
        insert_result, user_info = check_login()
        return flask.render_template('stu_terCourse.html', user_info=user_info, insert_result=insert_result)

    # 执行查询方法，获取查询条件和结果
    query_conditions, query_results = process_teacher(flask.request, cursor)

    # 检查是否执行了查询并且结果为空
    no_results = not query_conditions and not query_results

    return flask.render_template('stu_terCourse.html', query_conditions=query_conditions, query_results=query_results,
                                 no_results=no_results, user_info=user_info, insert_result=insert_result)


@app.route('/stu_Users', methods=['GET', "POST"])
def stuUsers():
    insert_result, user_info = check_login()

    # 根据当前登录用户的 userId 查询相应的学生用户信息
    insert_result, results = process_stuUser(flask.session.get('userId'), cursor, db)
    return flask.render_template('stu_Users.html', user_info=user_info, insert_result=insert_result, results=results)

# 启动服务器
app.debug = True
# 增加session会话保护(任意字符串,用来对session进行加密)
app.secret_key = 'carson'
try:
    app.run()
except Exception as err:
    print(err)
    db.close()  # 关闭数据库连接
