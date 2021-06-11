import datetime
import sqlite3

from flask import(
    Flask, render_template,request,session,redirect,url_for,g)

class User:
    def __init__(self,id,username,password,followers=()):
        self.id = id
        self.username = username
        self.password = password
        self.followers=followers
    def __repr__(self):
        return f'<User:{self.username}'

class Post:
    def __init__(self,username,text):
        self.username=username
        self.text=text
    def __repr__(self):
        rep=self.username+ ":"+ self.text
        return rep

app = Flask(__name__)
app.secret_key='sekretnyklucz'

DATABASE="C:/Users/darek/PycharmProjects/Projekt_v2/twitter.sqlite"

def get_db():
    db = getattr(g,'_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv



@app.route("/")
def jakos():

    return redirect(url_for("login"))
@app.route("/login",methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        user = query_db("Select user_id,user_name,password From user Where user_name=?",(username,))
        if user and user[0]['password'] == password:
            session['user_id'] = user[0]['user_id']
            session['username'] = user[0]['user_name']
            session['timestamp']=datetime.datetime.now()
            return redirect(url_for('main_side'))
        else:
            return render_template('login.html', login=username, foo=True)

    return render_template('login.html')


@app.route("/logout",methods=('POST',))
def logout():
    del session['username']
    del session['timestamp']
    return redirect(url_for('login'))

@app.route("/profil/<int:user_id>" ,methods=('GET', 'POST'))
def profil(user_id):
    user=query_db("Select * from user where user_id=?",(user_id,),True)
    followers=query_db("Select * from user_followers where user_id=?",(user_id,))
    return render_template('profil.html',followers=followers,user=user)


@app.route("/post",methods=('POST',))
def post():
    user_id=session['user_id']
    text=request.form['new_post']
    database=get_db()
    new_tweet=database.execute("Insert into tweets (user_id,tweet_text) VALUES (?,?)",(user_id,text))
    database.commit()
    new_tweet.close()
    return redirect(url_for("main_side"))

@app.route("/main", methods=('GET','Post'))
def main_side():
    posts=query_db("Select * from tweets")
    if request.method=="POST":

        return redirect(url_for('profil'))
    return render_template('main_side.html',posts=posts,username=session['username'])

