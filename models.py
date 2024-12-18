from extensions import db
from flask_login import UserMixin

class Test(db.Model):
    Test_Id = db.Column(db.Integer, primary_key=True, nullable=False)
    Test_Type = db.Column(db.String(50), nullable=False)

class Marks(db.Model):
    Rno = db.Column(db.String(20), nullable=False)
    Branch = db.Column(db.String(50), nullable=False)
    Sem = db.Column(db.Integer, nullable=False)
    Test_Id = db.Column(db.Integer, db.ForeignKey('test.Test_Id'), nullable=False)
    CId = db.Column(db.Integer, db.ForeignKey('course.CId'), nullable=False)
    Marks = db.Column(db.Integer, nullable=False)
    __table_args__ = (
        db.PrimaryKeyConstraint('Rno', 'Branch', 'Sem', 'Test_Id', 'CId'),
    )


# Models
class Course(db.Model):
    __tablename__ = 'course'
    CId = db.Column(db.Integer, primary_key=True)
    Cname = db.Column(db.String(100), nullable=False)
    Sem = db.Column(db.Integer, nullable=False)

    attendances = db.relationship('Attendance', back_populates='course', lazy=True)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    Attendance_Id = db.Column(db.Integer, primary_key=True)
    Rno = db.Column(db.String(20), db.ForeignKey('user.Rno'), nullable=False)
    Branch = db.Column(db.String(50), db.ForeignKey('user.Branch'), nullable=False)
    Sem = db.Column(db.Integer, db.ForeignKey('user.Sem'), nullable=False)
    CId = db.Column(db.Integer, db.ForeignKey('course.CId'), nullable=False)
    Classes = db.Column(db.Integer, nullable=False)
    Attended = db.Column(db.Integer, nullable=False)
    Attendance_perc = db.Column(db.Float, nullable=False)

    course = db.relationship('Course', back_populates='attendances', lazy=True)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    Rno = db.Column(db.String(20), primary_key=True)
    Branch = db.Column(db.String(50), primary_key=True)
    Sem = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Fname = db.Column(db.String(50), nullable=False)
    Lname = db.Column(db.String(50), nullable=False)

    def get_id(self):
        return f"{self.Rno}|{self.Branch}|{self.Sem}"