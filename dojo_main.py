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
    dojo_main.py load_state <sqlite_database>
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
import os
from docopt import docopt, DocoptExit
from colorama import init
from colorama import Fore, Style
from app.dojo import Dojo
from Models.dojo_DB import DojoDB

dojo = Dojo()
dojo_db = DojoDB()
path = os.path.dirname(os.path.abspath(__file__)) + '/'
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
    """The main dojo room allocator launch class."""
    print()
    intro = '******************* Welcome to the Dojo Room Allocator' \
        + ' (type help for a list of commands ********************.)'
    prompt = 'Enter Command=> '
    file = None
    print()

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_name>..."""

        room_type = arg["<room_type>"]
        room_names = arg["<room_name>"]
        try:
            dojo.create_room(room_type.lower(), room_names)
            length = len(room_names)
            if length > 0:
                print()
                print(Fore.GREEN + "***************** Rooms successfully created *****************")
                print(Style.RESET_ALL)
                print()
            else:
                print()
                print(Fore.GREEN + "***************** Room successfully created ******************")
                print(Style.RESET_ALL)
                print()
        except (ValueError, TypeError) as err:
            print()
            print(Fore.RED + str(err))
            print(Style.RESET_ALL)

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> <person_type> [<wants_accomodation>]"""

        first_name = arg["<first_name>"].upper()
        last_name = arg["<last_name>"].upper()
        person_name = first_name + " " + last_name
        person_type = arg["<person_type>"].upper()
        wants_accomodation = arg["<wants_accomodation>"].upper()

        try:
            if wants_accomodation is None:
                wants_accomodation = "N"
            if person_type == "STAFF" and wants_accomodation == "Y":
                print()
                print(Fore.RED +"Unfortunately a staff cannot get accomodation at the dojo")
            if person_type == "FELLOW":
                dojo.add_fellow(person_name, wants_accomodation.upper())
            elif person_type == "STAFF":
                dojo.add_staff(person_name)
            else:
                print()
                print(Fore.RED + "Please enter a valid person type.(FELLOW|STAFF)")
                print(Style.RESET_ALL)
                print()
            print()
            print(Fore.GREEN + person_name + " successfully created.")
            print(Style.RESET_ALL)
            print()
        except ValueError as err:
            print()
            print(Fore.RED + str(err))
            print()
            print(Style.RESET_ALL)

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
        try:
            room_name = arg["<room_name>"].upper()
            dojo.print_room(room_name)
        except ValueError as err:
            print()
            print(Fore.RED + str(err))
            print(Style.RESET_ALL)
            print()
    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=filename.txt]"""
        try:
            print_to_text = arg['--o']
            #if print_to_text:
            dojo.print_allocations(print_to_text)
                #print()
                #print(Fore.GREEN + "Done saving allocations to file.")
                #print(Style.RESET_ALL)
                #print()
            #else:
                #dojo.print_allocations()
            print()
        except ValueError as err:
            print()
            print(Fore.RED + str(err))
            print(Style.RESET_ALL)
            print()

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename.txt]"""
        try:
            print_to_text = arg['--o']
            #if print_to_text:
            dojo.print_unallocated(print_to_text)
                #print()
                #print(Fore.GREEN + "Done saving the unallocated to file.")
                #print(Style.RESET_ALL)
                #print()
            #else:
                #print()
                #dojo.print_unallocated()
            print()
        except ValueError as err:
            print()
            print(Fore.RED + str(err))
            print(Style.RESET_ALL)
            print()

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <first_name> <last_name> <new_room_name>"""
        first_name = arg['<first_name>'].upper()
        last_name = arg['<last_name>'].upper()
        person_name = first_name + " " + last_name
        new_room_name = arg['<new_room_name>'].upper().strip()
        try:
            dojo.reallocate_person(person_name, new_room_name)
            print()
            print(Fore.GREEN + person_name + " has been reallocated to " + new_room_name)
            print(Style.RESET_ALL)
            print()
        except (ValueError, KeyError) as err:
            print()
            print(Fore.RED + str(err))
            print(Style.RESET_ALL)
            print()

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people"""
        try:
            input_path = "/Users/donna/Documents/Andela/SpaceAllocator/"
            if not os.path.exists(input_path + 'inputs.txt'):
                print(Fore.RED + "inputs.txt file does not exist")
                return
            dojo.load_people('inputs.txt')
            print()
            print(Fore.GREEN + "************* People successfully loaded from file **************")
            print(Style.RESET_ALL)
            print()
        except ValueError as err:
            print()
            print(Fore.RED + str(err))
            print(Style.RESET_ALL)
            print()

    @docopt_cmd
    def do_print_available_rooms(self, arg):
        """Usage: print_available_rooms"""
        try:
            print()
            dojo.print_all_available_rooms()
            print()
        except Exception:
            print()
            print(Fore.RED + "Oops! Something went wrong")
            print(Style.RESET_ALL)
            print()


    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=sqlite_database]"""
        try:
            database_name = arg['--db']
            if database_name is None:
                database_name = 'dojo_db'

            if database_name == 'dojo_db':
                if os.path.exists(path + database_name + '.db'):
                    database = dojo_db.read_db(database_name)
                else:
                    database = dojo_db.create_db(database_name)
            else:
                if os.path.exists(path + database_name + '.db'):
                    database = dojo_db.read_db(database_name)
                else:
                    database = dojo_db.create_db(database_name)

            dojo.session = database.session

            print()
            print(Fore.BLUE + "Saving data. Please wait.........................")
            print()
            dojo.save_state()
            print(Fore.GREEN + "************ Data successfully saved in the database *************")
            print(Style.RESET_ALL)
            print()
        except Exception:
            print()
            print(Fore.RED + "Ooops! Sorry saving of data into the database has failed")
            print(Style.RESET_ALL)

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state <sqlite_database>"""
        try:
            database_name = arg['<sqlite_database>']
            if os.path.exists(path + database_name + '.db'):
                database = dojo_db.read_db(database_name)
                dojo.session = database.session
                dojo.reset()
                print()
                print(Fore.BLUE + "Loading the data. Please wait.........................")
                dojo.load_state()
                print()
                print(Fore.GREEN + "********* Data successfully loaded into the Dojo **********")
                print(Style.RESET_ALL)
                print()
            else:
                print(Fore.RED + '{}.db does not exit.'.format(database_name))
                print(Style.RESET_ALL)
        except Exception:
            print()
            print(Fore.RED + "Ooops! Sorry loading of data from the database has failed")
            print(Style.RESET_ALL)
            print()

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""
        print()
        print(Fore.CYAN + '********************** Good Bye! **********************')
        print(Style.RESET_ALL)
        print()
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive'] or opt['-i']:
    TheDojo().cmdloop()




