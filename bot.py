from threading import Thread 
import requests
from time import sleep
import random
import sqlite3
from base import Base
from game import get_all_by,get_session
from datetime import datetime
class Bot(Thread):
  def __init__(self,hname,name,levelD,levelN,rejim):
    super().__init__()
    self.name=name
    self.hname=hname
    self.time=levelD['time']
    self.level=levelN
    self.url='http://localhost:5000/fromBot'
    self.rejim=rejim
    self.intelect=20
    self.bd=Base()
    print('hname=',self.hname)
  def run_as_bot(self):
      pos=350
      print('Запущен как Bot')
      while (pos>=70 and pos<=400):
        t=random.randint(1, 4)
        p=random.randint(1, self.intelect-self.level)
        if p>self.level:
          pos-=10
        else:
          pos+=10
        sleep(t)
        payload={'name':self.name,'pos':pos,'run':'ok'}
        resp=requests.post(self.url,data=payload)
      pl={'name':self.name,'pos':-67,'run':'stop'}
      resp=requests.post(self.url,data=pl)
      
  def run(self):
    if self.rejim=='bot':
      self.run_as_bot()
    if self.rejim=='tin':
      print('tin')
      masiv=get_all_by(pole='name',value=self.hname)
      print('len ',len(masiv))
      if len(masiv)==0:#если еще нет своих записей
        self.run_as_bot()
      else:#сои записи есть 
        print('Запущен как Тень')
        oldSes=masiv[-1][7] #выберем последнюю
        ses=get_session(self.hname,oldSes)#self.hname,'12')#oldSes)
        o=datetime.strptime(ses[0][6],"%Y-%m-%d %H:%M:%S.%f")

        for i in ses:
          t=datetime.strptime(i[6],"%Y-%m-%d %H:%M:%S.%f")
          d=str(t-o)
          s1=int(d.split(':')[2].split('.')[0])
          print('\n\nзадержка ',s1)
          print('позиция  ',i[8],'\n\n')
          sleep(s1)
          o=t
          payload={'name':self.name,'pos':i[8],'run':'ok'}
          resp=requests.post(self.url,data=payload)
        pl={'name':self.name,'pos':-67,'run':'stop'}
        resp=requests.post(self.url,data=pl)  
          
          
          
