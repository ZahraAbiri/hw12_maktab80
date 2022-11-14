import os.path
import os.path
import time

from configs import INFO as information
from core.managers import DBManager
from users.models import User
import logging

logging.basicConfig(level=logging.INFO)
file_handler = logging.FileHandler("buyFile.log")
logger = logging.getLogger()
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(level=logging.INFO)
stream_format = logging.Formatter('%(asctime)s-%(name)-10s -%(levelname)-16s - %(filename)s - %(message)s')
file_format = logging.Formatter('%(asctime)s-%(name)s -%(levelname)s - %(filename)s - %(message)s')
stream_handler.setFormatter(stream_format)
file_handler.setFormatter(file_format)


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
    logging.basicConfig(filename='buyFile.log', filemode='a', level=logging.INFO)
    logger.info(
        f'fileName {fileName} description {description} ')


def buy_file():
    if DBManager.check_is_login():
        fileName = input('enter file name')
        DBManager.buy_file(db_manager, fileName)
    else:
        print('first login')
        Login()
    logging.basicConfig(filename='buyFile.log', filemode='a', level=logging.INFO)
    logger.info(
        f'buy_file')


def Login():
    user_name = input('enter email')
    password_user = input('enter password')
    email_user, password_u = DBManager.login_user(db_manager, user_name, password_user)
    print(email_user, password_u)
    if (email_user == user_name and password_u == password_user):
        print('welcome')
    else:
        print('we dont have this user')
    logging.basicConfig(filename='buyFile.log', filemode='a', level=logging.INFO)
    logger.info(
        f'login {user_name} ')

def create_user():
    name, family, phone, emailAddress, password, user_role = input(
        'enter name,family,phone,emailAddress,password,user_role').split(',')
    u1 = User(name, family, phone, User.isValid(emailAddress), password, user_role)
    DBManager.create(db_manager, u1)
    logging.basicConfig(filename='buyFile.log', filemode='a', level=logging.INFO)
    logger.info(
        f'name {name} family {family}phone {phone}emailAddress {emailAddress}create ')


def see_files():
    DBManager.read_file(db_manager)
    logging.basicConfig(filename='buyFile.log', filemode='a', level=logging.INFO)
    logger.info(
        f'seefiles')


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

        logging.basicConfig(filename='buyFile.log', filemode='a', level=logging.INFO)
        logger.info(
            f'fileName {filename} file_path {file_path} create')
    else:
        print('login first :)')
        Login()