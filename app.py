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

class Post:
    def __init__(self,username,text):
        self.username=username
        self.text=text
    def __repr__(self):
        rep=self.username+ ":"+ self.text
        return rep


users=[]
users.append(User(id=1,username='Darek',password='123'))
users.append(User(id=2,username='Krystian',password='123'))
users.append(User(id=3,username='Bartek',password='pass'))
users.append(User(id=4, username='Seba',password='123'))
users.append(User (id=5,username='Marek',password='123'))

posts=[]
posts.append(Post("Darek","tralalala"))
posts.append(Post("Darek","tralalala22222"))
posts.append(Post("Seba","alamakota"))
posts.append(Post("Bartek","kot nie ma ali"))

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
            return redirect(url_for('main_side'))
        else:
            return render_template('login.html', login=username, foo=True)

    return render_template('login.html')


@app.route("/logout",methods=('POST',))
def logout():
    del session['username']
    del session['timestamp']
    return redirect(url_for('login'))

@app.route("/profil" ,methods=('GET', 'POST'))
# @inactivity_logout
def profil():
    # age=session['timestamp']
    # #age=(datetime.datetime.now()-session['timestamp'])
    return render_template('profil.html', name=session['username'])
@app.route("/main", methods=('GET','Post'))
def main_side():
    username=users[0].username
    if request.method=="POST":
        return redirect(url_for('profil'))
    return render_template('main_side.html',name=username,username=posts[0].username,username1=posts[1].username,
                           username2=posts[2].username,
                           username3=posts[3].username,
                           wpis=posts[0].text,wpis1=posts[1].text,wpis2=posts[2].text,wpis3=posts[3].text)

