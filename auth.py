from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   session,
                   url_for,
                   Blueprint)
from base import Base
import random
from datetime import datetime
import sqlite3
from validation import valid_password,valid_phone,valid_mail
auth_bp = Blueprint('auth', __name__)
BD=Base()
Max_password_in=1000

@auth_bp.route('/login', methods=['POST','GET'])
def login():
  if 'username' in session:
        print('Сесия идет')
        return redirect(url_for('index'))
  try:
      session ['count']+=1
  except:
      session['count']=0
  print('спроба входу  ',session['count'])
  if request.method=='POST':
    name=request.form['username'].replace(" ","")
    pas=request.form['password']
    session['username'] = name
    if not(BD.check_user(name)):#Регистрация нового чела
      return render_template('newuser.html',name=name)
      #return render_template('personal.html',usernsme=request.form['username'])
    else:#чел уже регился, проверим парол
      f=BD.get_autorised(name=name,password=pas)
      if ((session['count']>Max_password_in) or (not(f))):#не правильный парол
        session.pop('username', None)
        #session.pop('password', None)
        print('неправильный пароль')
        return render_template('login.html',err_pass=1)
      else:
          session['count']=0
          session.pop('count', None)
    print(request.form['username'],' вошел на сайт')
  else:
      return render_template('login.html')
  return redirect (url_for('index'))
  
@auth_bp.route('/newpass',methods=['POST','GET'])  
def   newpassword():
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method=='GET':
        return render_template('newpass.html')
    else:
        pas1=request.form['pas1']
        pas2=request.form['pas2']
        name=request.form['name'].replace(" ","")
        valid=valid_password(pas1,level='light')
        if valid!=None:
            return render_template('newpass.html',no_pass=valid)
        if pas1==pas2:
            BD.set_pass(name,pas1)
            print('сохраним новий пароль для ',name)
            return render_template('login.html')
        else:
            return render_template('newuser.html',name=name)
    

  
@auth_bp.route('/newuser',methods=['POST','GET'])
def newuser():
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method=='POST':
        name=request.form['name'].replace(" ","")
        pas1=request.form['pas1']
        pas2=request.form['pas2']
        valid=valid_password(pas1,level='light')
        if valid!=None:
            return render_template('newuser.html',name=name,no_pass=valid)
        
        if (name and not(BD.check_user(name)) and (pas1==pas2)):
            session['password']=pas1
            session['username']=name
            return render_template('add_new_user.html',usename=name)
        elif pas1!=pas2:
            return render_template('newuser.html',name=name,error='неодинаковый пароль')
        else:
            return render_template('login.html',name=name,err_pass=2)
    else:
        return render_template('newuser.html',name='')
            

@auth_bp.route('/add_new_user', methods=['POST'])
def add_new_user():
  phone=request.form['phone']
  mail=request.form['mail']
  name=session['username']
  password=session['password']
  an=request.form['ansver']
  ot=request.form['otvet']
  if valid_phone(phone) and valid_mail(mail):
    BD.add_user((name,password,phone,mail,an,ot))
    return redirect(url_for('index'))
  return render_template('add_new_user.html',name=name,error='Правильно укажите телефон и почту') 
  
  
@auth_bp.route('/logout',methods=['POST','GET'])
def logout():
    if request.method=='GET':
      return render_template('logout.html')
    # удалить из сессии имя пользователя, если оно там есть
    else:
      if request.form['answer']=='да':
        print(session['username'],' покинул сайт')
        session.pop('username', None)
        session.pop('password', None)
    return redirect(url_for('index'))

@auth_bp.route('/востановить',methods=['POST','GET'])
def repass():
  if 'username' in session:
        return redirect(url_for('index'))
  session['count']+=1
  if ((request.method=='GET')or(session['count']>Max_password_in)):
    return render_template('востановить1.html')
  else: 
    ret=request.form['ret']
    print ("ret=",ret)
    if ret=='1':
      name=request.form['name']
      user=BD.get_by_name(name)
      if user:
           return render_template('востановить2.html',user=user)
      else:
          return render_template('newuser.html',name=name)
    elif ret=='2':
        print ("второй заход")
        name=request.form['name']
        user=BD.get_by_name(name)
        if ((user) and (user[7]==request.form['ans'])):
            print(user,' ответ верен')
            return render_template('newpass.html',name=name)
        else:
            print(user," неправильно")
            return render_template('востановить1.html')         
  return redirect(url_for('index'))
  
  
if __name__=='__main__': 
  app.debug = True
  # set the secret key.  keep this really secret:
  app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
  app.run( )
