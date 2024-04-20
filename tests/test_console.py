#!/usr/bin/python3
"""
Unit test for the console
"""
import json
import os
import sqlalchemy
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from tests import clear_stream


class TestHBNBCommand(unittest.TestCase):
    """
    Test class for the HBNBCommand class.
    """
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_for_fs_create(self):
        """
        Tests for create command with the file storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            x = HBNBCommand()
            x.onecmd('create City name="New York"')
            y = cout.getvalue().strip()
            clear_stream(cout)
            self.assertIn('City.{}'.format(y), storage.all().keys())
            x.onecmd('show City {}'.format(y))
            self.assertIn("'name': 'New York'", cout.getvalue().strip())
            clear_stream(cout)
            x.onecmd('create User name="Kaysee" age=17 height=5.9')
            y = cout.getvalue().strip()
            self.assertIn('User.{}'.format(y), storage.all().keys())
            clear_stream(cout)
            x.onecmd('show User {}'.format(y))
            self.assertIn("'name': 'Kaysee'", cout.getvalue().strip())
            self.assertIn("'age': 17", cout.getvalue().strip())
            self.assertIn("'height': 5.9", cout.getvalue().strip())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_for_db_create(self):
        """
        Tests for create command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            x = HBNBCommand()
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                x.onecmd('create User')
            clear_stream(cout)
            x.onecmd('create User email="kaysee17@gmail.com" password="234"')
            y = cout.getvalue().strip()
            url = dbcon.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = url.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(y))
            res = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('kaysee17@gmail.com', res)
            self.assertIn('123', res)
            cursor.close()
            url.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_for_db_show(self):
        """
        Tests for show command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            x = HBNBCommand()
            obj = User(email="kaysee17@gmail.com", password="234")
            url = dbcon.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = url.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            res = cursor.fetchone()
            self.assertTrue(result is None)
            x.onecmd('show User {}'.format(obj.id))
            self.assertEqual(
                cout.getvalue().strip(),
                '** no instance found **'
            )
            obj.save()
            url = dbcon.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = url.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            clear_stream(cout)
            x.onecmd('show User {}'.format(obj.id))
            res = cursor.fetchone()
            self.assertTrue(res is not None)
            self.assertIn('kaysee27@gmail.com', res)
            self.assertIn('234', res)
            self.assertIn('kaysee17@gmail.com', cout.getvalue())
            self.assertIn('234', cout.getvalue())
            cursor.close()
            url.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_for_db_count(self):
        """
        Tests for count command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            x = HBNBCommand()
            url = dbcon.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = url.cursor()
            cursor.execute('SELECT COUNT(*) FROM states;')
            res = cursor.fetchone()
            pc = int(res[0])
            cons.onecmd('create State name="Enugu"')
            clear_stream(cout)
            x.onecmd('count State')
            count_this = cout.getvalue().strip()
            self.assertEqual(int(count_this), pc + 1)
            clear_stream(cout)
            x.onecmd('count State')
            cursor.close()
            url.close()
