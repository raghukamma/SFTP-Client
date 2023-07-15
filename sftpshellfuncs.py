''' sftpshellfuncs.py
Tazwell B. 7/14/2023
this file should contain functions that the shell executes through the command decoder. 
'''

import os

commands = dict()

# uncomment for ide auto completion reasons
# from pysftp import Connection as t_sftp

# shell functions should take 2 args. The first is the initialized SFTP connection
# and the second is the list of args the user typed, like argv in C. Example:
#       sftp = pysftp.Connection()
# user input = "get foo bar.txt foobar.json"
#       args = ["get", "foo", "bar.txt", "foobar.json"]
def command_function_name(sftp, args):
    if sftp == None:
        return
    print("this is an exmple command")
    return
    
# functions go here:



# prints all commands
def help(sftp, args=None):
    # this does not print the command names aligned, only as a list separated 
    # by two spaces
    termw = os.get_terminal_size().columns
    currw = 0
    key_list = list(commands.keys())
    for key in key_list:
        if len(key) > termw:
            print(key, end=' ')
        else:
            if currw + len(key) + 2 > termw:
                print()
                currw = 0
            print(key, end='  ')
            currw = currw + len(key) + 2
    print('\n')


# to register a new command with the Command Decoder copy the form below:
commands["command_name"] = command_function_name
# copy to here:
commands["help"] = help


del commands["command_name"] # deletes example from command list