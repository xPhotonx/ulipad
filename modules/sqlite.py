#!/usr/bin/env python
#coding=utf-8
import sqlite3
from  datetime import datetime 

class DocBase(object):
    def __init__(self):
        self.conn = sqlite3.connect('doc\docbase')
        self.c = c = self.conn.cursor()
        c.execute('''create table IF NOT EXISTS docbase
                (date text, 
                keyword text, 
                link text        
                )''')
        
    def get_date(self):
        date = (datetime.date(datetime.now()))
        return str(date)

    def insert_link(self, index, link):
        date = self.get_date()
        temp = self.get_link(index, False)
        if temp:
            #link = temp + '\n' + link
            self.c.execute("update docbase set link=? where keyword=?", (link, index))
        else:
            for t in ((str(date), 
                       index, 
                       link),):
                self.c.execute('insert into docbase values (?,?,?)',t)
        self.conn.commit()
        
    def get_link(self, index, get_tag=False):
        self.c.execute('select * from docbase order by keyword')
        for row in self.c:
            if  row[1] == index:
                if  get_tag:
                    return "<info>\n" + row[2] + "</info>"
                else:
                    return row[2]
        #self.c.close()
            
    def get_count(self):
        self.c.execute("select count(*) from docbase")
        return self.c.fetchone()[0]

    def close(self):
        self.c.close()
    
    
    
    
