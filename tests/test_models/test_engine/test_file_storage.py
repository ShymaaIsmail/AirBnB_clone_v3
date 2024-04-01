#!/usr/bin/python3
""" Module for testing file storage"""
import inspect
import unittest
import os
from models.base_model import BaseModel
from models import storage
from models.engine.file_storage import FileStorage
from models.state import State
from models.user import User


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'file', "no")
class TestFileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def test_doc(self):
        """Test if module and class have docs"""
        self.assertIsNotNone(FileStorage.__doc__, 'no')
        self.assertIsNotNone(FileStorage.__doc__, 'no docs for module')
        for name, method in inspect.getmembers(FileStorage,
                                               inspect.isfunction):
            self.assertIsNotNone(method.__doc__, f"{name} has no docs")

    def setUp(self):
        """ Set up test environment """
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        objs = storage.all()
        if objs:
            for obj in objs.values():
                temp = obj
            self.assertTrue(temp is obj)

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = storage.all()
        if temp:
            self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        storage.save()
        storage.reload()
        objects = storage.all()
        if objects:
            for obj in objects.values():
                loaded = obj
            self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """ Load from an empty file """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        _id = new.to_dict()['id']
        objects = storage.all()
        if objects:
            for key in objects.keys():
                temp = key
            self.assertEqual(temp, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        self.assertEqual(type(storage), FileStorage)

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
        self.assertEqual(storage.count(), 3)


if __name__ == '__main__':
    unittest.main()
