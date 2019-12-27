# -*- coding: utf-8 -*-

import sqlite3


def create_db():
    conn = sqlite3.connect('../gift-box.db')
    cur = conn.cursor()
    ## 创建一个表 - company
    conn.execute('''CREATE TABLE wish_list
           (id INTEGER PRIMARY KEY  AUTOINCREMENT   NOT NULL,
           gift_name           VARCHAR(64)    NOT NULL,
           note            TEXT);''')
    cur.close()


def test():
    data=(("aaa","bbb"),
          ("ccc","ddd"))
    sql = "INSERT INTO wish_list (gift_name,note)VALUES (?,?)"
    conn = sqlite3.connect('../gift-box.db')
    cur = conn.cursor()
    cur.executemany(sql,data)
    conn.commit()

if __name__ == '__main__':
    create_db()
    print "-----数据库创建完成-----"
    # test()
    # print "----测试插入完成----"