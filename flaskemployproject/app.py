from flask import Flask, flash,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
#from flask_sqlalchemy import SQLAlchemy
#import db
import mysql.connector as con

app=Flask(__name__)
app.secret_key = "my-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@localhost/company"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
#my SQL Connection
def det_db_connection():
    db = con.connect(
        host='localhost',
        user='root',
        passwd='root',
        database='company',
    )
    return db

@app.route("/")
def home():
    return "Mysql connection"




class Employee(db.Model):

    __tablename__ = "employee"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column( db.String(100), nullable=False)
    email = db.Column(db.String(100),nullable=False)
    salary = db.Column(db.Float,nullable=False)
    department = db.Column(db.String(100), nullable=False)


# Create table in MySQL
with app.app_context():
    db.create_all()

#Add employee
@app.route("/employee/add", methods=["GET", "POST"])
def add_employee():

    if request.method == "POST":

        id = request.form["id"]
        name=request.form["name"]
        email = request.form["email"]
        salary = request.form["sal"]
        department = request.form["department"]

        employee = Employee(
            id=id,
            name=name,
            email=email,
            salary=salary,
             department=department
        )

        db.session.add(employee)
        db.session.commit()

        return "Employee Added Successfully"

    return render_template("add_employee.html")

#read employee
@app.route("/showempdata", methods=["GET"])
def display_employee_data():
    employees = Employee.query.all()
    return render_template("empdata.html", empdata=employees)

@app.route("/updateemployee/<int:id>", methods=["GET","POST"])
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == "POST":
        employee.name = request.form["name"]
        employee.email = request.form["email"]
        employee.salary = request.form["sal"]
        employee.department = request.form["department"]
        db.session.commit()
        message = "Employee with ID  updated successfully."
        return render_template("editemployee.html", emp=employee, message=message)
    return render_template("editemployee.html", emp=employee)
@app.route("/deleteemployee/<int:id>", methods=["POST"])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash("Employee  deleted successfully.")          
    return redirect("/showempdata")
    #return render_template("empdata.html", message=message) 

if __name__=="__main__":
    app.run(debug=True,use_reloader=False)