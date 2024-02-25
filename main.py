import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request
current_dir=os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(current_dir,"database.sqlite3")
db=SQLAlchemy(app)
class Course(db.Model):
  __tablename__='course'
  course_id=db.Column(db.Integer(),autoincrement=True,primary_key=True)
  course_code=db.Column(db.String(),nullable=False,unique=True)
  course_name=db.Column(db.String(50),nullable=False)
  course_description=db.Column(db.String(50))
class Student(db.Model):
  __tablename__='student'
  student_id=db.Column(db.Integer(),autoincrement=True,primary_key=True)
  roll_number=db.Column(db.String(50),unique=True)
  first_name=db.Column(db.String(50))
  last_name=db.Column(db.String(50))
class enrollments(db.Model):
  __enrollments__='enrollments'
  enrollment_id=db.Column(db.Integer(),autoincrement=True,primary_key=True)
  estudent_id=db.Column(db.Integer())
  ecourse_id=db.Column(db.Integer())
@app.route("/",methods=["GET","POST"])
def index():
  student=Student.query.all()
  if(len(student)!=0):
    return render_template("home.html",student=student)
  else:
    return render_template("empty.html")
@app.route("/student/create",methods=["GET","POST"])
def form():
  if(request.method=="GET"):
    return render_template("form.html")
  if(request.method=="POST"):
    r=request.form["roll"]
    fn=request.form["f_name"]
    ln=request.form["l_name"]
    a= Student.query.filter_by(roll_number=r).first()
    if(a is None):
      squidward = Student(roll_number=r, first_name=fn, last_name=ln)
      db.session.add(squidward)
      db.session.commit()
      stri=[]
      for key, val in request.form.items():
        if(key.startswith("courses")):
          if(val=="course_1"):
            stri+=["MAD I"]
          elif(val=="course_2"):
            stri+=["DBMS"]
          elif(val=="course_3"):
            stri+=["PDSA"]
          elif(val=="course_4"):
            stri+=["BDM"]
      for i in stri:
        c=Course.query.filter_by(course_name=i).first()
        cid=c.course_id
        s=Student.query.filter_by(roll_number=r).first()
        sid=s.student_id
        ward = enrollments(estudent_id=sid, ecourse_id=cid)
        db.session.add(ward)
        db.session.commit()
      student=Student.query.all()
      return render_template("home.html",student=student)
    else:
      return render_template("alreadyexisit.html")
@app.route("/student/<int:student_id>/delete",methods=["GET"])
def delete(student_id):
  s=Student.query.filter_by(student_id=student_id).first()
  db.session.delete(s)
  db.session.commit()
  c=enrollments.query.filter_by(estudent_id=student_id).all()
  for x in c:
    db.session.delete(x)
    db.session.commit()
  student=Student.query.all()
  return render_template("home.html",student=student)
@app.route("/student/<int:student_id>",methods=["GET"])
def studentdetail(student_id):
  student=Student.query.filter_by(student_id=student_id).first()
  erolls=enrollments.query.filter_by(estudent_id=student_id).all()
  temp=[]
  for x in erolls:
    c=Course.query.filter_by(course_id=x.ecourse_id).first()
    temp+=[c]
  return render_template("studentdetail.html",student=student,course=temp)
@app.route("/student/<int:student_id>/update",methods=["GET"])
def update(student_id):
  if(request.method=="GET"):
    s=Student.query.filter_by(student_id=student_id).first()
    return render_template("updateform.html",s=s)
@app.route("/student/<int:student_id>/updates",methods=["POST"])
def updatei(student_id):
  if(request.method=="POST"):
    sid=student_id
    fn=request.form["f_name"]
    ln=request.form["l_name"]
    s=Student.query.filter_by(student_id=sid).first()
    s.first_name=fn
    s.last_name=ln
    db.session.commit()
    c=enrollments.query.filter_by(estudent_id=student_id).all()
    for x in c:
      db.session.delete(x)
      db.session.commit()
    stri=[]
    if(request.form.items()==None):
      render_template("onecourse.html");
    flag=0
    for key, val in request.form.items():
      if(key.startswith("courses")):
        if(val=="course_1"):
          stri+=["MAD I"]
          flag=1
        elif(val=="course_2"):
          stri+=["DBMS"]
        elif(val=="course_3"):
          stri+=["PDSA"]
        elif(val=="course_4"):
          stri+=["BDM"]
          
    for i in stri:
      c=Course.query.filter_by(course_name=i).first()
      cid=c.course_id
      s=Student.query.filter_by(student_id=sid).first()
      sid=s.student_id
      ward = enrollments(estudent_id=sid, ecourse_id=cid)
      db.session.add(ward)
      db.session.commit()
    student=Student.query.all()
    return render_template("home.html",student=student)

  
if __name__=='__main__':
  app.run(host='0.0.0.0',debug=True,port=8080)