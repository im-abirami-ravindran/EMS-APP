from flask import Flask,render_template,Response,jsonify,redirect,request,flash,session,url_for
from flask_pymongo import PyMongo,ObjectId
from flask_session import Session
import bcrypt

app= Flask(__name__,static_url_path="/static")
app.secret_key='Nothing'
app.config['SESSION__PERMANENT']=False
app.config["SESSION_TYPE"]='filesystem'

app.config['MONGO_URI']="mongodb://localhost/EmployeeMS"
mongo = PyMongo(app)
global username
dbm = mongo.db.EmployeeMSystem
db = mongo.db.EmployeeDetails

@app.route("/")
def index():
    return render_template("index.html")

#SIGN UP FOR EMPLOYEES
@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == "POST":
        new_username = request.form['name']
        new_email = request.form['email']
        new_password = request.form['password']
        haspassword = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        id = dbm.insert_one({
            'name': new_username,
            'email': new_email,
            'password': new_password
        })
        flash(new_username,"Successfully Signed In")
        return redirect("/")

    return render_template("signup.html")

#LOGIN FOR BOTH EMPLOYEE/ADMIN
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        global username
        username=request.form['name']
        session['username']=username
        password=request.form['password']
        if dbm.find_one({'name':username})  and dbm.find({'password':password}):
             if username == 'admin':
                flash(username+" Successfully Signed In")
                return redirect("/admin")
             else:
                flash(username+ " Successfully Signed In")
                return redirect("/employee")
        else:
            return redirect("/signup")
    return render_template('login.html')

#ADMIN HOME PAGE
@app.route("/admin",methods=['GET','POST'])
def admin():
    detail=[]
    for i in db.find({},{"_id":0}):
        detail.append(i)
    # app.add_url_rule("/","/edit")
    return render_template("admin.html",newuser=detail)

#EMPLOYEE HOME PAGE
@app.route("/employee",methods=['GET','POST'])
def employee():
    detail=[]
    session['username']=username
    if db.find({'ename':username}):
        detail=db.find({'ename':username},{"_id":0})
        #print(detail) 
    return render_template("employee.html",newuser=detail)


#ADMIN ADDING NEW EMPLOYEE
@app.route("/admin/add",methods=['GET','POST'])
def aedit():
    db = mongo.db.EmployeeDetails
    if request.method == 'POST':
        eid=request.form['eid']
        ename=request.form['ename']
        email=request.form['email']
        dob=request.form['dob']
        Dept=request.form['Dept']
        LeaveReq=request.form['LeaveReq']
        adder=db.insert_one({
            'eid': eid ,
            'ename':ename,
            'email':email,
            'DoB': dob,
            'Dept': Dept,
            'LeaveReq':LeaveReq
        })
        return redirect("/admin")
    return render_template("add.html")

#EMPLOYEE EDITING HIS EMAIL & DOB
@app.route("/employee/add",methods=['GET','POST'])
def eedit():
    session['username']=username
    d=[]
    if request.method =='GET':
        empdata=db.find({'ename':username},{'_id':0})
        for i in empdata:
            d.append(i)
            print(d)
    if request.method == 'POST':
        email=request.form['email']
        dob=request.form['dob']
        if db.find({'eid':{'$exists':True},'ename':username}):
            updater=db.update_one({'ename':username},{'$set':{
            'email': email, 
            'DoB': dob,
            }})
            dbm.update_one({'name':username},{'$set':{'email':email}})
            return redirect("/employee")
        else:
            flash("Wait till Admin gives assigns you a ID")
    return render_template("eadd.html",newuser=d)

#EMPLOYEE APPLICATION LEAVE
@app.route("/employee/leave",methods=['GET','POST'])
def eleave():
    session['username']=username
    if request.method== 'POST':
        #Nod=request.form['nod']
        FromDate=request.form['FromDate']
        ToDate=request.form['ToDate']
        Nod=request.form['nod']
        Leave=request.form['LeaveReq']
        updateleave=db.update_one({'ename':username},{'$set':{
            'FromDate':FromDate,
            'ToDate':ToDate,
            'NoDays': Nod,
            'LeaveReq':Leave
        }})
        return redirect("/employee")
    return render_template("eleave.html")
        
#DELETE FROM ADMIN SIDE
@app.route("/admin/<id>",methods=['GET','POST'])
def delete(id):
    db.delete_one({'eid':id})
    return redirect(url_for('admin'))
    #return render_template("admin.html")

#LOGOUT OF USERS
@app.route("/logout",methods=['GET','POST'])
def logout():
    session["username"]=None
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True,port=5000)