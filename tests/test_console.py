from console import HBNBCommand
import unittest
from unittest.mock import create_autospec, patch
import sys
from io import StringIO
import os


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

        out_put = ("Documented commands (type help <topic>):\n"
                   "========================================\nEOF  "
                   "all  create  destroy  help  quit  show  update")
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(out_put, f.getvalue().strip())

    def test_help_EOF(self):
        """ test the help with with EOF """

        out_put = ("End Of File")
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

        out_put = ("Creates a new instance")
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(out_put, f.getvalue().strip())

    def test_help_destroy(self):
        """ test the help with destroy """

        out_put = ("Deletes an instance based on the class name and ID")
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(out_put, f.getvalue().strip())

    def test_help_quit(self):
        """ test the help with quit """

        out_put = ("Quit command to exit the program")
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(out_put, f.getvalue().strip())

    def test_help_show(self):
        """ test the help with show """

        out_put = ("Prints the string representation of an instance")
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(out_put, f.getvalue().strip())

    def test_help_update(self):
        """ test the help with update """

        out_put = ("Updates an instance based on the class name and ID")
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

    @unittest.skipIf(type(models.storage) == DBStorage, "db storage test")
    def test_create_kwargs(self):
        """Tesing the create command with keyword base argument"""
        cli = self.create_session()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create Place city_id="0001" user_id="0001" name="My_house"'
            self.HBNBCommand().onecmd(cmd)
            t_output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'all Place'
            self.HBNBCommand().onecmd(cmd)
            r_output = f.getvalue().strip()
            self.assertIn(t_output, r_output)
            self.assertIN("'city_id': '0001'", r_output)
            self.assertIN("'user_id': '0001'", r_output)
            self.assertIN("'name': 'My house'", r_output)
            self.assertNotIN("'latitude':", r_output)

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
            self.assertEqual("** no instance found **",
                             f.getvalue().strip())
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

        """ <class>.show(<id>) method """

        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.show("23456")'.format(cls)))
            self.assertEqual("** no instance found **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.show("{}")'.format(cls, ids)))
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
                self.assertFalse(cli.onecmd('{}.destroy("123456")'
                                 .format(cls)))
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
                self.assertFalse(cli.onecmd('{}.destroy("{}")'
                                 .format(cls, ids)))
            self.assertFalse(ids in f.getvalue().strip())
            self.assertEqual("", f.getvalue().strip())
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('all'))
            self.assertFalse(ids in f.getvalue().strip())

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

        """ <class>.all mode """

        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.all()'.format(cls)))
            self.assertEqual('[', f.getvalue().strip()[0])
            self.assertEqual(']', f.getvalue().strip()[-1])
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.all()'.format(cls)))
            self.assertTrue(ids in f.getvalue().strip())

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

        """
        <class name>.update(<id>, <attribute name>, <attribute value>)
        method
        """

        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.update()'.format(cls)))
            self.assertEqual("** instance id missing **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.update("123456")'.format(cls)))
            self.assertEqual("** no instance found **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.update("{}")'
                                 .format(cls, ids)))
            self.assertEqual("** attribute name missing **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.update("{}", "attribute")'
                                 .format(cls, ids)))
            self.assertEqual("** value missing **", f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.update("{}", "attr", "test")'
                                 .format(cls, ids)))
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('show {} {}'.format(cls, ids)))
            self.assertTrue("attr" in f.getvalue().strip())
            self.assertTrue("test" in f.getvalue().strip())

        """ <class name>.update(<id>, <dictionary representation>) method """

        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.update("{}", {{"num": 89}})'
                                 .format(cls, ids)))
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('show {} {}'.format(cls, ids)))
            self.assertTrue("num" in f.getvalue().strip())
            self.assertTrue("89" in f.getvalue().strip())

    def test_count(self):
        cli = self.create_session()
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.count()'.format(cls)))
                number1 = int(f.getvalue().strip())
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.count()'.format(cls)))
                number2 = int(f.getvalue().strip())
            self.assertTrue(number2 == number1 + 1)

    def test_quit(self):
        """exit command"""
        cli = self.create_session()
        self.assertTrue(cli.onecmd("quit"))

    def test_EOF(self):
        """End Of File"""
        cli = self.create_session()
        self.assertTrue(cli.onecmd("EOF"))
