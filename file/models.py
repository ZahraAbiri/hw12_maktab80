
from core.models import DBModel
import re


class File(DBModel):  # User model
    TABLE = 'files'
    PK = 'id'

    def __init__(self, name, directory, dateCreate, dateLastChange,show_name=None, seller_id=None, id=None) -> None:
        self.name = name
        self.directory = directory
        self.dateCreate = dateCreate
        self.dateLastChange = dateLastChange
        if id: self.show_name = show_name
        if id: self.seller_id = seller_id
        if id: self.id = id









