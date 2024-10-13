from threading import Thread 
from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   session,
                   url_for)
from flask_socketio import SocketIO, emit
from auth import auth_bp
import json
from flask import jsonify
import sqlite3,random
#from base import Base
from game import (add_data,
                 get_last_session,
                 get_session,
                 formating_level,
                 get_user_Rating)
from bot import Bot
from datetime import datetime

app = Flask(__name__)
socketio=SocketIO(app)
#BD=Base()
# Регистрируем <link>Blueprint</link> для авторизации 
app.register_blueprint(auth_bp, url_prefix='/auth')
s_us={"name": None,
      "position": 350, 
      "x":None, 
      "old":450,
      "step":-10,
      "flag":True, 
      "level": None,
      "color":"green",
      "raketa":0}
users=[]
bots=[]
chatBufer=[]
def getIndexBuName(name):
  o=0
  for i in users: 
    if i['name']==name:
      return o
    o+=1
  return None
  
  
def get_time_now():
   t=datetime.now()
   return f"{t.hour}:{t.minute}:{t.second}"

@socketio.on('connect')
def handle_connect():
    print(f'''{session['username']} подключился''')
    #chatBufer.append({'name':'Система','text':f"Зайшов - {session['username']}"})
 
@socketio.on('disconnect')
def handle_disconnect():
  i=getIndexBuName(session['username'])
  if i!=None:
    print(f'''удаляем {session['username']} из users''')
    del users[i]
  else:
    print(f'''В users не удалось найти {session['username']}''')
  print(f'''{session['username']} отключился''')


#Обновим данные полета ракет в ядре
@socketio.on('Obnova')
def Obnova(d):
  name=d['name']
  #m=json.loads(d['data'])
  m=json.loads(d['data'])
  #print(f'обновим {name} \n- {m}')
  i=getIndexBuName(name)
  if i!=None:
    users[i]=m
        
@socketio.on('toBase')
def socToBase(data):
  print(f"заносим в базу от {session['username']}")
  add_data(data,session['username'],session['number'],session['level'])
  #emit('response',json.dumps(users))#отправим новые позиции вссех пользователей

@socketio.on('Obmen')
def Obmen(data):
  emit('response',json.dumps(users))#отправим новые позиции вссех пользователей
  
@socketio.on('First')
def first(t):
  emit('response',json.dumps(users))
  
    
@socketio.on('readChat')
def readChat(t):
  global chatBufer
  emit('getChat',chatBufer)

@socketio.on('toChat')
def toChat(text):
  global chatBufer
  text['time']=get_time_now()
  chatBufer.append(text)
  print('Заносим в чат ',text)
    
@app.route('/endSesion')
def end_sesion():
  global chatBufer
  for i in users:
    if i==session['username']:
      print(f"удалим {session['username']} из ядра")
      users.remove(i)#удаляем пользователя из ядра
      if len(users)==0:
        chatBufer=[]
  h=datetime.now()        
  chatBufer.append({'name':'Система',
                    'text':f"{session['username']} -покинув гру ",
                    'time':get_time_now()})
  return redirect(url_for('index'))

@app.route('/fromBot',methods=['POST'])
def fromBot():
  global chatBufer
  if request.method=='POST':
    pos=request.form['pos']
    name=request.form['name']
    if request.form['run']=='stop':#останавливаем бота
      for i in bots:
        if name==i['name']:
          #i['bot'].join()
          h=datetime.now()
          chatBufer.append({'name':'Система',
                            'text':f"{name} -покинув гру ",
                            'time':get_time_now()})
          bots.remove(i)#останавливаем и удаляем бот из списка
      #print(users)
      for i in users:
        if name==i['name']:
          users.remove(i)# удаляем бота из ядра
          if len(users)==0:
            chatBufer=[]
          
    else:
      #обновляем позицию ракеты бота
      i=getIndexBuName(name)
      if i!=None:
        users[i]['old']=int(users[i]['position'])
        users[i]['position']=pos
        users[i]['flag']=True
      print(f'{name} позиция {pos}')
      #print(users)
  else:
    print('Бот херню прислал')
  return 'Ok' 
  
