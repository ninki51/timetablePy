#!/usr/bin/python3
import pymysql


class DB:
    tbName = ''

    def __init__(self, tbName):
        self.tbName = tbName

    def getConn(self):
        db = pymysql.connect("localhost", "root", "chenjian", "timetable")
        return db

    def addCell2DB(self, classID, Num, teacherID, subjectID, move):
        # 打开数据库连接
        db = self.getConn()

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 插入语句
        sql = "INSERT INTO cell(name, \
                 classID, Num, teacherID, subjectID,move) \
                 VALUES ('%s', %d, %d, %d, %d, %d)" % (self.tbName, classID, Num, teacherID, subjectID, move)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()

        # 关闭数据库连接
        db.close()

    # 基础信息
    def addBase2DB(self, row):
        # 打开数据库连接
        db = self.getConn()

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 插入语句
        sql = "INSERT INTO base (name, Mon, Tues, Wed, Thur,Fri,Sat,Sun) \
                 VALUES ('%s', %d,%d,%d,%d,%d,%d,%d)" % (
            self.tbName, row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()

        # 关闭数据库连接
        db.close()

    # 场地
    def addPlace2DB(self, place, subjectID, cap):
        # 打开数据库连接
        db = self.getConn()

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 插入语句
        sql = "INSERT INTO place (name, place, subjectID, cap) \
                     VALUES ('%s','%s',%d,%d)" % (self.tbName, place, subjectID, cap)
        # print(sql)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()

        # 关闭数据库连接
        db.close()

    # 班级约束:wid=星期ID，num=第几节,cid=班级ID
    def addClassCond2DB(self, wid, num, cid):
        # 打开数据库连接
        db = self.getConn()

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 插入语句
        sql = "INSERT INTO classCond (name, weekid, rowid, classid) \
                             VALUES ('%s',%d,%d,%d)" % (self.tbName, wid, num, cid)
        # print(sql)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()

        # 关闭数据库连接
        db.close()

    # 班级约束:wid=星期ID，num=第几节,tid=教师ID
    def addTeacherCond2DB(self, wid, num, tid):
        # 打开数据库连接
        db = self.getConn()

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 插入语句
        sql = "INSERT INTO teacherCond (name, weekid, rowid, teacherID) \
                                 VALUES ('%s',%d,%d,%d)" % (self.tbName, wid, num, tid)
        # print(sql)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()

        # 关闭数据库连接
        db.close()

