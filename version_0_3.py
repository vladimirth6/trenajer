from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   session,
                   url_for,
                   escape)
from auth import auth_bp
import json
from flask import jsonify
import sqlite3
from base import Base
from game import add_data,get_last_session,get_session
app = Flask(__name__)
BD=Base()
# Регистрируем <link>Blueprint</link> для авторизации 
app.register_blueprint(auth_bp, url_prefix='/auth')
#app.register_blueprint(raketa, url_prefix='/raket')
class kern:
    name=''
    pos=0
kernel=kern()
users=[]

@app.route('/')
def index():
    try:
        name=session ['username']
        
    except:
        name=''
    if name:
        session['number']=get_last_session(name)+1
        print(f"Для {name} установлена сесия № {session['number']}")
    session.modified = True
    return render_template('index.html',user=name)

@app.route('/умн',methods=['POST','GET'])
def umn():
    #global users
    f=True
    for i in users:
        if session ['username']==i[0]:
            f=False
    if f:
        users.append([session ['username'],350])
        session['index']=len(users)-1
        print(users)
        print(session['index'])
    session.modified = True
    return render_template('умн.html',user=session ['username'],)   
    
@app.route('/loser')
def loser():
    return render_template('лузер.html',user=session ['username'])
    
@app.route('/winer')
def winer():
    return render_template('перемога.html',user=session ['username'])  

@app.route('/result',methods=['POST','GET'])
def result():
   res=get_session(session ['username'],session['number'])
   count=len(res)
   err=0
   h=[]
   for r in res:
    if not(r[5]):
        err+=1
        s=r[2]+'='+r[3]
        h.append(s) 
   return render_template('результат.html',count=count,err=err,h=h,user=session ['username'])   
      
@app.route('/ajax', methods=['POST'])
def ajax():
    #global users
    history = request.get_json()
    print('Пришли данные от клиента ',session['username'])
    print(f"Текущая сесия пользователя {session['number']}")
    print(history[-1]['ques'],'=',history[-1]['userAnswer'])
    print(session['index'])
    #print(len(users))
    #print(users)
    # Обработка полученных данных
    # ...
    print(history[-1]['pos'])
    users[session['index']][1]=history[-1]['pos']
    print(f' новая позиция моей '+ users[session['index']][0]+' ракеты '+str(users[session['index']][1]))
    add_data(history[-1],session['username'],session['number'])
    response = {'users': users, 'message': 'Data received'}
    return jsonify(response) 


    
if __name__=='__main__': 
  app.debug = True
  # set the secret key.  keep this really secret:
  app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
  app.run(host='0.0.0.0' ) 
