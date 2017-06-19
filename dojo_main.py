"""
Usage:
    dojo_main.py create_room <room_type> <room_name>...
    dojo_main.py add_person <first_name> <last_name> <person_type> [<wants_accomodation>]
    dojo_main.py print_room <room_name>
    dojo_main.py print_allocations [--o=<filename>]
    dojo_main.py print_unallocated [--o=<filename>]
    dojo_main.py reallocate_person <first_name> <last_name> <new_room_name>
    dojo_main.py print_available_rooms
    dojo_main.py load_people
    dojo_main.py save_state [--db=sqlite_database]
    dojo_main.py save_state [sqlite_database]
    dojo_main.py (-i | --interactive)
    dojo_main.py (-h | --help)

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    --o=<filename>  Filename to save output
    --db=sqlite_database
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from app.dojo import Dojo

dojo = Dojo()
#Citation: Source => https://github.com/docopt/docopt/blob/master/examples/interactive_example.py
def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn
# End of citation

class TheDojo(cmd.Cmd):
    """ The main dojo room allocator launch class. """

    intro = '******************* Welcome to the Dojo Room Allocator' \
        + ' (type help for a list of commands ********************.)'
    prompt = '(dojo_main) '
    file = None

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_name>..."""

        room_type = arg["<room_type>"]
        room_names = arg["<room_name>"]
        try:
            dojo.create_room(room_type.lower(), room_names)
            length = len(room_names)
            if length > 0:
                print("********************** Rooms successfully created ************************")
            else:
                print("********************** Room successfully created ************************")
        except (ValueError, TypeError):
            print("Oops! Invalid room name/room type OR the room has already been created")

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> <person_type> [<wants_accomodation>]"""
        first_name = arg["<first_name>"].upper()
        last_name = arg["<last_name>"].upper()
        person_name = first_name + " " + last_name
        person_type = arg["<person_type>"].upper()
        wants_accomodation = arg["<wants_accomodation>"]

        try:
            if wants_accomodation is None:
                wants_accomodation = "N"

            if person_type == "FELLOW":
                dojo.add_fellow(person_name, wants_accomodation.upper())
            elif person_type == "STAFF":
                dojo.add_staff(person_name)
            else:
                print("Please enter a valid person type.(FELLOW|STAFF)")
            print(person_name + " successfully created.")
        except ValueError:
            print("Oops! The person already exists OR No rooms have been created yet")

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
        try:
            room_name = arg["<room_name>"].upper()
            dojo.print_room(room_name)
        except ValueError:
            print("Ooops! The room name does not exist in the system")

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=filename.txt]"""
        try:
            print_to_text = arg['--o']
            if print_to_text:
                dojo.print_allocations_to_a_file(print_to_text)
                print("Done saving allocations to file.")
            else:
                dojo.print_allocations()
        except ValueError:
            print("Please enter a valid file name")

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename.txt]"""
        try:
            print_to_text = arg['--o']
            if print_to_text:
                dojo.print_unallocated_to_file(print_to_text)
                print("Done saving the unallocated to file.")
            else:
                dojo.print_unallocated()
        except ValueError:
            print("Please enter a valid file name")

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <first_name> <last_name> <new_room_name>"""
        first_name = arg['<first_name>'].upper()
        last_name = arg['<last_name>'].upper()
        person_name = first_name + " " + last_name
        new_room_name = arg['<new_room_name>'].upper().strip()
        try:
            dojo.reallocate_person(person_name, new_room_name)
        except ValueError:
            print("Oops! The room has no available space or It doesn't exist. ")

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people"""
        try:
            dojo.load_people('inputs.txt')
            print("************* People successfully loaded from file **************")
        except ValueError:
            print("Oops! The person already exists OR No rooms have been created yet")

    @docopt_cmd
    def do_print_available_rooms(self, arg):
        """Usage: print_available_rooms"""
        try:
            dojo.print_all_available_rooms()
        except Exception:
            print("Oops! Something went wrong")


    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=sqlite_database]"""
        try:
            print("Saving data. Please wait.........................")
            dojo.save_state()
            print("************ Data successfully saved in the database *************")
        except Exception:
            print("Ooops! Sorry saving of data into the database has failed")

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: save_state [--db=sqlite_database]"""
        try:
            print("Loading the data. Please wait.........................")
            dojo.load_state()
            print("************** Data successfully loaded into the Dojo ***************")
        except Exception:
            print("Ooops! Sorry loading of data from the database has failed")

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('********************** Good Bye! **********************')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive'] or opt['-i']:
    TheDojo().cmdloop()



