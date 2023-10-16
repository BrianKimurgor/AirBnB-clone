#!/usr/bin/python3
"""Defining a module"""
import cmd
from models import storage
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """Command line interpreter for HBNB"""

    prompt = "(hbnb) "

    def do_EOF(self, arg):
        """Exit the console."""
        return True

    def do_quit(self, arg):
        """Exit the console."""
        return True

    def emptyline(self):
        """Handles an empty line to excute nothing"""

        pass

    def do_create(self, arg):
        """Create a new object."""
        if not arg:
            print("** class name missing **")
        elif arg not in storage.classes():
            print("** class doesn't exist **")
        else:
            classes = storage.classes()
            obj = classes[arg]()
            obj.save()
            print(obj.id)

    def do_show(self, arg):
        """Show the details of an object."""

        if arg == "" or arg is None:
            print("** class name missing **")
        else:
            args = arg.split(" ")
            class_name = args[0]
            if class_name not in storage.classes():
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                inst_id = args[1]
                key = "{}.{}".format(class_name, inst_id)
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, arg):
        """Destroy an object."""

        if arg == "" or arg is None:
            print("** class name missing **")
        else:
            args = arg.split(" ")
            class_name = args[0]
            if class_name not in storage.classes():
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                inst_id = args[1]
                key = "{}.{}".format(class_name, inst_id)
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, arg):
        """Show all objects or objects of a specific class."""

        if arg != "":
            args = arg.split(" ")
            class_name = args[0]
            if class_name not in storage.classes():
                print("** class doesn't exist **")
            else:
                inst_list = []
                for k, v in storage.all().items():
                    inst_list.append(str(v))
                print(inst_list)
        else:
            inst_list = []
            for k, v in storage.all().items():
                v = str(v)
                inst_list.append(v)
            print(inst_list)

    def do_update(self, arg):
        """Update an object with new attributes."""
        args = arg.split()

        if not args:
            print("** class name missing **")
            return

        classname = args[0]
        if classname not in storage.classes():
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        uid = args[1]
        key = "{}.{}".format(classname, uid)

        if key not in storage.all():
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        attribute = args[2]

        if len(args) < 4:
            print("** value missing **")
            return

        value = args[3]
        cast = None
        if '.' in value:
            cast = float
        else:
            cast = int

        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]

        attributes = storage.attributes()[classname]

        if attribute in attributes:
            if attribute not in ["id", "created_at", "update_at"]:
                value = attributes[attribute](value)
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()
        elif cast:
            try:
                value = cast(value)
            except ValueError:
                pass

        setattr(storage.all()[key], attribute, value)
        storage.all()[key].save()

    def do_count(self, arg):
        """to retrieve the number of instances of a
            class: <class name>.count().
        """
        args = arg.split(" ")
        if not args[0]:
            print("** class name missing **")
        elif args[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            matches = []
            for k in storage.all():
                if k.startswith(args[0] + '.'):
                    matches.append(k)
            print(len(matches))


if __name__ == "__main__":
    HBNBCommand().cmdloop()
