from flask import Flask,render_template,request,redirect,session
import mysql.connector
import os
app=Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="remotemysql.com",user="efUEDEdJmb",password="c0gjLGGwXq",database="efUEDEdJmb")
cursor=conn.cursor()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def about():
    return render_template('register.html')
@app.route('/sregister')
def about1():
    return render_template('sregister.html')


@app.route('/home')
def home():
    if 'user_id' in session:
       return render_template('home.html')
    else:
        return redirect('/')
@app.route('/dietplan')
def home1():
    if 'user_id' in session:
       return render_template('dietplan.html')
    else:
        return redirect('/')
@app.route('/weightgain')
def home2():
    if 'user_id' in session:
       return render_template('weightgain.html')
    else:
        return redirect('/')


@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    users=cursor.fetchall()

    if len(users)>0:
        session['user_id']=users[0][0]
        return redirect('/home')
    else:
        return redirect('/')
@app.route('/add_user',methods=['POST'])
def add_user():
    fname=request.form.get('ufname')
    lname = request.form.get('ulname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')
    cursor.execute("""INSERT INTO `users` (`user_id`,`fname`,`lname`,`email`,`password`) VALUES
     (NULL,'{}','{}','{}','{}')""".format(fname,lname,email,password))
    conn.commit()

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    session['user_id']=myuser[0][0]
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')



@app.route('/bmicalc',methods=['POST','GET'])
def calculate():

    bmi=''
    if request.method=='POST' and 'weight' in request.form and 'height' in request.form:
        Weight=float(request.form.get('weight'))
        Height=float(request.form.get('height'))
        bmi=round(Weight/((Height/100)**2),2)

    if 'user_id' in session:
        return render_template("bmi.html", bmi=bmi)
    else:
        return redirect('/')

@app.route('/hydcalc',methods=['POST','GET'])
def calculate1():

    hyd=''
    if request.method=='POST' and 'weight' in request.form and 'height' in request.form:
        Weight=float(request.form.get('weight'))
        Height=float(request.form.get('height'))
        hyd=round(Weight*0.033,3)

    if 'user_id' in session:
        return render_template("hyd.html", hyd=hyd)
    else:
        return redirect('/')





if __name__=="__main__":
    app.run(debug=True)


