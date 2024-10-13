from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   session,
                   url_for)
from auth import auth_bp
from f_tren import raketa
import sqlite3
from base import Base
app = Flask(__name__)
BD=Base()
# Регистрируем <link>Blueprint</link> для авторизации
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(raketa, url_prefix='/raket')
@app.route('/')
def index():
    try:
        name=session ['username']
    except:
        name=''
    return render_template('index.html',name=name)
@app.route('/go_rak')
def go_rak():
    return redirect(url_for('raket.index'))    
@app.route('/view_user_data',methods=['POST','GET'])
def view_user_data():
    if request.method=='GET':
        user=BD.get_by_name(session['username'])
        return render_template('view_user_data.html',user=user)
    else:
        return redirect (url_for('index'))
    
if __name__=='__main__': 
  app.debug = True
  # set the secret key.  keep this really secret:
  app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
  app.run(host='0.0.0.0' ) 
