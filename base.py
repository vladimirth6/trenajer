import sqlite3
import threading
#from level import Users
class Base:
  def __init__(self):
    self.conn=None
    self.c=None
    self.lock = threading.Lock()
    #self.connect()
    
      
  def createUserTable(self):
     self.create_table('data/Users.db',"User","""
            userid INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Password TEXT,
            Phone Text,
            Mail Text,
            Prava Text,
            SekretAns Text,
            Otvet Text
            """)   
  
  def create_table(self, name, table,bd='data/Users.db'):
    with self.lock:
      self.connect(bd)
      self.c.execute(f"CREATE TABLE IF NOT EXISTS {name} ({table})")
      self.conn.commit()
      print(f'Создана таблица {name}')
    self.close()
    
  def add_to_table(self,table,pole,data,bd='data/Users.db'):
      with self.lock:
        self.connect(bd)
        #self.c.execute(f"""INSERT INTO {table}({pole}) Values (?); """,data)
        self.c.execute(f"INSERT INTO {table}({pole}) VALUES (?)", (data,))
        self.conn.commit()
      self.close()
      
  def get_all(self,table='',bd='data/Users.db'):
    with self.lock:
        self.connect(bd)
        self.c.execute(f"SELECT * FROM {table}")
        result=self.c.fetchall()
        self.close()
    return result
        
  def connect(self,bd='data/Users.db'):
        self.conn = sqlite3.connect(bd)
        self.c = self.conn.cursor()   
 
  def add_user(self, usr):
        with self.lock:
            self.connect()
            self.c.execute("INSERT INTO User(Name, Password,Phone,Mail,SekretAns,Otvet) VALUES (?,?,?, ?,?,?);", usr)
            self.conn.commit()
            self.close()
  def set_pass(self,name='', password=''):
      with self.lock:
            self.connect()
            self.c.execute("UPDATE User SET Password = ? WHERE Name = ?", (password, name))
            self.conn.commit()
            self.close()
  def set_prava(self,name='',prava=''):
    with self.lock:
      self.connect()
      self.c.execute("UPDATE User SET Prava = ? WHERE Name = ?", (prava, name))
      self.conn.commit()
      self.close()
      
  def get_by_name(self,name=''):
    with self.lock:
      self.connect()
      self.c.execute("SELECT * FROM User WHERE Name = ?",(name,))
      result=self.c.fetchone()
      self.close()
    return result
    
  def get_autorised(self,name='',password=''):
    result=self.get_by_name(name=name)
    if password==result[2]:
      return True
    return False
               
  def print_user_info(self,name=''):
    result=self.get_by_name(name=name)
    if result:
      for i in result:
        print(i)
    else:
      print(f"Юзер {name} не знайдений")
      
  def check_user(self, name):
    result=self.get_by_name(name=name)
    if result:
      return True
    return False
  
  #def get_record(self,name):
      
  def close(self):
    self.conn.close()
if __name__=='__main__':
  bd=Base()
  bd.createUserTable() 
