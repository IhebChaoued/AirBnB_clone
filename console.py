#!/usr/bin/python3
"""HBNB Command"""
import cmd
from models.base_model import BaseModel
from models import storage
from shlex import split
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Cmd"""
    prompt = '(hbnb) '
    class_name = [
            "BaseModel",
            "User",
            "Place",
            "State",
            "City",
            "Amenity",
            "Review"
            ]

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    do_EOF = do_quit

    def do_help(self, arg):
        """Ask for help"""
        cmd.Cmd.do_help(self, arg)

    def emptyline(self):
        """Just empty"""
        pass

    def do_create(self, arg):
        """Create a new instance of BaseModel, save it, and print the id"""
        arguments = split(arg)
        if len(arguments) == 0:
            print("** class name missing **")
        elif arguments[0] not in self.class_name:
            print("** class doesn't exist **")
        else:
            new_instance = eval(f"{arguments[0]}()")
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """Show command to display the string representation of an instance"""
        arguments = split(arg)
        if len(arguments) == 0:
            print("** class name missing **")
        elif arguments[0] not in self.class_name:
            print("** class doesn't exist **")
        elif len(arguments) < 2:
            print("** instance id missing **")
        else:
            instance_key = f"{arguments[0]}.{arguments[1]}"
            if instance_key in storage.all():
                print(storage.all()[instance_key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Destroy command to delete an instance based on class name and id"""
        arguments = split(arg)
        if len(arguments) == 0:
            print("** class name missing **")
        elif arguments[0] not in self.class_name:
            print("** class doesn't exist **")
        elif len(arguments) < 2:
            print("** instance id missing **")
        else:
            instance_key = f"{arguments[0]}.{arguments[1]}"
            if instance_key in storage.all():
                del storage.all()[instance_key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """Print All"""
        arguments = split(arg)
        if len(arguments) == 0:
            instances_list = [str(value) for value in storage.all().values()]
            print(instances_list)
        elif arguments[0] not in self.class_name:
            print("** class doesn't exist **")
        else:
            class_name = arguments[0]
            class_instances = [
                    str(instance)
                    for instance in storage.all().values()
                    if instance.__class__.__name__ == class_name
                    ]
            print(class_instances)

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        arguments = split(arg)
        if len(arguments) == 0:
            print("** class name missing **")
        elif arguments[0] not in self.class_name:
            print("** class doesn't exist **")
        elif len(arguments) < 2:
            print("** instance id missing **")
        elif f"{arguments[0]}.{arguments[1]}" not in storage.all():
            print("** no instance found **")
        elif len(arguments) < 3:
            print("** attribute name missing **")
        elif len(arguments) < 4:
            print("** value missing **")
        else:
            instance_key = f"{arguments[0]}.{arguments[1]}"
            instance = storage.all()[instance_key]
            attr_name = arguments[2]
            attr_value = arguments[3]
            setattr(instance, attr_name, attr_value)
            instance.save()

    def do_count(self, arg):
        """Count the number of instances of a given class."""
        count = 0
        for instance in storage.all().values():
            if isinstance(instance, eval(arg)):
                count += 1
        print(count)

    def default(self, arg):
        """Handle unrecognized commands in a default manner."""
        arguments = arg.split(".")
        target_class = arguments[0]
        command_parts = arguments[1].split("(")
        issued_command = command_parts[0]
        command_actions = {
                'all': self.do_all,
                'count': self.do_count
                }
        if issued_command not in command_actions.keys():
            if not target_class:
                print("** target class name missing **")
                return
        else:
            return command_actions[issued_command]("{}".format(target_class))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
