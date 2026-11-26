#!/usr/bin/python
import MySQLdb


def get_all_users():
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="john",         # your username
                         passwd="megajonhy",  # your password
                         db="jonhydb")        # name of the data base

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()

    # Use all the SQL you like
    cur.execute("SELECT * FROM users")

    rows = cur.fetchall()

    db.close()
    return rows
