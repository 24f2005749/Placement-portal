from controllers.database import db
from sqlalchemy import Enum
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime, UTC

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),unique=True, nullable = False)
    email = db.Column(db.String(30),nullable=False, unique=True)
    password = db.Column(db.String(255),nullable = False)
    role = db.Column(Enum('student','company','admin'), nullable=False)
    active = db.Column(db.Boolean, default=True)

    student = db.relationship("Student",backref="user",uselist=False, cascade="all, delete-orphan")
    company = db.relationship("Company",backref="user",uselist=False, cascade="all, delete-orphan")

    def set_password(self,password):
        self.password = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password,password)
    
class Student(db.Model):                                                               

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False,unique=True)
    full_name = db.Column(db.String(100),nullable=False)
    roll_number = db.Column(db.String(50),unique=True,nullable=False)
    branch_id = db.Column(db.Integer,db.ForeignKey("branches.id"),nullable=False)
    cgpa = db.Column(db.Float, nullable = False)
    graduation_year = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(20))
    resume = db.Column(db.String(255))
    
    branch = db.relationship("Branch",backref="students")
    applications = db.relationship("Application",backref="student",cascade = "all, delete-orphan")


class Company(db.Model):
    
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable =False, unique=True)
    company_name = db.Column(db.String(150), nullable= False)
    website = db.Column(db.String(255))
    hr_name = db.Column(db.String(100))
    hr_email = db.Column(db.String(100))
    description = db.Column(db.Text)
    approval_status = db.Column(Enum("pending","approved","rejected"), default = "pending", nullable=False)

    drives = db.relationship("Drive",backref ="company", cascade = "all, delete-orphan")


class Application(db.Model):

    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("students.id"),nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("drives.id"),nullable=False)
    applied_at = db.Column(db.DateTime,nullable=False,default=lambda: datetime.now(UTC))          
    status = db.Column(Enum("applied","shortlisted","selected","rejected",name="application_status"), default = "applied", nullable=False)
    interview_date = db.Column(db.DateTime)
    remarks = db.Column(db.Text)
    __table_args__ = (db.UniqueConstraint("student_id","drive_id",name="unique_application"),)
    
class Drive(db.Model):
    
    __tablename__ = "drives"

    id = db.Column(db.Integer, primary_key = True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    title = db.Column(db.String(150),nullable = False)
    job_description = db.Column(db.Text, nullable = False)
    salary_package = db.Column(db.Float)
    location = db.Column(db.String(150))
    eligibility_year = db.Column(db.Integer)
    eligibility_cgpa = db.Column(db.Float)
    application_deadline= db.Column(db.Date,nullable=False)
    drive_date=db.Column(db.Date)
    approval_status = db.Column(Enum("pending","approved","rejected"), default = "pending")
    status = db.Column(Enum("open","closed"), default = "open")

    applications = db.relationship("Application", backref="drive", cascade="all, delete-orphan")

    
class Branch(db.Model):
    
    __tablename__ = "branches"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    drives = db.relationship("Drive",secondary="eligible_branches",backref="branches")

class EligibleBranch(db.Model):

    __tablename__ = "eligible_branches"

    drive_id = db.Column(db.Integer,  db.ForeignKey("drives.id"), nullable=False, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey("branches.id"), nullable=False, primary_key=True)
