from core.models import DBModel
import re


class User(DBModel):  # User model
    TABLE = 'userstable'
    PK = 'id'

    def __init__(self, name,family, phone, emailAddress, password, user_role, id=None) -> None:
        self.name = name
        self.family = family
        self.phone = phone
        self.emailAddress = emailAddress
        self.password = password
        self.user_role = user_role

        if id: self.id = id

    def isValid(email):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, email):
            return email
        else:
            return f"Invalid email"
