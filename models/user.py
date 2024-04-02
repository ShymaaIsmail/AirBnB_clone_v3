#!/usr/bin/python3
""" holds class User"""
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib
import models
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user", cascade="all, delete")
        reviews = relationship("Review", backref="user", cascade="all, delete")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        self.secure_password()

    def secure_password(self):
        """set password hashed as MDF5 value"""
        # Create a SHA-256 hash object
        hash_object = hashlib.md5()
        # Update the hash object with the string's bytes
        hash_object.update(self.password.encode())
        # Get the hexadecimal representation of the hash
        sha256_hash = hash_object.digest()
        self.password = sha256_hash
