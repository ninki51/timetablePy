#!/usr/bin/python3
import time
import random
import myDB
import csv1 as gl

db = myDB.DB("test25")

# 教师列表（无重复）
teacher_list = []

# 班级列表
class_arr = []

# 固定课程
fixed_list = []

# 班级约束数组
class_cond_list = []


# 判断是否是固定课程
def isFixed(subject):
    for row in gl.base:
        for col in row:
            if subject == col:
                return True
    return False


def isFixed2(sno, subject):
    for row in fixed_list:
        if sno == row[0] and subject == row[1]:
            return True
    return False


def fotmatStr(str):
    if str == '':
        return ''
    str = str.strip()
    return str.replace(' ', '')


# 检查时间冲突
def timeChongtu(cell):
    for k in cell:
        for row in cell[str(k)]:
            print(row)


# 班级列表
def getClassArr():
    if len(class_arr) > 0:
        del class_arr[:]
    for row in gl.arr:
        class_arr.append(row[0])


# 授课安排表
def getCell():
    # 班级列表
    # 总课时
    total_nums = len(gl.week_arr) * len(gl.base)
    print("总课时=", total_nums)
    # 以班级为单位，创建cell(no,subject,teacher)
    cell = []
    i = 0
    for row in gl.arr:
        # 班级
        k = class_arr[i]
        if len(k) == 0:
            print("班级不能为空!")
            return
        # print(k)
        # teacher-subject
        ts = []
        tea = []
        subject_nums_arr = []
        j = 0
        for col in row[1:]:
            if j % 2 == 0:
                # 教师
                t = fotmatStr(col)
                tea.append(t)
                if col != '':
                    addTeacher(t)
            elif j % 2 == 1:
                # 课程
                if col != '':
                    subject_nums_arr.append(int(col))
                else:
                    subject_nums_arr.append(0)
            j += 1

        j = 0
        # print("教师：", tea)
        # print("课时数组:", subject_nums_arr)
        # 课程序号

        sno = 0
        for nums in subject_nums_arr:
            subject = gl.subject[j]
            # 注意：teacher有可能为空
            teacher = tea[j]
            # if teacher == "":
            #     j += 1

            for x in range(nums):
                ts.append([sno, teacher, subject])
                # db.addCell2DB(i, sno, getTeacherID(teacher), getSubjectID(subject))
                sno += 1

            j += 1
        # 补齐空白时间块
        for aa in range(total_nums - sno):
            ts.append([sno, 999, 999])
            # db.addCell2DB(i, sno, 999, 999)
            sno += 1
        dict = {k: ts}
        cell.append(dict)
        i += 1
    return cell


# 添加教师
def addTeacher(t):
    for name in teacher_list:
        if name == t:
            return
    teacher_list.append(t)


# 查找教师ID
def getTeacherID(t):
    idx = 0
    for name in teacher_list:
        if name == t:
            return idx
        idx += 1
    return -1


# 查找课程ID
def getSubjectID(s):
    idx = 0
    for name in gl.subject:
        if name == s:
            return idx
        idx += 1
    return -1


# 查找weekID
def getWeekID(w):
    idx = 0
    for name in gl.week_arr:
        if name == w:
            return idx
        idx += 1
    return -1


# 查找classID
def getClassID(c):
    idx = 0
    for name in class_arr:
        if name == c:
            return idx
        idx += 1
    return -1


# 场地
def place2db():
    for p in gl.place:
        place = p[0]
        suject = p[1]
        subjectID = getSubjectID(suject)
        cap = int(p[2])
        db.addPlace2DB(place, subjectID, cap)


# 班级约束
def classCond2db():
    for c in gl.class_cond:
        wid = getWeekID(c[0])
        rowid = c[1] - 1
        cid = getClassID(c[2])
        db.addClassCond2DB(wid, rowid, cid)
        sno = rowid * len(gl.base[0]) + wid
        class_cond_list.append([sno, cid])
    print("班级约束=", class_cond_list)


# 教师约束
def teacherCond2db():
    for t in gl.teacher_cond:
        wid = getWeekID(t[0])
        rowid = t[1] - 1
        tid = getTeacherID(t[2])
        db.addTeacherCond2DB(wid, rowid, tid)


# 基础信息写入数据库
def base2db():
    for r in gl.base:
        row = [-1, -1, -1, -1, -1, -1, -1]
        idx = 0
        for c in r:
            if c == '有课':
                row[idx] = 888
            elif c == '无课':
                row[idx] = 999
            elif len(c) >= 1:
                row[idx] = getSubjectID(c)
            idx += 1
        print(row)
        db.addBase2DB(row)


# 把固定课程移动到位
def moveFixed(cell):
    for dict in cell:
        for k in dict:
            # 每个班
            row = dict[k]
            # 要交换的ID
            sid0 = sid1 = -1
            for f in fixed_list:
                sid0 = f[0]
                fixedSubject = f[1]
                for col in row:
                    sno = col[0]
                    teacher = col[1]
                    subject = col[2]
                    if subject == fixedSubject:
                        sid1 = sno
                        break
                # 交换位置
                if sid0 > -1 and sid1 > -1:
                    row[sid0][1], row[sid1][1] = row[sid1][1], row[sid0][1]
                    row[sid0][2], row[sid1][2] = row[sid1][2], row[sid0][2]


# 移动空白位置
def moveBlank(cell):
    for dict in cell:
        for k in dict:
            # 每个班
            row = dict[k]
            # 要交换的ID
            sid0 = sid1 = -1
            for f in class_cond_list:
                sid0 = f[0]
                clsid = f[1]
                for col in row:
                    sno = col[0]
                    if col[1] == 999 and clsid == getClassID(k):
                        sid1 = sno
                        break
                # 交换位置
                if sid0 > -1 and sid1 > -1:
                    row[sid0][1], row[sid1][1] = row[sid1][1], row[sid0][1]
                    row[sid0][2], row[sid1][2] = row[sid1][2], row[sid0][2]
                    break


# 把固定课程放到fixed_list中
def addFixed():
    row_id = 0
    for row in gl.base:
        col_id = 0
        for col in row:
            if col != '有课' and col != '无课':
                subject_id = getSubjectID(col)
                sno = row_id * len(gl.week_arr) + col_id
                print(col, '.序号:', sno, '.id:', subject_id)
                fixed_list.append([sno, col])
            col_id += 1
        row_id += 1


def cell2db(cell):
    for dict in cell:
        for k in dict:
            # 每个班
            row = dict[k]
            clsid = getClassID(k)
            for col in row:
                sno = col[0]
                teacher = col[1]

                subject = col[2]

                move = 1
                if teacher == 999:
                    move = 0
                    teacher_id = 999
                else:
                    teacher_id = getTeacherID(teacher)
                if subject == 999:
                    subject_id = 999
                else:
                    subject_id = getSubjectID(subject)
                if isFixed2(sno, subject):
                    move = 0
                db.addCell2DB(clsid, sno, teacher_id, subject_id, move)


def main():
    start = time.clock()
    # 基础信息
    base2db()
    # 班级列表
    getClassArr()
    # print(class_arr)
    # 班级约束
    classCond2db()
    # 提取固定课程
    addFixed()
    print(fixed_list)

    # 授课安排
    cell = getCell()

    # 固定课程，摆正位置
    moveFixed(cell)
    moveBlank(cell)
    cell2db(cell)
    print(cell)

    # 教师约束
    teacherCond2db()
    print(teacher_list)
    end = time.clock()
    # print(random.randint(0, 100))
    # timeChongtu(cell)
    print("用时：%.05f 秒" % (end - start))


main()
