import os

class Config:
    SECRET_KEY = 'a0f0d5a116e1e6b03e394451f2b7476c'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://admin81:admin81@localhost/attendance_system' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False