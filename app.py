from flask import Flask,render_template,Response,jsonify,redirect,request,flash
from flask_pymongo import PyMongo,ObjectId
from flask_session import Session
import bcrypt

app= Flask(__name__,static_url_path="/static")
app.secret_key='Nothing'

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
        return redirect("/")

    return render_template("signup.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        global username
        username=request.form['name']
        password=request.form['password']
        if db.find_one({'name':username})  and db.find({'password':password}):
             if username == 'admin':
                return redirect("/admin")
             else:
                return redirect("/employee")
        else:
            print('No such user id exists.Please Sign In')
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
    if db.find({'ename':username}):
        for i in db.find({'ename':username},{"_id":0}):
            detail.append(i) 

    return render_template("employee.html",newuser=detail)

@app.route("/admin/edit",methods=['GET','POST'])
def aedit():
    return render_template("edit.html")

if __name__ == "__main__":
    app.run(debug=True,port=5000)