@app.route('/')
def index():
    data=None
    try:
        name=session ['username']
    except:
        name=''
    if name:
        session['number']=get_last_session(name)+1
        data=get_user_Rating(name)
        print(f"Для {name} установлена сесия № {session['number']}")
    session['SameSite']=None
    session.modified = True
    return render_template('index.html',user=name,data=data)
@app.route('/newGame')
def newGame():
    print('В новой игре \n',users)
    session['number']+=1;
    add_user_to_kernel(session['level'])
    level=formating_level(session['level'])
    h=datetime.now()
    chatBufer.append({'name':'Система',
                      'text':f"{session['username']} знову в грi ",
                      'time':get_time_now()})
    return render_template('умн_0_4.html',
                            user=session ['username'],
                            level=level,
                            lvl=session['level'])

def add_user_to_kernel(level):
    session['level']=level
    us=s_us.copy()
    us['name']=session ['username']
    us['position']=350
    us['level']=level
    us['x']=random.randrange(50,400,40)
    us['old']=450
    users.append(us) 
    #print('добавили в users учасника ',users )
    #print('в игре ',(len(users)),' учасников.')
    session.modified = True 
      
def add_bot(name,levelD,levelN,rejim):
      if rejim=='bot':
        newName='Bot-'+str(len(users))
      else:
        newName='Тiнь-'+session['username']
      bots.append({'name':newName,'bot':Bot(session['username'],newName,levelD,levelN,rejim)})
      print('Bot ',bots[-1]['bot'])
      us=s_us.copy()
      us['name']=newName
      us['position']=350
      us['level']=levelN
      us['x']=random.randrange(50,400,40)
      us['old']=450
      users.append(us)
      bots[-1]['bot'].start()
      h=datetime.now()
      chatBufer.append({'name':'Система',
                        'text':f"Зайшов - {newName}",
                        'time':get_time_now()})
      #print('добавили в users бота ',users )
      print(f"создан бот {users[-1]['name']}  {newName}")
      
      
@app.route('/titul2',methods=['POST','GET'])
def titul2():
  if request.method=="POST":
    level={'min1':int(request.form['min1']),
            'max1':int(request.form['max1']),
            'min2':int(request.form['min2']),
            'max2':int(request.form['max2']),
            'operand':request.form['operand'],
            'time':int(request.form['time'])}
    game=request.form['game']
    if request.form['game']!='1':
      add_bot(session ['username'],level,int(request.form['level']),game)
    add_user_to_kernel("6")
    h=datetime.now()
    chatBufer.append({'name':'Система',
                      'text':f"Зайшов - {session['username']}",
                      'time':get_time_now()})
    session.modified = True
    return render_template('умн_0_4.html',
                            user=session ['username'],
                            level=level,
                            lvl='власний')
  return redirect(url_for('/')) 
     
@app.route('/titul',methods=['POST','GET'])
def titul():
  if request.method=='POST':
    #for i in users:
    #    if session ['username']==i['name']:
    #      print('Дубликат')
    #      return redirect('/')
    if request.form['level']=="6":
      return render_template('titul2.html')      
    level=formating_level(request.form['level'])
    game=request.form['game']
    if request.form['game']!='1':
      add_bot(session ['username'],level,int(request.form['level']),game)
    add_user_to_kernel(request.form['level'])
    chatBufer.append({'name':'Система',
                      'text':f"Зайшов - {session['username']}",
                      'time':get_time_now()})
    session.modified = True
    return render_template('умн_0_4.html',
                            user=session ['username'],
                            level=level,
                            lvl=request.form['level'])
  session.modified = True                          
  return render_template('titul.html',user=session ['username'])
    

@app.route('/ERROR')
def error():
  render_template('ERROR.html',error="Ползователь может иметь лишь одну сесию")
if __name__=='__main__': 
  app.debug = True
  # set the secret key.  keep this really secret:
  app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
  #app.host='0.0.0.0'
  socketio.run(app,host='0.0.0.0')
  #app.run(host='0.0.0.0' ) 
