"""
Usage:
    dojo_main.py create_room <room_type> <room_name>...
    dojo_main.py add_person <first_name> <last_name> (FELLOW|STAFF) [<wants_accomodation>]
    dojo_main.py print_room <room_name>
    dojo_main.py print_allocations [--o=<filename>]
    dojo_main.py print_unallocated [--o=<filename>]
    dojo_main.py reallocate_person <first_name> <last_name> <new_room_name>
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
"""
The main dojo room allocator launch class.
"""
class TheDojo(cmd.Cmd):
    intro = '******************* Welcome to the Dojo Room Allocator' \
        + ' (type help for a list of commands ********************.)'
    prompt = '(dojo_main) '
    file = None

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_name>..."""

        room_type = arg["<room_type>"]
        room_names = arg["<room_name>"]
        dojo.create_room(room_type.lower(), room_names)
        length = len(room_names)
        if length > 0:
            print("********************** Rooms successfully created ************************")
        else:
            print("********************** Room successfully created ************************")

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> (FELLOW|STAFF) [<wants_accomodation>]"""
        first_name = arg["<first_name>"].upper()
        last_name = arg["<last_name>"].upper()
        person_name = first_name + " " + last_name
        fellow = arg["FELLOW"]
        staff = arg["STAFF"]
        wants_accomodation = arg["<wants_accomodation>"]

        if fellow is None:
            dojo.add_fellow(person_name, wants_accomodation.upper())

        if staff is None:
            dojo.add_staff(person_name)
        print(person_name + " successfully created.")

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
        room_name = arg["<room_name>"]
        dojo.print_room(room_name)

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=filename.txt]"""
        print_to_text = arg['--o']
        if print_to_text:
            dojo.print_allocations_to_a_file(print_to_text)
            print("Done saving allocations to file.")
        else:
            dojo.print_allocations()

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename.txt]"""
        print_to_text = arg['--o']
        if print_to_text:
            dojo.print_unallocated_to_file(print_to_text)
            print("Done saving the unallocated to file.")
        else:
            dojo.print_unallocated()

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <first_name> <last_name> <new_room_name>"""
        first_name = arg['<first_name>'].upper()
        last_name = arg['<last_name>'].upper()
        person_name = first_name + " " + last_name
        new_room_name = arg['<new_room_name>']
        dojo.reallocate_person(person_name, new_room_name)

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people"""
        dojo.load_people('inputs.txt')
        print("************* People successfully loaded from file **************")

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=sqlite_database]"""
        print("Saving data. Please wait.........................")
        dojo.save_state()
        print("************ Data successfully saved in the database *************")

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: save_state [--db=sqlite_database]"""
        print("Loading the data. Please wait.........................")
        dojo.load_state()
        print("************** Data successfully loaded into the Dojo ***************")
    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('********************** Good Bye! **********************')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive'] or opt['-i']:
    TheDojo().cmdloop()



