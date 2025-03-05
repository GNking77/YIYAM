import random 
import os
import sqlite3
from flask import render_template,request,Flask,url_for,redirect
import mysql.connector
app=Flask(__name__,template_folder="template")


conn=mysql.connector.connect(
    host='0.tcp.in.ngrok.io',
    port='19216',
    user='root',
    password='Sathinj123@',
    database='credential',
    auth_plugin='mysql_native_password',
)
cur=conn.cursor()
format = "YIYAM"
data = ''
username=0
all=''
update_id=''


def check_login_details_user(Username,Password):
    global username,cur,conn
    cur=conn.cursor()
    cur.execute("select * from student where username=%s and password=%s;",(Username,Password))
    username=Username
    return cur.fetchone()
def check_login_details_email(Email,Password):
    global username,cur,conn
    cur=conn.cursor()
    cur.execute("select * from student where email=%s and password=%s;",(Email,Password))
    username=Email
    return cur.fetchone()
def active_user():
    conn=sqlite3.connect("active.db")
    cur=conn.cursor()
    cur.execute("create table if not exists user(user text);")
    cur.execute("insert into user(user) values(%s);",(username,))
    conn.commit()
#def update_login_details(Email,Username):
    # conn=sqlite3.connect('st.db')
    # cur=conn.cursor()
    # cur.execute("select * from student where email=? and username=?;",(Email,Username))
    # return cur.fetchone()
def update_login_details_email(Email):
    global cur
    cur=conn.cursor()
    cur.execute("select * from student where email=%s;",(Email,))
    return cur.fetchone()
def update_login_details_user(Username):
    cur=conn.cursor()
    cur.execute("select * from student where username=%s;",(Username,))
    return cur.fetchone()
def delete_details_user(Username,Password):
    cur=conn.cursor()
    cur.execute("select * from student where username=%s and password=%s;",(Username,Password))
    return cur.fetchone()
def delete_details_email(Email,Password):
    cur=conn.cursor()
    cur.execute("select * from student where email=%s and password=%s;",(Email,Password))
    return cur.fetchone()
def check_register_details(Username, Email):
    cur=conn.cursor()
    cur.execute("select * from student where username=%s or email=%s;",(Username, Email))
    return cur.fetchone()
def user():
    cur=conn.cursor()
    cur.execute("select Username from student")
    user=cur.fetchone()
    user=user
@app.route("/")
def index():
    return render_template("login.html")
@app.route("/login",methods=['GET','POST'])
def login():
        global conn, cur
        Email=request.form['email']
        Username=request.form['email']
        Password=request.form['passw']
    
        if request.method=='POST' and check_login_details_email(Email,Password) or check_login_details_user(Username,Password):
            #return render_template("student_data.html")
            cur=conn.cursor()
            cur.execute("select * from data where col0!='0'")
            all=cur.fetchall()
            cur.execute("select Token from student where username=%s or email=%s;",(username,username))
            Id=cur.fetchone()[0]
            print(Id)
            
            try:
                cur.execute('select col0 from data where col0=%s;',(Id,))
                userid = cur.fetchone()[0]
                print(userid)
            except:
                userid=0
            data = {'userid': userid, 'data': all}
            return render_template("database.html",data=data)
            #return '<center><h1><a href="/student_details">Student details</a><br><br><a href="/add_student">Add student</a><br><br><a href="/delete_student">Delete student</a><br><br><a href="/update_student">Update student</a></h1></center>'
        else:   
            return '<h1>Invalid username and password... <a href="/reg">Register</a> OR <a href="/">Try again...</a></h1>'
@app.route("/register",methods=["GET","POST"])
def register():
    global conn, cur
    id = random.randint(1000, 9999)
    id = str(id)
    id = format+id
    if request.method=="POST":
        User=request.form['user']
        Email=request.form['email']
        Password=request.form['password']
        cur=conn.cursor()
        if check_register_details(User,Email):
            return '<h1>Username or Email already exist! Please <a href="/reg">Try again</a> or <a href="/">Login</a></h1>'
        else:
            cur.execute("insert into student (Username,Email,Password,Token) values(%s,%s,%s,%s)",(User,Email,Password,id))
            conn.commit()
        return '<h1>Registered successfully! Click to <a href="/">Login</a></h1>'
    
@app.route("/reg")
def reg():
        return render_template("register.html")
