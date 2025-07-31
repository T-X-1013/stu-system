import random
import pymysql  # 导入数据库连接库，这里以 MySQL 为例


# 建立数据库连接
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='root',
                             database='stu_system',
                             charset='utf8')

# 创建游标对象
cursor = connection.cursor()
# 教师信息列表
teachers_info = []

# 姓名列表
names = ['赵宏', '梁雪峰', '刘先河', '刘晓涛', '包敏', '杨伟涛', '毛国强', '胡国锋', '蔡明京', '李祥东', '胥军', '张苇杭', '计钟', '张洁', '王勇超', '宋晓丹',
         '任效江', '游淑珍', '陈睿', '石光明', '沈中', '曹琦', '裴庆祺', '刘雷', '何鑫', '李红宁', '刘静', '黄婷', '高大化', '沈八中', '张大兴', '刘于金', '李晓辉',
         '侯松岩', '刘佳宜', '牛冠冲', '谢雪梅', '邢伟川', '王从思', '刘志宏', '白宝明']

# 工号集合
teacher_ids = set()

# 性别列表
genders = ['男', '女']

# 学院列表
schools = ['计算机与信息工程学院'] * 6 + ['金融学院'] * 4

# 职称列表
titles = ['教授'] * 3 + ['副教授'] * 4 + ['讲师'] * 2 + ['助教']

# 计算机与信息工程学院课程列表
computer_courses = ['计算机组成原理', '操作系统', '数据结构与算法', '数据库系统原理', '计算机网络', '编译原理', '软件工程导论', '人工智能与机器学习', '数据科学导论',
                    '数据挖掘与分析', '大数据处理技术', '机器学习与深度学习', '数据可视化', '分布式计算与云计算', '数据库原理与应用', '统计数据分析', '信号与系统', '通信原理',
                    '数字电路与逻辑设计', '微机原理与接口技术', '电磁场与电磁波', '电子测量技术', '嵌入式系统', '信息论基础', '电子商务概论', '网络营销', '电子商务物流',
                    '电子商务法律', '电子商务数据分析', '电子商务系统设计与开发', '跨境电子商务', '电子商务运营管理', '面向对象程序设计', '软件需求工程', '软件设计模式', '软件测试技术',
                    '软件项目管理', '软件体系结构', '软件开发工具与环境', '密码学基础', '网络安全协议', '防火墙与入侵检测技术', '网络安全管理与策略', '网络安全法律与伦理',
                    '网络攻击与防御', '云计算与大数据安全']

# 金融学院课程列表
finance_courses = ['投资学原理', '证券投资分析', '投资组合管理', '衍生金融工具与风险管理', '房地产投资与管理', '行为金融与投资心理', '保险学原理', '保险精算与风险管理', '保险市场与营销',
                   '保险公司经营管理', '社会保险与员工福利', '保险法规与监管', '金融工程导论', '金融计量经济学', '固定收益证券分析', '金融衍生品定价', '金融风险管理', '金融算法与编程',
                   '金融学基础', '货币银行学', '国际金融', '公司金融', '金融市场与机构', '商业银行经营与管理']

# 创建老师信息
for _ in range(40):
    # 随机生成工号
    while True:
        teacher_id = '11' + str(random.randint(100, 999))
        if teacher_id not in teacher_ids:
            teacher_ids.add(teacher_id)
            break

    # 随机选择姓名
    name = random.choice(names)
    names.remove(name)  # 从列表中删除已选姓名

    # 随机选择性别
    gender = random.choice(genders)

    # 随机选择学院
    school = random.choice(schools)

    # 随机选择职称
    title = random.choice(titles)

    # 随机选择课程
    if school == '计算机与信息工程学院':
        classes = random.sample(computer_courses, random.randint(1, 3))
    else:
        classes = random.sample(finance_courses, random.randint(1, 3))

    # 将课程填充到对应的字段
    class1, class2, class3 = (classes + [None] * 3)[:3]

    # 添加老师信息到列表
    teachers_info.append({
        'ter_id': teacher_id,
        'ter_name': name,
        'ter_gender': gender,
        'ter_school': school,
        'ter_title': title,
        'ter_class1': class1,
        'ter_class2': class2,
        'ter_class3': class3
    })



# 构建 SQL 插入语句
sql_insert = "INSERT INTO " \
             "teachers_infos (ter_id, ter_name, ter_gender, ter_school, ter_title, ter_class1, ter_class2, ter_class3) " \
             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

# 执行插入操作
try:
    # 将字典中的值插入数据库
    for teacher in teachers_info:
        cursor.execute(sql_insert,
                       (teacher['ter_id'], teacher['ter_name'], teacher['ter_gender'],
                        teacher['ter_school'], teacher['ter_title'], teacher['ter_class1'],
                        teacher['ter_class2'], teacher['ter_class3'] ))

    # 提交事务
    connection.commit()
    print("数据插入成功！")
except Exception as e:
    # 发生错误时回滚
    connection.rollback()
    print("数据插入失败:", e)