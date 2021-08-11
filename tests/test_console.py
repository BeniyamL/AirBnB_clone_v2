from console import HBNBCommand
import unittest
from unittest.mock import create_autospec, patch
import sys
from io import StringIO
import os
import models
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage


class TestConsole_prompt(unittest.TestCase):
    """ class definition for test console class"""

    def test_console_prompt_message(self):
        """ function to test the prompt message """
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(self):
        """ function to test the empty line """
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", f.getvalue().strip())


class TestHelpFunction(unittest.TestCase):
    """ function to test the help """

    def test_help(self):
        """ test the help with no argumnet """

        out = ("Documented commands (type help <topic>):\n"
               "========================================\n"
               "EOF  all  count  create  destroy  help  quit  show  update")
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(out, f.getvalue().strip())

    def test_help_EOF(self):
        """ test the help with with EOF """

        out_put = ("Exits the program without formatting")
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(out_put, f.getvalue().strip())

    def test_help_all(self):
        """ test the help with with all """

        out = ("Prints all str repr of all instances of class name")
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(out, f.getvalue().strip())

    def test_help_create(self):
        """ test the help with create """

        out_put = ("Creates a class of any type\n"
                   "[Usage]: create <className>")
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(out_put, f.getvalue().strip())

    def test_help_destroy(self):
        """ test the help with destroy """

        out_put = ("Destroys an individual instance of a class\n"
                   "[Usage]: destroy <className> <objectId>")
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(out_put, f.getvalue().strip())

    def test_help_quit(self):
        """ test the help with quit """

        out_put = ("Exits the program with formatting")
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(out_put, f.getvalue().strip())

    def test_help_show(self):
        """ test the help with show """

        out_put = ("Shows an individual instance of a class\n"
                   "[Usage]: show <className> <objectId>")
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(out_put, f.getvalue().strip())

    def test_help_update(self):
        """ test the help with update """

        out_put = ("Updates an object with new information\n"
                   "Usage: update <className> <id> <attName> <attVal>")
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(out_put, f.getvalue().strip())


class TestConsole(unittest.TestCase):

    classes = ["BaseModel", "User", "State", "City",
               "Amenity", "Place", "Review"]

    @classmethod
    def teardown(cls):
        """ final statement """
        try:
            os.remove("file.json")
        except Exception:
            pass

    def setUp(self):
        self.mock_stdin = create_autospec(sys.stdin)
        self.mock_stdout = create_autospec(sys.stdout)

    def create_session(self, server=None):
        return HBNBCommand(stdin=self.mock_stdin, stdout=self.mock_stdout)

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_create_kwargs(self):
        """Test create command with kwargs."""
        with patch("sys.stdout", new=StringIO()) as f:
            call = ('create Place city_id="0001" name="My_house" '
                    'number_rooms=4 latitude=37.77 longitude=a')
            HBNBCommand().onecmd(call)
            pl = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all Place")
            output = f.getvalue()
            self.assertIn(pl, output)
            self.assertIn("'city_id': '0001'", output)
            self.assertIn("'name': 'My house'", output)
            self.assertIn("'number_rooms': 4", output)
            self.assertIn("'latitude': 37.77", output)
            self.assertNotIn("'longitude'", output)

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_create(self):
        """Tesing `active` command"""
        cli = self.create_session()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(cli.onecmd('create'))
        self.assertEqual('** class name missing **',
                         f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(cli.onecmd('create obj'))
        self.assertEqual("** class doesn't exist **",
                         f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
            self.assertEqual(36, len(f.getvalue().strip()))

    def test_show(self):
        cli = self.create_session()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(cli.onecmd('show'))
        self.assertEqual('** class name missing **',
                         f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(cli.onecmd('show obj'))
        self.assertEqual("** class doesn't exist **",
                         f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('show {}'.format(cls)))
            self.assertEqual("** instance id missing **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('show {} 123456'.format(cls)))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('show {} {}'.format(cls, ids)))
            self.assertTrue(ids in f.getvalue().strip())
            self.assertTrue(cls in f.getvalue().strip())
            self.assertTrue("created_at" in f.getvalue().strip())
            self.assertTrue("updated_at" in f.getvalue().strip())

    def test_destroy(self):
        cli = self.create_session()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(cli.onecmd('destroy'))
        self.assertEqual('** class name missing **',
                         f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(cli.onecmd('destroy obj'))
        self.assertEqual("** class doesn't exist **",
                         f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('destroy {}'.format(cls)))
            self.assertEqual("** instance id missing **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('destroy {} 123456'.format(cls)))
            self.assertEqual("** no instance found **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('all'))
            self.assertTrue(ids in f.getvalue().strip())
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('destroy {} {}'.format(cls, ids)))
            self.assertFalse(ids in f.getvalue().strip())
            self.assertEqual("", f.getvalue().strip())
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('all'))
            self.assertFalse(ids in f.getvalue().strip())

        """ <class>.destroy(<id>) method """

        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('all'))
            self.assertTrue(ids in f.getvalue().strip())
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.destroy("{}")'
                                 .format(cls, ids)))
            self.assertFalse(ids in f.getvalue().strip())
            self.assertEqual("", f.getvalue().strip())
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('all'))
            self.assertTrue(ids in f.getvalue().strip())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_all(self):
        cli = self.create_session()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(cli.onecmd('all'))
        self.assertEqual('[', f.getvalue().strip()[0])
        self.assertEqual(']', f.getvalue().strip()[-1])
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(cli.onecmd('all obj'))
        self.assertEqual("** class doesn't exist **",
                         f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('all {}'.format(cls)))
                self.assertEqual('[', f.getvalue().strip()[0])
                self.assertEqual(']', f.getvalue().strip()[-1])
            self.assertTrue(ids in f.getvalue().strip())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_update(self):
        cli = self.create_session()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(cli.onecmd('update'))
        self.assertEqual('** class name missing **',
                         f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(cli.onecmd('update obj'))
        self.assertEqual("** class doesn't exist **",
                         f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('update {}'.format(cls)))
            self.assertEqual("** instance id missing **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('update {} 123456'.format(cls)))
            self.assertEqual("** no instance found **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('update {} {}'.format(cls, ids)))
            self.assertEqual("** attribute name missing **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('update {} {} attribute'
                                 .format(cls, ids)))
            self.assertEqual("** value missing **", f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('update {} {} attribute "test"'
                                 .format(cls, ids)))
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('show {} {}'.format(cls, ids)))
            self.assertTrue("attribute" in f.getvalue().strip())
            self.assertTrue("test" in f.getvalue().strip())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_count(self):
        cli = self.create_session()
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.count()'.format(cls)))
                number1 = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.count()'.format(cls)))
                number2 = f.getvalue().strip()
                print(number2)

    def test_quit(self):
        """exit command"""
        cli = self.create_session()
        self.assertTrue(cli.onecmd("quit"))

    def test_EOF(self):
        """End Of File"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd("EOF"))