@app.route("/forgot",methods=['POST','GET'])
def forgot():
    global conn, cur
    if request.method=="POST":
        Username=request.form['user']
        Email=request.form['user']
        new_pass=request.form['new_pass']
        con_pass=request.form['con_pass']
        if update_login_details_email(Email) or update_login_details_user(Username):
            if new_pass==con_pass:
                cur=conn.cursor()
                cur.execute("update student set password=%s where username=%s or email=%s;",(new_pass,Username,Email))
                conn.commit()
                return '<h1>Update password successfully! <a href="/">Login</a></h1>'
            else: 
                return '<h1>Password not matched please try again!<a href="/forgotp">Try again</a></h1>'
        else:
            return '<h1>Invalid details! Please <a href="/for">Try again...</a></h1>'
    return render_template("login.html")
@app.route("/for")
def forg():
    return render_template('forgot.html')
@app.route("/forgotp")
def forgotp():
    return render_template("forgot.html")
@app.route("/erase",methods=['GET','POST'])
def erase():
    if request.method=="POST":
        Username=request.form['user']
        Email=request.form['user']
        Password=request.form['password']
        if delete_details_email(Email,Password) or delete_details_user(Username,Password):
            cur=conn.cursor()
            cur.execute("delete from student where username=%s or email=%s and password=%s;",(Username,Email,Password))
            conn.commit()
            return '<h1>Delete details successfully! Click to <a href="/reg">Register</a></h1>'
        else:
            return '<h1>Invalid Username or Email! <a href="/delete">Try Again</a> or <a href="/">Login</a></h1>'
    return render_template("login.html")
@app.route("/index")
def Home():
    return render_template("database.html")
@app.route("/Home",methods=['GET','POST'])
def add():
    if request.method=='POST':
        global username,all,data,conn,cur
        mobile = '+91 '
        Name=request.form['name']
        City=request.form['city']
        Mobile=request.form['mobile'] 
        Blood=request.form['blood']
        Mobile=mobile+Mobile
        cur=conn.cursor()
        cur.execute("select Token from student where username=%s or email=%s;",(username,username))
        Id=cur.fetchone()[0]
        cur.execute("insert into data(col0,col1,col2,col3,col4) values(%s,%s,%s,%s,%s);",(Id,Name,City,Mobile,Blood))
        conn.commit()
        cur.execute("select * from data where col0!='0'")
        all=cur.fetchall()
        data={'userid': Id,'data':all}
        return redirect(url_for('add'))
    return render_template("database.html",data=data)
    #return render_template("database.html")
        #return '<h1>Data inserted successfully! <a href="/student_details">See details</a></h1>'

@app.route("/row_update",methods=['GET','POST'])
def row_update():
    global update_id
    userid = request.args.get('userid')
    update_id=userid
    return redirect(url_for('update'))
@app.route("/update",methods=['GET','POST'])
def update():
    
    
    if request.method=='POST':
        global all,data,username,conn,cur
        mobile='+91 '
        userid = request.form['userid']
        Name=request.form['name']
        City=request.form['city']
        Mobile=request.form['mobile'] 
        Blood=request.form['blood']
        Mobile=mobile+Mobile
        cur.execute("select Token from student where username=%s or email=%s;",(username,username))
        Id = cur.fetchone()[0]
        cur.execute('select col0 from data where col0=%s;',(Id,))
        userid = cur.fetchone()[0]
        cur.execute('update data set col1=%s, col2=%s, col3=%s, col4=%s where col0=%s;',(Name,City,Mobile,Blood,userid))
        conn.commit()
        cur.execute("select * from data where col0!='0'")
        all=cur.fetchall()
        data={'userid': userid,'data':all}
        return redirect(url_for('add'))
    return render_template("database.html",data=data)
@app.route('/details',methods=['GET','POST'])
def open():
    userid = request.args.get('userid')
    cur.execute("select * from data where col0=%s;",(userid,))
    one=cur.fetchone()
    return render_template("details.html",data=one)
@app.route("/delete",methods=['GET','POST'])
def delete():
    global all,username,conn,cur
    userid = request.args.get('userid')
    cur.execute('delete from data where col0=%s',(userid,))
    conn.commit()
    cur.execute("select * from data where col0!='0'")
    all=cur.fetchall()
    cur.execute("select Token from student where Username=%s or Email=%s;",(username,username))
    Id = cur.fetchone()[0]
    
    try:
        cur.execute('select col0 from data where col0=%s;',(Id,))
        userid = cur.fetchone()[0]
        print(userid)
    except:
        userid=0
    data = {'userid': userid, 'data': all}
    
    
    
    
    #cur.execute('select col0 from data where col0=%s;',(Id,))
    #conn.commit()
    #userid = cur.fetchone()[0]
    #data={'userid': Id,'data':all}
    return render_template('database.html',data=data)

        
if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
