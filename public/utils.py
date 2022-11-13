import os.path
import os.path
import time

from configs import INFO as information
from core.managers import DBManager
from users.models import User





def about_us():
    print(
        f"""Store name : {information["name"]}
Description : {information["description"]}
Version : {information["version"]}
"""
    )


db_manager = DBManager(database="postgres", user="postgres", password="123456", host="localhost",
                       port="5432")


def salam(name):
    print("Hello ", name)


def add_comment():
    fileName = input('enter file name')
    description = input('enter your command')
    DBManager.add_comment(db_manager, fileName, description)



def buy_file():
    if DBManager.check_is_login():
        fileName = input('enter file name')
        DBManager.buy_file(db_manager, fileName)
    else:
        print('first login')
        Login()


def Login():
    user_name = input('enter email')
    password_user = input('enter password')
    email_user, password_u = DBManager.login_user(db_manager, user_name, password_user)
    print(email_user, password_u)
    if (email_user == user_name and password_u == password_user):
        print('welcome')
    else:
        print('we dont have this user')


def create_user():
    name, family, phone, emailAddress, password, user_role = input(
        'enter name,family,phone,emailAddress,password,user_role').split(',')
    u1 = User(name, family, phone, User.isValid(emailAddress), password, user_role)
    DBManager.create(db_manager, u1)


def see_files():
    DBManager.read_file(db_manager)


def add_file():
    if DBManager.check_is_login():

        directory = 'D:\maktab_python80\session16\M78__FileStore-main\myFiles'
        filename = input("What is the name of the file: ")
        file_path = os.path.join(directory, filename)
        if not os.path.isdir(directory):
            os.mkdir(directory)
        file = open(file_path, "w")
        toFile = input("Write what you want into the field")
        file.write(toFile)
        file.close()
        print("last modified: %s" % time.ctime(os.path.getmtime(directory + '\\' + filename)))
        print("created: %s" % time.ctime(os.path.getctime(directory + '\\' + filename)))
        DBManager.add_file(db_manager, filename, file_path,
                           "last modified: %s" % time.ctime(os.path.getmtime(directory + '\\' + filename)),
                           "created: %s" % time.ctime(os.path.getctime(directory + '\\' + filename)))


    else:
        print('login first :)')
        Login()