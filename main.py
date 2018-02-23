#!/usr/bin/python3
import time
import random
import myDB
import csv1 as gl

db = myDB.DB("test13")

# 教师列表（无重复）
teacher_list = []


# 判断是否是固定课程
def isFixed(subject):
    for row in gl.base:
        for col in row:
            if subject == col:
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
    cls_arr = []
    for row in gl.arr:
        cls_arr.append(row[0])
    return cls_arr


# 授课安排表
def getCell():
    # 班级列表
    cls_arr = getClassArr()
    # 总课时
    total_nums = len(gl.week_arr) * len(gl.base)
    print("总课时=", total_nums)
    # 以班级为单位，创建cell(no,subject,teacher)
    cell = []
    i = 0
    for row in gl.arr:
        k = cls_arr[i]
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
        # 课程序号
        sno = 0
        for nums in subject_nums_arr:
            teacher = tea[j]
            # 判断是否是固定课程
            subject = gl.subject[j]

            for x in range(nums):
                ts.append([sno, teacher, subject])
                db.addCell2DB(i, sno, getTeacherID(teacher), j)
                sno += 1

            j += 1
        # 补齐空白时间块
        for aa in range(total_nums - sno):
            ts.append([sno, 999, 999])
            db.addCell2DB(i, sno, 999, 999)
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
def getClassID(c,c_arr):
    idx = 0
    for name in c_arr:
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

#班级约束
def classCond2db(c_arr):
    for c in gl.class_cond:
        wid = getWeekID(c[0])
        rowid = c[1]
        cid = getClassID(c[2],c_arr)
        db.addClassCond2DB(wid, rowid, cid)
#教师约束
def teacherCond2db():
    for t in gl.teacher_cond:
        wid = getWeekID(t[0])
        rowid = t[1]
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
def moveFixed():
    row_id = 0
    for row in gl.base:
        col_id = 0
        for col in row:
            if col != '有课' and col != '无课':
                subject_id = getSubjectID(col)
                sno = row_id * len(gl.week_arr) + col_id
                print(col, '.序号:', sno, '.id:', subject_id)
            col_id += 1
        row_id += 1


def main():
    start = time.clock()
    # 基础信息
    base2db()
    # 授课安排
    cell = getCell()
    print(cell)

    class_arr = getClassArr()
    print(class_arr)
    # 班级约束
    classCond2db(class_arr)
    # 教师约束
    teacherCond2db()
    print(teacher_list)
    end = time.clock()
    # print(random.randint(0, 100))
    # timeChongtu(cell)
    print("用时：%.05f 秒" % (end - start))


main()
