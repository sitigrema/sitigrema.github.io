#!/usr/bin/env python3

import sqlite3


class DBproto(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self._connect()

    def _connect(self):
        pass

    def query(self, q, *args):
        self.cur.execute(q,*args)

    def fetchall(self):
        return self.cur.fetchall()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()

    def __len__(self):
        return True

class DB(DBproto):
    def _connect(self):
        try:
            self.conn = sqlite3.connect("groups.s3db")
            self.cur = self.conn.cursor()
        except:
            raise (Exception, "Unable to connect database.")

    def sanit(self, instr):
        try:
            return str(instr).replace("''","'").replace("'","''").decode("utf-8")
        except:
            return instr.replace("''","'").replace("'","''")

    def lastid(self):
        r = self.cur.lastrowid
        return r



db = DB()
db.query("SELECT id_group, title, slug FROM groups")
res_groups = db.fetchall()

result = ""
for id_group, group_title, group_slug in res_groups:
    result += "- id    : {}\n".format(id_group)
    result += "  title : {}\n".format(group_title)
    result += "  slug  : {}\n".format(group_slug)

    db.query("SELECT id_subgroup, title, slug FROM subgroups WHERE parent = ?", [id_group])
    res_subgroups = db.fetchall()
    if res_subgroups:
        result += "  groups :\n"

    for id_subgroup, subgroup_title, subgroup_slug in res_subgroups:
        result += "    - id   : {}\n".format(id_subgroup)
        result += "      title: {}\n".format(subgroup_title)
        result += "      slug : {}\n".format(subgroup_slug)



f = open("_data/products.yml","w")
f.write(result)
f.close()
