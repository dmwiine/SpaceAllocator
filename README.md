[![Build Status](https://travis-ci.org/dmwiine/SpaceAllocator.svg?branch=Review)](https://travis-ci.org/dmwiine/SpaceAllocator)  [![Coverage Status](https://coveralls.io/repos/github/dmwiine/SpaceAllocator/badge.svg?branch=Review)](https://coveralls.io/github/dmwiine/SpaceAllocator?branch=Review)
# Dojo Room Allocator    

This is the implementation of a system that randomly allocates rooms to Andela fellows and staff at the Dojo.
 
## Features:
- Create rooms, which can be of type Office or Living Space
- Add people to the Dojo. The people can be Fellows or Staff members
- Randomly allocate offices to staff and fellows. Randomly allocate living spaces to fellows that choose to opt in.
- Load People from a txt file directly into the system.
- Print Allocations of fellows and staff in the various rooms.
- Print all unallocated fellows and staff
- Print all available rooms and the spaces available in each room.
- Load state from a previously saved database
- Save all data you've worked on during a particular session.
 
## Installation and running
```
$ git clone https://github.com/dmwiine/SpaceAllocator.git
$ cd your-dir
$ pip3 install requirements.txt
$ python3 dojo_main.py -i
```
 
 
## Commands, their usage and examples
 
### create_room
This command creates offices and living_spaces in the Dojo. You can create as many offices/living_spaces as you want. 
#### Usage:
`create_room <room_type> <room_name> ...`
##### Example: 
```
create_room office Red Blue Yellow Pink
create_room living_space A B C D 
``` 
### add_person
This command creates a new person and automatically assigns them office or living space as per the user’s specifications . 
#### Usage:
`add_person <first_name> <last_name> <person_type> [<wants_accommodation>]`
##### Example: 
```
add_person Donna Mwiine Staff
add_person Daphne Murungi Fellow Y
add_person David Kimathi Fellow
```
 
### print_room
This command prints all the people allocated to a particular room. 
#### Usage:
`print_room <room_name>`
##### Example:
`print_room Yellow`
 
### print_allocations
This command prints all fellow & staff allocations assigned to a particular room. An optional file name may be provided in which case the results will be saved to a text file. 
#### Usage:
`print_allocations [—-o=<filename>]`
##### Example: 
```
print_allocations
print_allocations allocations.txt
```
 
### reallocate_person
This command reallocates a person to the new room specified. It takes a person’s name and a room name to reallocated them to. 
#### Usage:
`reallocate_person <first_name> <last_name> <new_room_name>`
##### Example: 
`reallocate_person Donna Mwiine Pink`
 
### print_unallocated
This command prints all the fellows and staff that have not been assigned rooms. An optional file name may be provided in which case the results will be saved to a text file. 
#### Usage:
`print_allocations [—-o=<filename>]`
##### Example: 
`print_allocations my_file_name.txt`
 
### print_available_rooms
This prints all the offices and living rooms that have space and how much space they have.
#### Usage:
##### Example: 
`print_available_rooms`
 
### load_people
This command loads people data from a text file. This text file can be found in Files/inputs.txt .
#### Usage:
##### Example: 
`load_people`
 
### save_state
This command saves the data in the current session to a database.
#### Usage:
##### Example: 
`save_state`
 
### load_state
This loads data from a previously saved session. 
#### Usage:
##### Example: 
`load_state` 
 
## Tests
Enables you to run tests on the different parts of the application to ensure that they are running as intended.
 
### Running tests
Open the terminal, cd into the project folder and type in the command below to run tests on the program. Please remember to use the correct python installation on your system.
```python3 -m unittest Tests/<test_file_name>```
 
### Gather test coverage data
Determine the percentage of code tested.
```coverage run -m unittest discover -s Tests```
 
### Print / Output test coverage report
#### Command-line report
Use the commands below to print out a simple command-line report. Be sure to cd into the project folder first.
```coverage report -m```
 
 

 
 
