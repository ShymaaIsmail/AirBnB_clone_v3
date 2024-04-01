#!/usr/bin/python3
import os
import inspect
import unittest
from datetime import datetime
import MySQLdb
import pycodestyle
from models.engine.db_storage import DBStorage
from models import storage
from models.state import State
from models.user import User
from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "DB storage not selected")
class TestDBStorageModel(unittest.TestCase):

    def test_doc(self):
        """Test if module and class have docs"""
        self.assertIsNotNone(DBStorage.__doc__, 'no docs for DBStorage Class')
        self.assertIsNotNone(DBStorage.__doc__, 'no docs for module')
        for name, method in inspect.getmembers(DBStorage, inspect.isfunction):
            self.assertIsNotNone(method.__doc__, f"{name} has no docs")

    def test_pycodestyle(self):
        style = pycodestyle.StyleGuide(ignore=['E501', 'W503'])
        module_path = "models/engine/db_storage.py"
        result = style.check_files([module_path])
        self.assertEqual(result.total_errors, 0)

    def setUp(self):
        self.dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        self.cursor = self.dbc.cursor()
        self.dbc_concurrent = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        self.cursor_concurrent = self.dbc_concurrent.cursor()

    def tearDown(self):
        self.cursor.close()
        self.dbc.close()
        self.cursor_concurrent.close()
        self.dbc_concurrent.close()

    def test_new(self):
        """ New object is correctly added to database """
        new = User(
            email='test_user@gmail.com',
            password='password',
            first_name='test',
            last_name='last'
        )
        self.assertFalse(new in storage.all().values())
        new.save()
        self.assertTrue(new in storage.all().values())
        self.cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = self.cursor.fetchone()
        self.assertTrue(result is not None)
        self.assertIn('test_user@gmail.com', result)
        self.assertIn('password', result)
        self.assertIn('test', result)
        self.assertIn('last', result)

    def test_delete(self):
        """ Object is correctly deleted from database """
        new = User(
            email='test@test.com',
            password='password',
            first_name='test',
            last_name='last'
        )
        obj_key = 'User.{}'.format(new.id)
        new.save()
        self.assertTrue(new in storage.all().values())
        self.cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = self.cursor.fetchone()
        self.assertTrue(result is not None)
        self.assertIn('test@test.com', result)
        self.assertIn('password', result)
        self.assertIn('test', result)
        self.assertIn('last', result)
        self.assertIn(obj_key, storage.all(User).keys())
        new.delete()
        self.assertNotIn(obj_key, storage.all(User).keys())

    def test_reload(self):
        """ Tests the reloading of the database session """
        self.cursor.execute(
            'INSERT INTO users(id, created_at, updated_at, email, password' +
            ', first_name, last_name) VALUES(%s, %s, %s, %s, %s, %s, %s);',
            [
                'aa-bb-cc-dd',
                str(datetime.now()),
                str(datetime.now()),
                'mama@baba.com',
                'pass',
                'first',
                'name',
            ]
        )
        self.assertNotIn('User.aa-bb-cc-dd', storage.all())
        self.dbc.commit()
        storage.reload()
        self.assertIn('User.aa-bb-cc-dd', storage.all())

    def test_save(self):
        """ object is successfully saved to database """
        new = User(
            email='test@test.com',
            password='password',
            first_name='test',
            last_name='last'
        )
        self.cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = self.cursor.fetchone()
        self.cursor.execute('SELECT COUNT(*) FROM users;')
        old_cnt = self.cursor.fetchone()[0]
        self.assertTrue(result is None)
        self.assertFalse(new in storage.all().values())
        new.save()
        self.cursor_concurrent.execute('SELECT * FROM users WHERE id="{}"'.
                                       format(new.id))
        result = self.cursor_concurrent.fetchone()
        self.cursor_concurrent.execute('SELECT COUNT(*) FROM users;')
        new_cnt = self.cursor_concurrent.fetchone()[0]
        self.assertFalse(result is None)
        self.assertEqual(old_cnt + 1, new_cnt)
        self.assertTrue(new in storage.all().values())

    def test_storage_var_created(self):
        """ DBStorage object storage created """
        from models.engine.db_storage import DBStorage
        self.assertEqual(type(storage), DBStorage)

    def test_new_and_save(self):
        """testing the new and save methods"""
        new_user = User(**{'first_name': 'firstname',
                           'last_name': 'lasttt',
                           'email': 'firstname@lasttt.com',
                           'password': 'abcd'})
        cur = self.dbc.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        old_count = cur.fetchall()
        new_user.save()
        self.cursor_concurrent.execute('SELECT COUNT(*) FROM users')
        new_count = self.cursor_concurrent.fetchall()
        self.assertEqual(new_count[0][0], old_count[0][0] + 1)

    def test_save_and_get(self):
        # Test saving and retrieving an object
        obj_id = "1"
        obj = State(**{'id': obj_id, 'name': 'california'})
        obj.save()
        self.assertEqual(storage.get(State, obj_id), obj)

    def test_count(self):
        # Test counting objects
        obj1 = State(**{'name': 'new york'})
        obj2 = State(**{'name': 'california'})
        obj3 = User(**{'first_name': 'firstname',
                       'last_name': 'lasttt',
                       'email': 'firstname@lasttt.com',
                       'password': 'abcd'})
        obj1.save()
        obj2.save()
        obj3.save()

        self.assertEqual(storage.count(State), 2)
        self.assertEqual(storage.count(User), 1)


if __name__ == '__main__':
    unittest.main()
