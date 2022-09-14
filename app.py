from flask import Flask,render_template,Response,jsonify,redirect,request,flash,session
from flask_pymongo import PyMongo,ObjectId
from flask_session import Session
import bcrypt

app= Flask(__name__,static_url_path="/static")
app.secret_key='Nothing'
app.config['SESSION__PERMANENT']=False
app.config["SESSION_TYPE"]='filesystem'

app.config['MONGO_URI']="mongodb://localhost/EmployeeMS"
mongo = PyMongo(app)

db = mongo.db.EmployeeMSystem

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == "POST":
        new_username = request.form['name']
        new_email = request.form['email']
        new_password = request.form['password']
        haspassword = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        id = db.insert_one({
            'name': new_username,
            'email': new_email,
            'password': new_password
        })
        flash(new_username,"Successfully Signed In")
        return redirect("/")

    return render_template("signup.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        global username
        username=request.form['name']
        session['username']=username
        password=request.form['password']
        if db.find_one({'name':username})  and db.find({'password':password}):
             if username == 'admin':
                flash(username+" Successfully Signed In")
                return redirect("/admin")
             else:
                flash(username+ " Successfully Signed In")
                return redirect("/employee")
        else:
            return redirect("/signup")
    return render_template('login.html')

@app.route("/admin",methods=['GET','POST'])
def admin():
    db = mongo.db.EmployeeDetails
    detail=[]
    for i in db.find({},{"_id":0}):
        detail.append(i)
    # app.add_url_rule("/","/edit")
    return render_template("admin.html",newuser=detail)


@app.route("/employee",methods=['GET','POST'])
def employee():
    db=mongo.db.EmployeeDetails
    detail=[]
    session['username']=username
    if db.find({'ename':username}):
        for i in db.find({'ename':username},{"_id":0}):
            detail.append(i) 
    return render_template("employee.html",newuser=detail)

@app.route("/admin/add",methods=['GET','POST'])
def aedit():
    db = mongo.db.EmployeeDetails
    if request.method == 'POST':
<<<<<<< HEAD
=======
        print(request.form['eid'])
>>>>>>> a56c1252cac41d62a13cea509e34e1be18231a4c
        eid=request.form['eid']
        ename=request.form['ename']
        email=request.form['email']
        dob=request.form['dob']
        Dept=request.form['Dept']
        nod=request.form['nod']
        FromDate=request.form['FromDate']
        ToDate=request.form['ToDate']
        Ain=request.form['Ain']
        Aout=request.form['Aout']
        LeaveReq=request.form['LeaveReq']
        adder=db.insert_one({
            'eid': eid ,
            'ename':ename,
            'email':email,
            'DoB': dob,
            'Dept': Dept,
            'NoDays':nod,
            'FromDate':FromDate,
            'ToDate':ToDate,
            'Ain':Ain,
            'Aout':Aout,
            'LeaveReq':LeaveReq
        })
<<<<<<< HEAD
        flash(eid ," ",ename," Successfully Signed In")
    return render_template("add.html")

@app.route("/admin/<eid>",methods=['GET','POST'])
def delete(eid):
    return render_template("admin.html")

@app.route("/logout",methods=['GET','POST'])
def logout():
    session["username"]=None
    return render_template("login.html")
=======
    return render_template("add.html")
>>>>>>> a56c1252cac41d62a13cea509e34e1be18231a4c

if __name__ == "__main__":
    app.run(debug=True,port=5000)