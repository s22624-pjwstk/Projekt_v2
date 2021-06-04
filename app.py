import datetime
from flask import(
    Flask, render_template,request,session,redirect,url_for,)


class User:
    def __init__(self,id,username,password):
        self.id = id
        self.username = username
        self.password = password
    def __repr__(self):
        return f'<User:{self.username}'

users=[]
users.append(User(id=1,username='Darek',password='123'))
users.append(User(id=2,username='Krystian',password='123'))
users.append(User(id=3,username='Bartek',password='pass'))
users.append(User(id=4, username='Seba',password='123'))

app = Flask(__name__)
app.secret_key='sekretnyklucz'

@app.route("/")
def jakos():

    return redirect(url_for("login"))
@app.route("/login",methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        user = [x for x in users if x.username == username]
        if user and user[0].password == password:
            session['user_id'] = user[0].id
            session['username'] = username
            session['timestamp']=datetime.datetime.now()
            return redirect(url_for('home'))
        else:
            return render_template('login.html', login=username, foo=True)

    return render_template('login.html')

# def inactivity_logout(fn):
#     def wrapped(*args,**kwargs):
#         age = (datetime.datetime.now() - session['timestamp'])
#         if age > datetime.timedelta(seconds=10):
#             return redirect(url_for('logout'))
#         session['timestamp'] = datetime.datetime.now()
#         return fn(*args, **kwargs)
#     wrapped.__name__=fn.__name__
#     return wrapped

@app.route("/logout",methods=('POST',))
def logout():
    del session['username']
    del session['timestamp']
    return redirect(url_for('login'))

@app.route("/profil" ,methods=('GET', 'POST'))
# @inactivity_logout
def home():
    # age=session['timestamp']
    # #age=(datetime.datetime.now()-session['timestamp'])
    return render_template('profil.html', name=session['username'])