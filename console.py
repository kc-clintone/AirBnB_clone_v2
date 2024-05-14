#!/usr/bin/python3
"""
The airbnb clone console
"""

import cmd
from datetime import datetime
import models
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity
import shlex
from models.base_model import BaseModel

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class HBNBCommand(cmd.Cmd):
    """ HBNB console """
    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """ Exits/closes console """
        return True

    def emptyline(self):
        """ Empty line cmd """
        return False

    def do_quit(self, arg):
        """ This command exits the program """
        return True

    def _key_value_parser(self, args):
        """ This creates a dict from a list of strings """
        _dict = {}
        for arg in args:
            if "=" in arg:
                kv = arg.split('=', 1)
                k = kv[0]
                value = kv[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except:
                        try:
                            value = float(value)
                        except:
                            continue
                _dict[k] = value
        return _dict

    def do_create(self, arg):
        """ This creates a new instance of a class """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            _dict = self._key_value_parser(args[1:])
            instance = classes[args[0]](**_dict)
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)
        instance.save()

    def do_show(self, arg):
        """ This prints an instance as a string based on the class and id """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """ This deletes an instance based on the class and id """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    models.storage.all().pop(key)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """ This prints string repr of instances """
        args = shlex.split(arg)
        _list = []
        if len(args) == 0:
            _dict = models.storage.all()
        elif args[0] in classes:
            _dict = models.storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in _dict:
            _list.append(str(_dict[key]))
        print("[", end="")
        print(", ".join(_list), end="")
        print("]")

    def do_update(self, arg):
        """ This updates an instance based on the class name, id, attribute & value """
        args = shlex.split(arg)
        ints = ["number_rooms", "number_bathrooms", "max_guest",
                    "price_by_night"]
        floats = ["latitude", "longitude"]
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    if len(args) > 2:
                        if len(args) > 3:
                            if args[0] == "Place":
                                if args[2] in integers:
                                    try:
                                        args[3] = int(args[3])
                                    except:
                                        args[3] = 0
                                elif args[2] in floats:
                                    try:
                                        args[3] = float(args[3])
                                    except:
                                        args[3] = 0.0
                            setattr(models.storage.all()[k], args[2], args[3])
                            models.storage.all()[key].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

if __name__ == '__main__':
    HBNBCommand().cmdloop()
