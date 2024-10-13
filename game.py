from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   session,
                   url_for,
                   Blueprint)
from base import Base
import sqlite3
from datetime import datetime
import random
bd=Base()

tabl="""id Integer primary key autoincrement,
   name text,
   ques text,
   res text,
   answer text,
   corect bool,
   time text,
   session integer,
   position integer,
   level text
"""

bas='data/game_tbl.db'



#bd.add_to_table(table='game',pole='ques',data='2+2',bd=bas)

#print(bd.select_all(table='game',bd=bas))
def formating_level(level):
  #l={'min1'=None,'max1'=None,'min2'=None,'max2'=None,'operand'=None}
  if level=='1':
    l={'min1':1,'max1':9,'min2':1,'max2':9,'operand':'+-','time':30}
  elif level=='2':
    l={'min1':1,'max1':9,'min2':1,'max2':9,'operand':'*/','time':30}
  elif level=='3':
    l={'min1':2,'max1':9,'min2':2,'max2':10,'operand':'*/','time':30}
  elif level=='4':
    l={'min1':1,'max1':99,'min2':2,'max2':9,'operand':'*/+-','time':120}
  elif level=='5':
    l={'min1':11,'max1':99,'min2':12,'max2':99,'operand':'*/','time':120}
  else:
    l={'min1':1,'max1':9,'min2':1,'max2':9,'operand':'+-','time':300}
  return l

def add_data(data,name,num,level):
    with bd.lock:
        bd.connect(bas)
        bd.c.execute('''INSERT INTO game (name,ques,res,answer,corect,position,time,session,level)      
                        values(?,?,?,?,?,?,?,?,?);''',
                        (name,data['ques'],
                        data['res'],
                        data['userAnswer'],
                        data['isCorrect'],
                        data['pos'],
                        datetime.now(),
                        num,
                        level,));
        
        bd.conn.commit()
    bd.close()
    
def get_last_session(name):
    with bd.lock:
        bd.connect(bas)
        bd.c.execute(f"SELECT * FROM game WHERE name = ?",(name,))
        res=bd.c.fetchall()
        if res:
            result=res[-1][7]
        else:
            result=0
    bd.close()
    return result
    
    
def get_all_by(pole='name',value=''):
    with bd.lock:
        bd.connect(bas)
        bd.c.execute(f"SELECT * FROM game WHERE {pole} = ?",(value,))
        result=bd.c.fetchall()
    bd.close()
    return result

    
    
def get_one(pole,value):
    result=get_all_by(pole,value)[-1]
    return result
    
def get_session(name,session):
    with bd.lock:
        bd.connect(bas)
        bd.c.execute("SELECT * FROM game WHERE name = ? AND session = ?", (name, session,))
        result=bd.c.fetchall()
    bd.close()
    return result
    
def del_all(table):
    r=bd.get_all(table,bd=bas)
    for i in r:
        with bd.lock:
            bd.connect(bas)
            #bd.conn.execute(f"DELETE FROM {n} WHERE id = ?", (i[0],))
            print(f'{i}')
            bd.conn.commit()
            bd.close()
def view_users(table='User'):
    r=bd.get_all(table,bd=bas)
    for i in r:
        print(i)
        
def get_user_Rating(name):
  p=get_all_by(pole='name',value=name)
  n=None
  old=None
  t=None
  if len(p)==0:
    ent=0
  else:
    ent=p[-1][7]
    old=1000
    for i in p:
      res=get_session(name,i[7])
      if old> len(res):
        old=len(res)
        n=res
    t1=str(datetime.strptime(n[-1][6],"%Y-%m-%d %H:%M:%S.%f")-datetime.strptime(n[0][6],"%Y-%m-%d %H:%M:%S.%f"))
    t=t1.split('.')[0]
  return {'enter':ent,'lengt':old,'time':t}   
    
  
  
if __name__=='__main__':
    from time import sleep
    #bd.create_table(name='game', table=tabl,bd=bas)
    #del_all('game')
    #view_users('game')
    #add_data({'ques': '18 / 3', 'res': 6, 'userAnswer': '1', 'isCorrect': False, 'pos': 350},'Vladimir',0)
    #view_users('game')
    #print(get_one('name','qazaq'))
    #p=get_all_by(pole='name',value='Vladimir')
    #print('количество записей ',len(p))
    #print('первая \n',p[0])
    #print('последняя \n',p[-1])
    #r=datetime.strptime(p[-1][6],"%Y-%m-%d %H:%M:%S.%f")
    #g=datetime.now()
    #print(r)
    #print(g-r)
    #r=datetime.strptime(r,"%Y-%m-%d %H:%M:%S.%f")
    #print((r.hour*3600)+(r.minute*60)+r.second)
    w=get_user_Rating('qazaq')
    print(w['time'])
    #res=get_session('qazaq','12')
    #print(res)
    
    
    
